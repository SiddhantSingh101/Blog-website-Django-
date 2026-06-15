# Blog-website-Django-
Blog website using django.

## EC2 deployment

These instructions assume Ubuntu 24.04 on EC2, a domain pointed at the instance, and the project deployed to `/srv/storefront`.

### 1. Prepare the instance

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip nginx git
sudo mkdir -p /srv/storefront
sudo chown ubuntu:www-data /srv/storefront
```

Clone or copy this repository into `/srv/storefront`, then create a virtual environment:

```bash
cd /srv/storefront
python3.12 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt
```

### 2. Configure production environment

```bash
cp .env.example .env
./venv/bin/python - <<'PY'
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
PY
```

Edit `.env`:

```bash
nano .env
```

Set:

- `DJANGO_SECRET_KEY` to the generated secret.
- `DJANGO_ALLOWED_HOSTS` to your domain and/or EC2 public IP.
- `DJANGO_CSRF_TRUSTED_ORIGINS` to your `https://` domain.
- Email settings only if you want real activation emails.

If you also run the analytics collector, create `/srv/storefront/.env.collector` with the same Django production settings plus `COLLECTOR_ALLOWED_ORIGINS`.

### 3. Initialize Django

For one-off commands, load the environment first:

```bash
cd /srv/storefront
set -a
. ./.env
set +a
```

Then run:

```bash
./venv/bin/python manage.py migrate
./venv/bin/python manage.py collectstatic --noinput
./venv/bin/python manage.py check --deploy
```

Create an admin user if needed:

```bash
./venv/bin/python manage.py createsuperuser
```

For the optional collector:

```bash
set -a
. ./.env.collector
set +a
DJANGO_SETTINGS_MODULE=collector_config.settings ./venv/bin/python manage.py migrate
DJANGO_SETTINGS_MODULE=collector_config.settings ./venv/bin/python manage.py collectstatic --noinput
DJANGO_SETTINGS_MODULE=collector_config.settings ./venv/bin/python manage.py check --deploy
```

### 4. Install Gunicorn as a service

```bash
sudo cp deploy/gunicorn-storefront.service /etc/systemd/system/gunicorn-storefront.service
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-storefront
sudo systemctl status gunicorn-storefront
```

For the optional collector:

```bash
sudo cp deploy/gunicorn-collector.service /etc/systemd/system/gunicorn-collector.service
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-collector
sudo systemctl status gunicorn-collector
```

### 5. Configure Nginx

Edit `deploy/nginx-storefront.conf` and replace `example.com www.example.com` with your domain or public IP.

```bash
sudo cp deploy/nginx-storefront.conf /etc/nginx/sites-available/storefront
sudo ln -s /etc/nginx/sites-available/storefront /etc/nginx/sites-enabled/storefront
sudo nginx -t
sudo systemctl reload nginx
```

For the optional collector, edit `deploy/nginx-collector.conf`, copy it to sites-available, symlink it, test Nginx, and reload.

### 6. Add HTTPS

After DNS points to EC2:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```

Then update `.env` so the production security settings stay enabled:

```bash
DJANGO_SECURE_SSL_REDIRECT=true
DJANGO_SESSION_COOKIE_SECURE=true
DJANGO_CSRF_COOKIE_SECURE=true
```

Restart after environment changes:

```bash
sudo systemctl restart gunicorn-storefront
```

### Useful checks

```bash
sudo journalctl -u gunicorn-storefront -f
sudo tail -f /var/log/nginx/error.log
curl -I http://127.0.0.1
```
