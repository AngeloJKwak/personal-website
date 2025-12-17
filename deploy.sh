#!/bin/bash

# Portfolio Deployment Script for Digital Ocean
# Run this on your Digital Ocean droplet

set -e

echo "🚀 Portfolio Deployment Script"
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Get domain name
read -p "Enter your domain name (e.g., example.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo -e "${RED}Domain name is required${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Installing dependencies...${NC}"

# Update system
apt update && apt upgrade -y

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl start docker
    systemctl enable docker
else
    echo "Docker already installed"
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "Docker Compose already installed"
fi

# Install Certbot
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    apt install certbot -y
else
    echo "Certbot already installed"
fi

echo ""
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}Please edit .env file with your actual values${NC}"
        echo "Run: nano .env"
        exit 0
    else
        echo -e "${RED}Error: .env.example not found${NC}"
        exit 1
    fi
fi

# Update nginx.conf with domain
echo "Updating nginx.conf with domain: $DOMAIN"
sed -i "s/your-domain.com/$DOMAIN/g" nginx.conf

# Build Docker image
echo ""
echo -e "${GREEN}Building Docker image...${NC}"
docker-compose build

# Start Flask app only (for SSL setup)
echo ""
echo -e "${GREEN}Starting Flask application...${NC}"
docker-compose up -d web

# Wait for app to be ready
echo "Waiting for application to start..."
sleep 10

# Test if app is running
if curl -f http://localhost:5000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Application is running${NC}"
else
    echo -e "${RED}✗ Application failed to start${NC}"
    echo "Check logs with: docker-compose logs web"
    exit 1
fi

# Get SSL certificate
echo ""
echo -e "${GREEN}Obtaining SSL certificate...${NC}"
echo "This will validate your domain ownership"

# Stop nginx if running
docker-compose stop nginx 2>/dev/null || true

# Get certificate
certbot certonly --standalone --agree-tos --no-eff-email -d $DOMAIN -d www.$DOMAIN

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SSL certificate obtained${NC}"
    
    # Create certbot directories
    mkdir -p certbot/conf certbot/www
    
    # Copy certificates
    cp -r /etc/letsencrypt/* certbot/conf/
    
    # Start all services
    echo ""
    echo -e "${GREEN}Starting all services...${NC}"
    docker-compose up -d
    
    # Wait for services to start
    sleep 5
    
    # Check status
    echo ""
    echo -e "${GREEN}Checking service status...${NC}"
    docker-compose ps
    
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}🎉 Deployment Complete!${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo "Your website is now live at:"
    echo -e "${GREEN}https://$DOMAIN${NC}"
    echo -e "${GREEN}https://www.$DOMAIN${NC}"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "To restart services:"
    echo "  docker-compose restart"
    echo ""
    
    # Set up SSL renewal
    echo "Setting up SSL auto-renewal..."
    cat > /opt/renew-ssl.sh << 'EOF'
#!/bin/bash
docker-compose -f $(pwd)/docker-compose.yml stop nginx
certbot renew --quiet
cp -r /etc/letsencrypt/* $(pwd)/certbot/conf/
docker-compose -f $(pwd)/docker-compose.yml start nginx
EOF
    
    chmod +x /opt/renew-ssl.sh
    
    # Add to crontab if not already there
    if ! crontab -l | grep -q "renew-ssl.sh"; then
        (crontab -l 2>/dev/null; echo "0 3 * * 1 /opt/renew-ssl.sh >> /var/log/ssl-renew.log 2>&1") | crontab -
        echo -e "${GREEN}✓ SSL auto-renewal configured${NC}"
    fi
    
else
    echo -e "${RED}✗ Failed to obtain SSL certificate${NC}"
    echo ""
    echo "Make sure:"
    echo "1. Your domain DNS is pointing to this server"
    echo "2. Ports 80 and 443 are open"
    echo "3. No other service is using port 80"
    echo ""
    echo "Your site is still accessible at:"
    echo "http://$DOMAIN (without SSL)"
fi

echo ""
echo "Deployment script finished!"
