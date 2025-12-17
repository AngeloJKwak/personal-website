# 🚀 Digital Ocean Deployment Guide

## Complete guide to containerize and deploy your portfolio to Digital Ocean

---

## 📋 Prerequisites

Before you start, make sure you have:

- ✅ Digital Ocean account
- ✅ A droplet created (Ubuntu 22.04 recommended)
- ✅ Domain name pointed to your droplet's IP address
- ✅ SSH access to your droplet
- ✅ Docker and Docker Compose installed on your droplet

---

## 🎯 Overview

We'll deploy your portfolio using:
- **Docker** - Containerization
- **Flask + Gunicorn** - Application server
- **Nginx** - Reverse proxy & SSL
- **Let's Encrypt** - Free SSL certificates

---

## 📦 Step 1: Prepare Your Local Files

### **Files Created:**

1. ✅ `Dockerfile` - Container configuration
2. ✅ `docker-compose.yml` - Multi-container orchestration
3. ✅ `nginx.conf` - Nginx reverse proxy config
4. ✅ `.dockerignore` - Exclude unnecessary files
5. ✅ `requirements.txt` - Python dependencies
6. ✅ `.env.example` - Environment variables template

### **Create Your .env File:**

```bash
cp .env.example .env
nano .env
```

Update with your actual values:
```
SECRET_KEY=generate-a-random-secret-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**Generate a secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🌐 Step 2: Set Up Digital Ocean Droplet

### **A. Create Droplet**

1. Log into Digital Ocean
2. Click "Create" → "Droplets"
3. Choose:
   - **Image:** Ubuntu 22.04 LTS
   - **Plan:** Basic ($6/month or higher)
   - **CPU:** Regular Intel (1GB+ RAM recommended)
   - **Datacenter:** Closest to your target audience
   - **Authentication:** SSH key (recommended) or password
4. Click "Create Droplet"
5. Note your droplet's IP address

### **B. Point Your Domain**

In your domain registrar (GoDaddy, Namecheap, etc.):

Add these DNS records:
```
Type: A
Name: @
Value: YOUR_DROPLET_IP
TTL: 3600

Type: A
Name: www
Value: YOUR_DROPLET_IP
TTL: 3600
```

Wait 15-60 minutes for DNS propagation.

---

## 🔧 Step 3: Set Up Droplet

### **SSH into your droplet:**

```bash
ssh root@YOUR_DROPLET_IP
```

### **Update system:**

```bash
apt update && apt upgrade -y
```

### **Install Docker:**

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Start Docker
systemctl start docker
systemctl enable docker

# Verify
docker --version
```

### **Install Docker Compose:**

```bash
# Download Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose --version
```

### **Install Git (if not installed):**

```bash
apt install git -y
```

---

## 📤 Step 4: Upload Your Code

### **Option A: Using Git (Recommended)**

1. **On your local machine:**

```bash
# Initialize git (if not already)
cd /path/to/your/portfolio
git init

# Create .gitignore
cat > .gitignore << EOF
__pycache__/
*.pyc
.env
*.log
.DS_Store
venv/
env/
EOF

# Commit your code
git add .
git commit -m "Initial commit"

# Push to GitHub (create repo first on github.com)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

2. **On your droplet:**

```bash
# Clone your repository
cd /opt
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git portfolio
cd portfolio
```

### **Option B: Using SCP (Direct Upload)**

On your local machine:

```bash
# Create a tarball
cd /path/to/your/portfolio
tar -czf portfolio.tar.gz .

# Upload to droplet
scp portfolio.tar.gz root@YOUR_DROPLET_IP:/opt/

# SSH into droplet
ssh root@YOUR_DROPLET_IP

# Extract
cd /opt
mkdir portfolio
tar -xzf portfolio.tar.gz -C portfolio
cd portfolio
```

---

## 🔐 Step 5: Configure Environment

### **On your droplet:**

```bash
cd /opt/portfolio

# Create .env file
nano .env
```

Add your configuration:
```
SECRET_KEY=your-generated-secret-key
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### **Update nginx.conf with your domain:**

```bash
nano nginx.conf
```

Replace `your-domain.com` with your actual domain in ALL locations:
- Line 14: `server_name your-domain.com www.your-domain.com;`
- Line 25: `server_name your-domain.com www.your-domain.com;`
- Line 28-29: SSL certificate paths

---

## 🏗️ Step 6: Build and Deploy

### **A. Build Docker Image:**

```bash
cd /opt/portfolio
docker-compose build
```

### **B. Start Without SSL (First Time):**

For initial setup, we'll start without SSL to get Let's Encrypt certificate:

```bash
# Comment out SSL lines in nginx.conf temporarily
nano nginx.conf
# Comment out lines 28-29 and the entire server block for 443

# Start containers
docker-compose up -d web

# Test the app
curl http://localhost:5000
```

### **C. Get SSL Certificate:**

```bash
# Install Certbot
apt install certbot -y

# Stop nginx temporarily
docker-compose stop nginx

# Get certificate
certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Certificates will be in: /etc/letsencrypt/live/your-domain.com/
```

### **D. Update nginx.conf and Start Everything:**

```bash
# Uncomment SSL lines in nginx.conf
nano nginx.conf

# Create certbot directories
mkdir -p certbot/conf certbot/www

# Copy certificates
cp -r /etc/letsencrypt/* certbot/conf/

# Start all services
docker-compose up -d
```

---

## ✅ Step 7: Verify Deployment

### **Check if containers are running:**

```bash
docker-compose ps
```

You should see:
```
NAME                STATUS              PORTS
portfolio-web       Up About a minute   0.0.0.0:5000->5000/tcp
portfolio-nginx     Up About a minute   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```

### **Check logs:**

```bash
# Check Flask app logs
docker-compose logs web

# Check Nginx logs
docker-compose logs nginx

# Follow logs in real-time
docker-compose logs -f
```

### **Test your website:**

1. Visit: `http://your-domain.com` (should redirect to HTTPS)
2. Visit: `https://your-domain.com` (should work with SSL)
3. Test all pages:
   - Homepage
   - About
   - Projects
   - Resume Bot
   - Contact

---

## 🔄 Step 8: Set Up Auto-Renewal (SSL)

### **Create renewal script:**

```bash
nano /opt/renew-ssl.sh
```

Add:
```bash
#!/bin/bash
docker-compose -f /opt/portfolio/docker-compose.yml stop nginx
certbot renew --quiet
cp -r /etc/letsencrypt/* /opt/portfolio/certbot/conf/
docker-compose -f /opt/portfolio/docker-compose.yml start nginx
```

Make executable:
```bash
chmod +x /opt/renew-ssl.sh
```

### **Add to crontab:**

```bash
crontab -e
```

Add this line:
```
0 3 * * 1 /opt/renew-ssl.sh >> /var/log/ssl-renew.log 2>&1
```

This will renew SSL every Monday at 3 AM.

---

## 🔄 Updating Your Site

### **When you make changes:**

```bash
# SSH into droplet
ssh root@YOUR_DROPLET_IP

# Navigate to project
cd /opt/portfolio

# Pull latest changes (if using Git)
git pull

# Or upload new files with SCP

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d

# Check logs
docker-compose logs -f
```

---

## 📊 Monitoring

### **Check container status:**

```bash
docker-compose ps
```

### **View logs:**

```bash
# All logs
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs nginx

# Follow logs
docker-compose logs -f web
```

### **Resource usage:**

```bash
docker stats
```

### **Restart services:**

```bash
# Restart everything
docker-compose restart

# Restart specific service
docker-compose restart web
docker-compose restart nginx
```

---

## 🛡️ Security Best Practices

### **1. Set up firewall:**

```bash
# Install UFW
apt install ufw -y

# Allow SSH
ufw allow 22/tcp

# Allow HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
ufw enable

# Check status
ufw status
```

### **2. Create non-root user:**

```bash
# Create user
adduser deploy
usermod -aG sudo deploy
usermod -aG docker deploy

# Switch to deploy user
su - deploy
```

### **3. Disable root SSH:**

```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Change this line:
PermitRootLogin no

# Restart SSH
sudo systemctl restart sshd
```

### **4. Set up automatic security updates:**

```bash
apt install unattended-upgrades -y
dpkg-reconfigure --priority=low unattended-upgrades
```

---

## 🐛 Troubleshooting

### **Website not loading:**

```bash
# Check if containers are running
docker-compose ps

# Check logs
docker-compose logs web
docker-compose logs nginx

# Restart containers
docker-compose restart
```

### **SSL certificate error:**

```bash
# Check certificate
ls -la /etc/letsencrypt/live/your-domain.com/

# Verify nginx config
docker-compose exec nginx nginx -t

# Check certbot logs
cat /var/log/letsencrypt/letsencrypt.log
```

### **Port already in use:**

```bash
# Check what's using port 80/443
sudo lsof -i :80
sudo lsof -i :443

# Kill the process
sudo kill -9 PID
```

### **Container keeps restarting:**

```bash
# Check logs
docker-compose logs web

# Check if app.py has errors
docker-compose exec web python -c "import app; print('OK')"
```

---

## 📈 Performance Optimization

### **1. Adjust Gunicorn workers:**

In `Dockerfile`, change workers based on CPU:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
```

**Formula:** `(2 x CPU_CORES) + 1`

### **2. Enable caching:**

Add to nginx.conf:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
proxy_cache my_cache;
```

### **3. Monitor resources:**

```bash
# Watch resource usage
docker stats

# Check droplet resources
htop
```

---

## 💰 Cost Estimation

**Digital Ocean Droplet:**
- Basic ($6/month): 1GB RAM, 25GB SSD - Good for starting
- Standard ($12/month): 2GB RAM, 50GB SSD - Recommended
- Performance ($18/month): 2GB RAM, 60GB SSD - For high traffic

**Domain:** $10-15/year (varies by provider)

**SSL Certificate:** FREE (Let's Encrypt)

**Total:** ~$6-18/month + domain

---

## 🎯 Quick Reference Commands

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose down
docker-compose build
docker-compose up -d

# Check status
docker-compose ps

# SSH into container
docker-compose exec web /bin/bash

# Update code (if using Git)
git pull
docker-compose restart
```

---

## ✅ Deployment Checklist

- [ ] Droplet created on Digital Ocean
- [ ] Domain DNS pointed to droplet IP
- [ ] Docker & Docker Compose installed
- [ ] Code uploaded to droplet
- [ ] .env file created with correct values
- [ ] nginx.conf updated with your domain
- [ ] SSL certificate obtained
- [ ] Docker containers built and running
- [ ] Website accessible via HTTPS
- [ ] All pages working correctly
- [ ] SSL auto-renewal configured
- [ ] Firewall configured
- [ ] Monitoring set up

---

## 🚀 You're Live!

Your portfolio is now deployed and accessible at:
- `https://your-domain.com`
- `https://www.your-domain.com`

**Congratulations! 🎉**

---

## 📞 Need Help?

Common issues:
1. DNS not propagating → Wait 24 hours
2. SSL error → Check certificate paths in nginx.conf
3. Container not starting → Check `docker-compose logs`
4. 502 Bad Gateway → Check if Flask app is running

For Digital Ocean specific issues:
- https://docs.digitalocean.com/
- https://www.digitalocean.com/community/

---

## 📝 Next Steps

1. Set up monitoring (UptimeRobot, etc.)
2. Configure backups
3. Add Google Analytics
4. Set up email alerts
5. Configure CDN (optional)

**Your portfolio is production-ready! 🚀**
