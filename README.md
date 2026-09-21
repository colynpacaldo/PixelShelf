# Vertical Slicing Django Project (CSIT327)

A Django project organized by feature (vertical slicing) instead of by
technical layer, with optional Supabase PostgreSQL integration. Built to
match the CSIT327 "Django Vertical Slicing + Supabase" guide.

## Features (each is its own Django app)

| Feature | App | What it owns |
|---|---|---|
| Login | `apps/login` | Authenticate an existing user, logout |
| Register | `apps/register` | Create a new user account |
| Home | `apps/home` | Main authenticated dashboard |
| Profile | `apps/profile` | Profile model, view/edit profile |
| Settings | `apps/user_settings` | Preferences model, view/edit settings |

Each feature owns its own `templates/<feature>/`, and
`static/css|js|images/<feature>/` folders, plus its own `urls.py`,
`views.py`, and (where relevant) `models.py`.

## Setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt

copy .env.example .env    # Windows
# cp .env.example .env    # macOS/Linux
```

Edit `.env`:
- Leave `DATABASE_URL` unset to run on local SQLite immediately.
- To use Supabase, paste the exact PostgreSQL connection string from
  Supabase Dashboard -> Connect (Session Pooler recommended for
  classroom/IPv4-only networks) into `DATABASE_URL`.

Then:

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit:
- `/register/` to create an account
- `/login/` to log in
- `/` (Home) after logging in
- `/profile/` to view/edit your profile
- `/settings/` to view/edit your preferences
- `/admin/` for the Django admin

## Notes

- `DATABASES` automatically falls back to SQLite if `DATABASE_URL` is not
  set, so the project runs immediately without Supabase for local
  development. Set `DATABASE_URL` to point Django at Supabase PostgreSQL.
- Never commit `.env` — it's already in `.gitignore`.
- Profile images are stored under `media/profile/` (served by Django only
  while `DEBUG=True`).
# PixelShelf

**A 2D game asset catalog and web-based sprite previewer for creators.**

PixelShelf is a dedicated web platform for indie game developers and pixel artists to organize, tag, and preview 2D game assets. Whether you are assembling tilesets for a museum-themed 2D platformer or keeping track of complex character animations, PixelShelf centralizes your collections with clear metadata so project files stay organized. 

Users can upload spritesheets, document their grid dimensions, and run a simple in-browser animation preview before importing files into a game engine.

## The Problem

Student game developers and 2D artists often lose track of sprite files across scattered local folders. Furthermore, they lack a quick way to test animation loops without booting up heavy game engines. Standard art portfolio websites display only static images, making it difficult to verify how a spritesheet moves in motion. PixelShelf provides a lightweight web organizer with an integrated animation viewer built specifically for 2D sprites.

## Features

* **Asset Manager & Uploader:** Upload 2D image files (PNG/GIF) up to 10MB. Tag your assets with metadata such as frame size, author, category (characters, tilesets, UI), and license type.
* **Interactive Sprite Animator:** A custom HTML5 Canvas widget where users can enter frame width/height to view a looping animation preview with play/pause controls.
* **Background Contrast Tester:** Switch the canvas backdrop between light, dark, and transparent checkerboards to test sprite edge clarity and readability.
* **Dashboard & Collections:** View recent uploads, total asset counts, and organize private asset libraries and project collections.
* **User Profiles:** Showcase a portfolio of public assets and quick stats on uploaded spritesheets.
* **Secure Authentication:** Full register, login, and logout functionality to keep private assets secure.

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite 
* **Frontend:** HTML, CSS, JavaScript (HTML5 Canvas API for the Sprite Animator)

## Project Limitations

To keep the application lightweight and focused on its core objective, PixelShelf adheres to the following constraints:
* **No Built-in Drawing Editor:** The app is purely for organizing and previewing assets; users cannot draw or edit pixel art within the browser.
* **2D Raster Files Only:** Support is restricted to standard PNG and GIF formats. 3D models and audio files are not supported.
* **No Engine Auto-Export:** The system does not generate engine-specific scripts (e.g., Unity ScriptableObjects or Godot scene files). It provides direct file downloads.
* **File Upload Size Limit:** Individual asset uploads are capped at a maximum of 10MB to maintain efficient server storage.
