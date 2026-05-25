# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Windows desktop app that captures a screen region via mouse drag and sends it to Google Cloud Vision API for OCR. Built with Python / Tkinter. Targets Windows only.

## Setup

```powershell
uv sync                         # install deps + create .venv
.venv\Scripts\Activate.ps1      # activate
```

Create a `.env` file at the project root:

```
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_LOCATION=asia-northeast1
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}   # single-line JSON
```

Use `scripts/json_minifier.py` to convert a multi-line service account JSON file to the single-line format required by `GOOGLE_CREDENTIALS_JSON`.

## Commands

```bash
python main.py          # run the app
pyright                 # static type checking
python build.py         # build standalone .exe (PyInstaller)
```

Test commands are in `.claude/rules/testing.md`.

## Architecture

Three layers — put new code in the right layer:

| Layer | Directory | Responsibility |
|---|---|---|
| Presentation | `app/` | Tkinter GUI, screen capture |
| Business logic | `service/`, `external_service/` | OCR orchestration, file I/O |
| Utilities | `utils/`, `widgets/` | Config, constants, UI factories |

All UI text must go through `utils/constants.py` — no magic strings in other files.

## Git

Commit directly to `main`. No branch convention.
