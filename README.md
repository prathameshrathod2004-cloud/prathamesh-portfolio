# Prathamesh Rathod — Video Editor Portfolio Website

A professional, animated portfolio website built with **Python (Flask)** on the backend
and **SQL (SQLite)** as the database. Frontend uses HTML, CSS and JavaScript with
smooth scroll animations.

## What's inside
- **Home page** — hero intro with your photo, about section, services
- **Portfolio page** — all your services + link to your Instagram reels
- **Contact page** — contact form (saved to the SQL database) + WhatsApp/phone/Instagram
- **Admin Dashboard** (`/admin`) — password-protected panel to add/remove services and view contact messages, backed by the SQL database

## How to run it in VS Code

1. **Install Python** if you don't have it: https://www.python.org/downloads/
   (while installing, tick "Add Python to PATH")

2. **Open the folder in VS Code**
   - Extract/copy this whole `portfolio` folder anywhere on your PC
   - Open VS Code → File → Open Folder → select the `portfolio` folder

3. **Open a terminal in VS Code**
   - Menu: Terminal → New Terminal

4. **Install Flask** (only needed once):
   ```
   pip install flask
   ```

5. **Run the website**:
   ```
   python app.py
   ```

6. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

7. **Admin Dashboard**: go to `http://127.0.0.1:5000/admin`
   - Default password: `pratya123`
   - **Change this password** — open `app.py`, find the line:
     ```python
     ADMIN_PASSWORD = "pratya123"
     ```
     and replace it with your own password.

## Folder structure
```
portfolio/
├── app.py                 → Python/Flask backend + SQL database logic
├── portfolio.db            → auto-created SQLite database (on first run)
├── templates/               → HTML pages (Jinja2 templates)
│   ├── base.html
│   ├── index.html
│   ├── portfolio.html
│   ├── contact.html
│   ├── admin_login.html
│   └── admin.html
├── static/
│   ├── css/style.css        → all styling & animations
│   ├── js/script.js         → animations & interactions
│   └── images/prathamesh.jpeg
└── README.md
```

## Notes
- Your photo is already added at `static/images/prathamesh.jpeg` — to change it, just
  replace that file with a new photo (keep the same filename), or update the filename in
  `templates/index.html`.
- WhatsApp number and Instagram link are already wired in (edit `templates/base.html`
  and `templates/contact.html` if you ever need to change them).
- To put this live on the internet (not just your PC), you'll need a hosting service
  like PythonAnywhere, Render, or Railway — happy to walk you through that whenever you're ready.
