# Render Deployment Guide for Sri Lakshmi Textile Shop (LoomLuxe)

This project is fully configured for deployment on [Render](https://render.com/).

---

## 🛠️ Files Configured for Render

1. **`requirements.txt`**: Added `dj-database-url==2.2.0`, `gunicorn==22.0.0`, `whitenoise==6.7.0`, `psycopg2-binary==2.9.9`.
2. **`config/settings.py`**:
   - `dj-database-url` parses `DATABASE_URL` automatically provided by Render PostgreSQL.
   - Dynamic `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` configured using `RENDER_EXTERNAL_HOSTNAME`.
   - WhiteNoise static file handling with non-strict manifest to prevent build errors.
   - Fallback to SQLite3 if no PostgreSQL database is linked.
3. **`config/urls.py`**: Media files serving enabled in production for uploaded media assets.
4. **`Procfile`**: Specifies Gunicorn WSGI server startup command:
   ```text
   web: gunicorn config.wsgi:application
   ```
5. **`build.sh`**: Automatic build script executing pip install, static collection, and database migrations:
   ```bash
   #!/usr/bin/env bash
   set -o errexit
   pip install --upgrade pip
   pip install -r requirements.txt
   python manage.py collectstatic --no-input
   python manage.py migrate
   ```
6. **`render.yaml`**: Complete Render Blueprint configuration defining both the Python Web Service and PostgreSQL Database.
7. **`runtime.txt`**: Specifies `python-3.12.8`.

---

## 🚀 How to Deploy on Render

### Option 1: Automatic 1-Click Deployment (Render Blueprint - Recommended)

1. **Push Code to GitHub / GitLab**:
   ```bash
   git add .
   git commit -m "Configure project for Render deployment"
   git push origin main
   ```

2. **Deploy via Render Dashboard**:
   - Log into [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** -> **Blueprint**.
   - Connect your GitHub repository (`Sri-Lakshmi-textile-shop`).
   - Render will read `render.yaml` and automatically set up:
     - Web Service (`Sri-Lakshmi-textile-shop`)
     - PostgreSQL Database (`sri-lakshmi-db`)
     - Linked `DATABASE_URL`
     - Auto-generated `SECRET_KEY`
   - Click **Apply**. Render will run `./build.sh` and launch Gunicorn.

---

### Option 2: Manual Web Service Setup on Render

If you prefer creating services manually:

1. **Create PostgreSQL Database**:
   - Go to **New +** -> **PostgreSQL**.
   - Name: `sri-lakshmi-db`
   - Database Name: `sri_lakshmi_db`
   - Click **Create Database**.
   - Copy the **Internal Database URL**.

2. **Create Web Service**:
   - Go to **New +** -> **Web Service**.
   - Connect your repository.
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`

3. **Set Environment Variables**:
   In your Web Service **Environment** tab, add:
   - `PYTHON_VERSION` = `3.12.8`
   - `DEBUG` = `False`
   - `SECRET_KEY` = *(a secure random string)*
   - `ALLOWED_HOSTS` = `*`
   - `CSRF_TRUSTED_ORIGINS` = `https://*.onrender.com`
   - `DATABASE_URL` = *(Internal Database URL copied from step 1)*
   - *(Optional)* `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, etc.

4. Click **Deploy Web Service**.
