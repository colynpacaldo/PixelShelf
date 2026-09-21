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
