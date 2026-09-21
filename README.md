# AI Image Generator

A complete, high-performance, professional AI Image Generator web application built strictly with **Python**, **Django**, **PostgreSQL**, **HTML5**, and **CSS3**, designed around a **Zero-JavaScript Policy** and traditional server-side rendering architecture.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Environment Variables Guide (.env)](#environment-variables-guide-env)
   - [Overview of All Variables](#overview-of-all-variables)
   - [Where and How to Get Each Value](#where-and-how-to-get-each-value)
5. [Step-by-Step Installation & Run Guide](#step-by-step-installation--run-guide)
   - [Prerequisites](#prerequisites)
   - [1. Clone or Navigate to Project](#1-clone-or-navigate-to-project)
   - [2. Set Up a Virtual Environment](#2-set-up-a-virtual-environment)
   - [3. Install Dependencies](#3-install-dependencies)
   - [4. Create and Configure `.env`](#4-create-and-configure-env)
   - [5. Run Database Migrations](#5-run-database-migrations)
   - [6. Start the Development Server](#6-start-the-development-server)
   - [7. Open in Your Browser](#7-open-in-your-browser)
6. [Application Routes & Features](#application-routes--features)
7. [Testing & Quality Assurance](#testing--quality-assurance)
8. [Project Structure](#project-structure)
9. [Troubleshooting & FAQs](#troubleshooting--faqs)
10. [License](#license)

---

## Overview

The **AI Image Generator** provides an intuitive, high-performance platform where users enter descriptive text prompts, choose aesthetic styles (*Realistic*, *Cinematic*, *Anime*, *Digital Art*, *Fantasy*, *3D Render*), and select aspect ratios (*1:1*, *16:9*, *4:3*, *3:4*, *9:16*).

The Django backend securely integrates with external AI image diffusion models (Google GenAI Imagen 3 and Pollinations AI), stores generations persistently in PostgreSQL (with automatic zero-config SQLite fallback), and serves dynamic result pages using pure server-side HTML and CSS.

---

## Key Features

- **Text-to-Image Diffusion**: Generates detailed, high-resolution visuals from plain-text descriptions.
- **Curated Artistic Styles**:
  - *Realistic* (Photorealistic, 8k resolution, 35mm lens)
  - *Cinematic* (Anamorphic movie stills, dramatic lighting)
  - *Anime* (Studio anime key visuals, vibrant color grading)
  - *Digital Art* (Concept art, dynamic lighting, ArtStation aesthetic)
  - *Fantasy* (Intricate magical landscapes, mystical atmosphere)
  - *3D Render* (Octane render, Unreal Engine 5 ray-tracing)
- **5 Aspect Ratios**: Square (1:1), Landscape (16:9), Standard (4:3), Portrait (3:4), and Vertical Story (9:16).
- **Persistent History & Gallery (`/history/`)**: View previous generations in an interactive, responsive grid with timestamp and metadata tags.
- **Detail View (`/generation/<id>/`)**: Inspect full prompt text, high-resolution image, style parameters, and creation time.
- **Direct Attachment Downloads (`/generation/<id>/download/`)**: Pure server-side streaming downloads without requiring JavaScript.
- **Safe Record Deletion (`/generation/<id>/delete/`)**: Dedicated deletion view with confirmation and CSRF verification.
- **Zero-JavaScript Policy**: 100% accessible HTML5 + CSS3. No front-end JavaScript frameworks, scripts, or client-side dependencies.
- **Dark Mode Design System**: Built with CSS variables (`#0B0D12` background, `#141720` surface, `#7C5CFC` primary accent, and `#F5F7FA` typography).

---

## Architecture

```
                  TIER 1: FRONTEND
        ┌──────────────────────────────────┐
        │  HTML5 + CSS3 (Zero JavaScript)  │
        │  Django Templates & Forms        │
        │                                  │
        │  • Prompt Generation Form        │
        │  • Result Presentation View      │
        │  • Gallery & History Cards       │
        │  • Generation Details & Download │
        └────────────────┬─────────────────┘
                         │
                    HTTP POST/GET
                         │
                         ▼
                  TIER 2: BACKEND
        ┌──────────────────────────────────┐
        │  Python 3 + Django Core          │
        │                                  │
        │  • Form Validation & Sanitization│
        │  • Image Service Orchestrator    │
        │  • Django ORM Models             │
        │  • File Attachment Streaming     │
        └────────────┬────────────┬────────┘
                     │            │
                     ▼            ▼
             Database Engine    External AI Services
          PostgreSQL / SQLite   (Google GenAI Imagen 3 / Pollinations AI)
```

---

## Environment Variables Guide (.env)

The application uses `python-dotenv` to read environment variables from a `.env` file at the root of the project.

### Overview of All Variables

| Variable Name | Required | Default Value | Description |
| :--- | :---: | :--- | :--- |
| `DEBUG` | Optional | `True` | Runs Django in debug mode for development. Set to `False` in production. |
| `SECRET_KEY` | **Recommended** | Built-in fallback | Unique cryptographic key for Django sessions and CSRF security. |
| `APP_URL` | Optional | `http://localhost:3000` | The primary URL where the app is hosted (used for CSRF trusted origins). |
| `USE_SQLITE` | Optional | `True` | When `True`, runs with local SQLite (`db.sqlite3`). Set `False` to use PostgreSQL. |
| `DB_NAME` | Required if Postgres | `ai_image_generator` | PostgreSQL database name. |
| `DB_USER` | Required if Postgres | `postgres` | PostgreSQL username. |
| `DB_PASSWORD` | Required if Postgres | `your-password` | PostgreSQL password. |
| `DB_HOST` | Required if Postgres | `localhost` | PostgreSQL host address (e.g. `localhost` or remote IP). |
| `DB_PORT` | Required if Postgres | `5432` | PostgreSQL port (default is `5432`). |
| `GEMINI_API_KEY` | Optional | None | Google AI Studio API key for Google GenAI models. |
| `IMAGE_API_KEY` | Optional | None | Alternate/Custom AI generation service key. |

---

### Where and How to Get Each Value

#### 1. `SECRET_KEY`
- **What it is**: A long, random string used by Django to sign cookies and CSRF tokens.
- **Where to get it**: You can generate a fresh, secure Django secret key right from your terminal by running:
  ```bash
  python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  Copy the output string and paste it as `SECRET_KEY=your_output_key_here`.

#### 2. `GEMINI_API_KEY` / `IMAGE_API_KEY`
- **What it is**: The API key required to invoke Google AI Studio models (such as Imagen 3 / Gemini).
- **Where to get it (Free)**:
  1. Visit **[Google AI Studio](https://aistudio.google.com/)**.
  2. Sign in with your Google account.
  3. Navigate to **Get API Key** or open **[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)** directly.
  4. Click **Create API Key** (choose an existing Google Cloud project or let AI Studio create a new one).
  5. Copy your generated key (starts with `AIza...` or similar).
  6. Paste it into `.env`:
     ```env
     GEMINI_API_KEY=AIzaSyD...
     ```
  > **Note**: Even if you leave this empty, the application will automatically fall back to **Pollinations AI**, which is free, public, and works out-of-the-box with zero configuration!

#### 3. Database Credentials (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)
- **Option A: Instant Zero-Configuration (Default)**
  - Set `USE_SQLITE=True` in `.env`.
  - No database server or password needed! Django will automatically create and use a local `db.sqlite3` file.

- **Option B: Using PostgreSQL**
  - Set `USE_SQLITE=False` in `.env`.
  - **Where to get/create values**:
    1. Install PostgreSQL on your computer (from [postgresql.org](https://www.postgresql.org/download/)).
    2. Open your terminal or `psql`:
       ```bash
       psql -U postgres
       ```
    3. Run the following SQL queries to create your database and user:
       ```sql
       CREATE DATABASE ai_image_generator;
       CREATE USER postgres WITH PASSWORD 'mysecurepassword';
       GRANT ALL PRIVILEGES ON DATABASE ai_image_generator TO postgres;
       ```
    4. Fill in `.env` with the values you just created:
       ```env
       USE_SQLITE=False
       DB_NAME=ai_image_generator
       DB_USER=postgres
       DB_PASSWORD=mysecurepassword
       DB_HOST=localhost
       DB_PORT=5432
       ```

#### 4. `APP_URL`
- For local running: `http://localhost:3000` or `http://127.0.0.1:8000`.
- For production: Your full domain name (e.g., `https://myapp.com`).

---

## Step-by-Step Installation & Run Guide

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.10+**: Run `python3 --version` (or `python --version` on Windows) to verify.
- **Git**: Run `git --version` to verify.
- **Pip**: Python package manager (included with Python).

---

### 1. Clone or Navigate to Project

```bash
cd ai-image-generator
```

---

### 2. Set Up a Virtual Environment

Isolating dependencies ensures no conflicts with other Python projects.

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

*(You will see `(venv)` in your terminal prompt when activated).*

---

### 3. Install Dependencies

Install all required Python libraries from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 4. Create and Configure `.env`

Copy the provided example file:

**macOS / Linux:**
```bash
cp .env.example .env
```

**Windows:**
```cmd
copy .env.example .env
```

Open `.env` in any text editor (e.g. VS Code, Notepad, nano) and verify your settings. Here is a ready-to-use default template:

```env
# Application Settings
DEBUG=True
SECRET_KEY=django-insecure-ai-image-generator-key-9284712048
APP_URL=http://localhost:3000

# Database Configuration (Set True for zero-setup SQLite, or False for PostgreSQL)
USE_SQLITE=True
DB_NAME=ai_image_generator
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# AI Service Keys (Optional: leaves empty to use built-in diffusion fallback)
GEMINI_API_KEY=
IMAGE_API_KEY=
```

---

### 5. Run Database Migrations

Apply Django migrations to set up the `ImageGeneration` table:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

You should see output ending with:
```
Applying generator.0001_initial... OK
```

---

### 6. Start the Development Server

Start the Django application on port 3000 (or default port 8000):

**To run on port 3000 (standard):**
```bash
python3 manage.py runserver 0.0.0.0:3000
```

*(Or if you use npm / standard runner: `npm run dev` or `npm start`)*.

---

### 7. Open in Your Browser

Open your preferred web browser and navigate to:

```
http://localhost:3000/
```
*(or `http://127.0.0.1:8000/` if running on default port).*

---

## Application Routes & Features

| Route | Method | Description |
| :--- | :---: | :--- |
| `/` | `GET` | **Home Page**: Features the prompt input form, style selectors, and aspect ratio chips. |
| `/generate/` | `POST` | **Generation Action**: Validates prompt and creates the image. Displays the result page. |
| `/history/` | `GET` | **Generation History**: Visual gallery of all previously generated images with metadata. |
| `/generation/<id>/` | `GET` | **Detail View**: View full prompt, creation timestamp, and high-res image preview. |
| `/generation/<id>/download/` | `GET` | **Direct Download**: Streams the JPEG image directly as a downloadable attachment. |
| `/generation/<id>/delete/` | `POST` | **Delete Generation**: Removes the record and redirects cleanly to `/history/`. |

---

## Testing & Quality Assurance

The project includes an automated unit and integration test suite testing models, views, forms, and service fallbacks.

### Run the Test Suite

```bash
python3 manage.py test generator
```

Expected output:
```
Ran 12 tests in 0.070s
OK
```

### Run Django System Check

```bash
python3 manage.py check
```

Expected output:
```
System check identified no issues (0 silenced).
```

---

## Project Structure

```
ai-image-generator/
│
├── manage.py                   # Django CLI management script
├── package.json                # Run and test scripts configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment variables
├── .env                        # Local environment configuration file
├── README.md                   # Comprehensive project documentation
│
├── config/                     # Django project configuration
│   ├── __init__.py
│   ├── settings.py             # App settings, DB logic, static/media paths
│   ├── urls.py                 # Root URL configuration (No admin exposed)
│   ├── wsgi.py                 # WSGI production entrypoint
│   └── asgi.py                 # ASGI entrypoint
│
├── generator/                  # Core Image Generator application
│   ├── migrations/             # Database migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py     # ImageGeneration schema
│   │
│   ├── templates/generator/    # Server-rendered HTML templates
│   │   ├── base.html           # Shared layout, skip-links, header, footer
│   │   ├── home.html           # Generation prompt form & style selection
│   │   ├── result.html         # Generated image display & actions
│   │   ├── history.html        # Gallery grid of all generations
│   │   └── detail.html         # Single generation view & delete confirm
│   │
│   ├── static/generator/css/
│   │   └── style.css           # Pure CSS3 dark design system (Zero JS)
│   │
│   ├── forms.py                # Django Form with server-side validation
│   ├── models.py               # ImageGeneration ORM model
│   ├── services.py             # Isolated AI generation service layer
│   ├── views.py                # Server-rendered view handlers & downloads
│   ├── urls.py                 # App URL patterns
│   └── tests.py                # Comprehensive test suite
│
└── media/                      # Generated image files directory
    └── generations/            # Stored JPEG assets
```

---

## Troubleshooting & FAQs

### Q1: `ModuleNotFoundError: No module named 'django'`
**Solution**: Make sure your virtual environment is activated (`source venv/bin/activate` or `venv\Scripts\activate`) before running `pip install -r requirements.txt`.

### Q2: `Connection to server at "localhost", port 5432 failed`
**Solution**: If you don't have PostgreSQL running locally, simply open `.env` and set:
```env
USE_SQLITE=True
```
Django will switch to SQLite automatically and execute smoothly without needing PostgreSQL.

### Q3: `Forbidden (403) CSRF verification failed`
**Solution**: If you are accessing the app from an external host or behind an ngrok/cloud proxy, add your domain to `CSRF_TRUSTED_ORIGINS` in `config/settings.py` or set `APP_URL` in `.env`:
```env
APP_URL=https://your-domain.com
```

### Q4: Does image generation work without a Gemini API Key?
**Yes!** The application has a resilient dual-provider setup in `generator/services.py`. If `GEMINI_API_KEY` is not provided or quota is limited, it automatically falls back to Pollinations AI, ensuring images are generated without errors.

---

## License

This project is licensed under the [MIT License](LICENSE).
Feel free to customize, adapt, and use it in your personal and commercial projects.
