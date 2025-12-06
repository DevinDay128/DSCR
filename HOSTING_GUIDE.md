# Hosting Guide - AI Rent & DSCR Calculator

This guide shows you how to run and host the AI Rent & DSCR Calculator web interface.

## Quick Start (Run Locally)

### Option 1: Flask Web App (Recommended for Production)

1. **Install Dependencies**
   ```bash
   pip install flask
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open in Browser**
   - Navigate to: `http://localhost:5000`
   - You'll see a beautiful web interface to calculate DSCR!

### Option 2: Streamlit App (Easiest for Demos)

1. **Install Dependencies**
   ```bash
   pip install streamlit
   ```

2. **Run the Application**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open in Browser**
   - Streamlit will automatically open your browser
   - Usually at: `http://localhost:8501`

## Screenshots & Features

### Flask App Features:
- 🎨 Beautiful gradient design
- 📱 Fully responsive (works on mobile)
- 📊 Interactive form with real-time validation
- 📈 Visual results with color-coded risk badges
- 💾 All results displayed in an easy-to-read format

### Streamlit App Features:
- ⚡ Instant setup, no HTML/CSS needed
- 📥 Download results as JSON
- 🔄 Tabbed interface (Input/Results)
- 🎯 Simple and clean design

## Production Hosting Options

### 1. Deploy Flask App to Heroku

**Step 1:** Create a `Procfile`
```bash
echo "web: gunicorn app:app" > Procfile
```

**Step 2:** Install Gunicorn
```bash
pip install gunicorn
pip freeze > requirements.txt
```

**Step 3:** Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-dscr-calculator

# Deploy
git push heroku main

# Open in browser
heroku open
```

### 2. Deploy Streamlit App to Streamlit Cloud (FREE!)

**Step 1:** Push your code to GitHub (already done!)

**Step 2:** Go to [share.streamlit.io](https://share.streamlit.io)

**Step 3:** Connect your GitHub repository

**Step 4:** Select `streamlit_app.py` as the main file

**Step 5:** Click Deploy!

Your app will be live at: `https://your-username-dscr-calculator.streamlit.app`

### 3. Deploy Flask App to AWS EC2

**Step 1:** Launch an EC2 instance (Ubuntu)

**Step 2:** SSH into your instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

**Step 3:** Install dependencies
```bash
sudo apt update
sudo apt install python3-pip nginx
pip3 install flask gunicorn
```

**Step 4:** Clone your repository
```bash
git clone https://github.com/your-username/DSCR.git
cd DSCR
```

**Step 5:** Run with Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

**Step 6:** Configure Nginx (optional, for production)
```bash
sudo nano /etc/nginx/sites-available/dscr
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Step 7:** Enable and restart Nginx
```bash
sudo ln -s /etc/nginx/sites-available/dscr /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 4. Deploy to Google Cloud Run (Flask)

**Step 1:** Create a `Dockerfile`
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir flask gunicorn

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

**Step 2:** Build and deploy
```bash
gcloud builds submit --tag gcr.io/your-project/dscr-calculator
gcloud run deploy --image gcr.io/your-project/dscr-calculator --platform managed
```

### 5. Deploy to Vercel (Serverless)

**Step 1:** Install Vercel CLI
```bash
npm i -g vercel
```

**Step 2:** Create `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**Step 3:** Deploy
```bash
vercel --prod
```

## Running Behind a Reverse Proxy

If you're running on a server with other applications:

### Nginx Configuration
```nginx
location /dscr/ {
    proxy_pass http://127.0.0.1:5000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### Apache Configuration
```apache
ProxyPass /dscr http://localhost:5000/
ProxyPassReverse /dscr http://localhost:5000/
```

## Environment Variables

For production, set these environment variables:

### Flask App
```bash
export FLASK_ENV=production
export SECRET_KEY="your-secret-key-here"
```

### Security Considerations

1. **HTTPS**: Always use HTTPS in production
   - Use Let's Encrypt for free SSL certificates
   - `sudo certbot --nginx -d yourdomain.com`

2. **Rate Limiting**: Prevent abuse
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   ```

3. **CORS**: If building an API
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

4. **Input Validation**: Already built-in, but verify on backend

## Performance Tips

### Flask App Optimization
```bash
# Use multiple workers
gunicorn --workers 4 --threads 2 app:app

# Enable async
pip install gevent
gunicorn --worker-class gevent --workers 4 app:app
```

### Caching (Optional)
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

## Monitoring & Logging

### Basic Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Advanced Monitoring
- Use **Sentry** for error tracking
- Use **New Relic** or **DataDog** for performance monitoring
- Use **Google Analytics** for user tracking

## API Access

The Flask app also provides a JSON API endpoint:

```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Main St, Austin, TX",
    "purchase_price": 400000,
    "down_payment_percent": 0.25,
    "interest_rate_annual": 0.07,
    "term_years": 30
  }'
```

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
python app.py --port 5001
```

### Permission Denied
```bash
# Don't use port 80 directly, use 5000 and proxy with Nginx
# Or use sudo (not recommended)
sudo python app.py
```

### Module Not Found
```bash
# Install all dependencies
pip install -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Static Files Not Loading
- Check that `/static/style.css` exists
- Verify Flask is serving static files correctly
- Check browser console for 404 errors

## Development vs Production

### Development (Current Setup)
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Production (Recommended)
```python
# Don't use debug=True in production!
# Use gunicorn or similar WSGI server
gunicorn --bind 0.0.0.0:5000 app:app
```

## Customization

### Change Colors/Styling
Edit `static/style.css`:
```css
/* Change primary color from purple to blue */
background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
```

### Add Logo
Add to `templates/index.html`:
```html
<header>
    <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo">
    <h1>🏠 AI Rent & DSCR Calculator</h1>
</header>
```

### Modify Calculations
Edit `ai_rent_dscr.py` to adjust:
- Rent estimation multipliers
- Operating expense defaults
- Risk thresholds
- Insurance estimates

## Support & Resources

- **Documentation**: See `README.md`
- **Examples**: Run `python examples.py`
- **Tests**: Run `python test_calculations.py`
- **Issues**: Create a GitHub issue

## Next Steps

1. ✅ Run locally with Flask or Streamlit
2. 🌐 Deploy to cloud platform of choice
3. 🔒 Add authentication if needed
4. 📊 Add analytics tracking
5. 🎨 Customize branding
6. 📱 Share with users!

---

**Need Help?** The easiest way to get started:
```bash
pip install streamlit
streamlit run streamlit_app.py
```

Your calculator will be live in seconds! 🚀
