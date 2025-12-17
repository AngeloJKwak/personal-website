# 🚀 Quick Start - Deploy to Digital Ocean

## Fastest way to get your portfolio live!

---

## ⚡ Prerequisites

1. **Digital Ocean Account** - Sign up at digitalocean.com
2. **Domain Name** - Point to your droplet's IP
3. **5 minutes** - That's all you need!

---

## 📦 What You Have

All files are ready:
- ✅ `Dockerfile` - Container setup
- ✅ `docker-compose.yml` - Services orchestration
- ✅ `nginx.conf` - Web server config
- ✅ `requirements.txt` - Python dependencies
- ✅ `deploy.sh` - Automated deployment script
- ✅ `.env.example` - Configuration template

---

## 🎯 3-Step Deployment

### **Step 1: Create Droplet**

1. Go to [Digital Ocean](https://digitalocean.com)
2. Click "Create" → "Droplets"
3. Choose:
   - Ubuntu 22.04 LTS
   - $6/month plan (or higher)
   - Add SSH key
4. Click "Create"
5. **Copy your droplet's IP address**

### **Step 2: Point Your Domain**

In your domain registrar (GoDaddy, Namecheap, etc.):

**Add A Records:**
```
Type: A
Name: @
Value: YOUR_DROPLET_IP

Type: A  
Name: www
Value: YOUR_DROPLET_IP
```

Wait 15-30 minutes for DNS to propagate.

### **Step 3: Deploy**

**On your local machine:**

```bash
# Create .env file
cp .env.example .env
nano .env  # Add your secret key and email settings

# Upload to droplet
scp -r . root@YOUR_DROPLET_IP:/opt/portfolio
```

**On your droplet (SSH in):**

```bash
ssh root@YOUR_DROPLET_IP

cd /opt/portfolio

# Make deploy script executable
chmod +x deploy.sh

# Run deployment
sudo ./deploy.sh
```

The script will:
- Install Docker & Docker Compose
- Install Certbot for SSL
- Build your application
- Get SSL certificate
- Start all services

**That's it!** 🎉

Visit `https://your-domain.com`

---

## 📋 Manual Steps (Alternative)

If you prefer to do it manually:

### **1. SSH into droplet:**
```bash
ssh root@YOUR_DROPLET_IP
```

### **2. Install Docker:**
```bash
curl -fsSL https://get.docker.com | sh
```

### **3. Install Docker Compose:**
```bash
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### **4. Upload your code:**
```bash
# From your local machine
scp -r . root@YOUR_DROPLET_IP:/opt/portfolio
```

### **5. Deploy:**
```bash
cd /opt/portfolio
docker-compose build
docker-compose up -d
```

---

## 🔐 Get SSL Certificate

```bash
# Install Certbot
apt install certbot -y

# Get certificate
certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Copy certificates
mkdir -p certbot/conf
cp -r /etc/letsencrypt/* certbot/conf/

# Restart services
docker-compose restart
```

---

## ✅ Verify Everything Works

### **Check containers:**
```bash
docker-compose ps
```

Should show:
```
portfolio-web     Up
portfolio-nginx   Up
```

### **Check logs:**
```bash
docker-compose logs -f
```

### **Test your site:**
- Visit `https://your-domain.com`
- Test all pages (Home, About, Projects, Resume Bot, Contact)

---

## 🔄 Update Your Site

```bash
# SSH into droplet
ssh root@YOUR_DROPLET_IP

cd /opt/portfolio

# Upload new files or pull from git
git pull  # if using git

# Restart
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 🛠️ Useful Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop everything
docker-compose down

# Start everything
docker-compose up -d

# Check container status
docker-compose ps

# View resource usage
docker stats
```

---

## 🐛 Troubleshooting

### **Site not loading:**
```bash
# Check if containers are running
docker-compose ps

# Check logs
docker-compose logs web
docker-compose logs nginx
```

### **SSL error:**
```bash
# Verify certificate exists
ls -la /etc/letsencrypt/live/your-domain.com/

# Check nginx config
docker-compose exec nginx nginx -t
```

### **Port already in use:**
```bash
# See what's using port 80
sudo lsof -i :80

# Kill it
sudo kill -9 PID
```

---

## 💰 Costs

- **Droplet:** $6-12/month
- **Domain:** $10-15/year
- **SSL:** FREE (Let's Encrypt)

**Total:** ~$6-12/month

---

## 🎉 You're Done!

Your portfolio is now live at `https://your-domain.com`

**Key Features:**
✅ Containerized with Docker
✅ SSL/HTTPS enabled
✅ Production-ready
✅ Auto-scaling with Gunicorn
✅ Nginx reverse proxy
✅ SSL auto-renewal

---

## 📚 Full Documentation

For detailed information, see `DEPLOYMENT_GUIDE.md`

**Congratulations on deploying your portfolio! 🚀**
