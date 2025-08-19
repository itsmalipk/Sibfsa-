# Sibfsa (Django) — Premium full‑stack 

Python-only full-stack ecommerce for Sibfsa. Django 5, session cart, COD checkout, reviews with moderation, admin CMS, premium theme, dark/light toggle via cookie. 7-section homepage.

## Quick start (VS Code, Windows PowerShell)
```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_sibfsa
python manage.py runserver
