# Fotacos - AI Coding Agent Instructions

## Project Overview

Fotacos is a **multi-interface photo album application** for Raspberry Pi with three distinct frontends sharing a unified FastAPI backend:
- **Web**: React + TanStack Router + Vite (TypeScript) at `src/web/`
- **GUI**: PySide6/Qt QML desktop application at `src/fotacos/gui/`
- **API**: FastAPI REST service serving both frontends

The backend handles photo uploads, converts images to WebP format, generates thumbnails, and stores metadata in SQLite via Tortoise ORM.

## Architecture & Data Flow

### Backend Structure (`src/fotacos/`)
- **`api/app.py`**: FastAPI app configuration with CORS, static file mounting (`/public` for photos, `/` for built web app)
- **`api/routes/photos.py`**: Photo CRUD endpoints (`GET /api/photos`, `POST /api/photos`, `DELETE /api/photos/{id}`)
- **`models/photo.py`**: Tortoise ORM model with fields: `filename`, `original_url`, `thumbnail_url`, `file_size`, `created_at`
- **`services/images.py`**: PIL-based image processing (WebP conversion with EXIF orientation fixing, thumbnail generation)
- **`database.py`**: Tortoise ORM initialization pointing to `fotacos.models.photo` module
- **`env.py`**: Pydantic Settings for config (database_url, upload_dir, CORS origins, thumbnail settings)

### Frontend-Backend Integration
- **Web dev mode** (`make dev`): Vite proxies `/api` and `/public` requests to FastAPI at `localhost:8000` (see `src/web/vite.config.ts`)
- **Production**: Web frontend builds to `src/web/dist/`, which gets bundled into Python wheel via `hatch` (see `tool.hatch.build.targets.wheel.force-include` in `pyproject.toml`)
- **API responses**: Pydantic models (`PhotoResponse`, `PhotoListResponse`) in `api/routes/photos.py` define JSON contract
- **Web client**: TanStack Query in `src/web/src/lib/api.ts` handles API calls with TypeScript types matching backend schemas

## Development Workflows

### Setup & Running
```bash
make install         # uv sync + pre-commit install + bun install (web deps)
make dev            # honcho starts both API (uvicorn) and web (vite) with hot reload
fotacos gui         # Run PySide6 desktop app (separate from web)
```

**Critical**: Use `uv run` prefix for all Python commands (e.g., `uv run pytest`, `uv run fotacos gui`)

### Code Quality & Testing
```bash
make check          # Runs: uv lock check, pre-commit, ty (type checking), deptry (unused deps)
make test           # pytest with coverage (reports to codecov)
make build          # Builds web frontend THEN creates Python wheel (includes web dist/)
```

**Linting**: Ruff configured with strict rules (120 char line length, auto-fix enabled). Ignores `E501` (line too long) and `E731` (lambda assignment). Tests allow `S101` (assert usage).

**Type checking**: Uses `ty` (not mypy) - see `[tool.ty.environment]` in `pyproject.toml`

### Photo Upload Flow (Critical Implementation Detail)
1. User uploads photo via `POST /api/photos` with multipart/form-data
2. Backend validates extension (`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`) and MIME type
3. Generate unique filename with UUID: `f"{uuid.uuid4()}.webp"`
4. Image processing pipeline:
   - Original: Convert to WebP (quality 90, preserves transparency for RGBA/P modes)
   - Thumbnail: Resize to `settings.thumbnail_size` (default 300x300) as WebP (quality 85)
   - Both apply `_fix_orientation()` from EXIF data before processing
5. Save to `public/picts/` (original) and `public/picts/thumbnails/` (thumbnail)
6. Store Photo record in SQLite with URL paths like `/public/picts/{filename}.webp`
7. Return `PhotoResponse` with `id`, `filename`, URLs, `file_size`, `created_at`

## Project-Specific Conventions

### Python
- **Settings pattern**: Single `get_settings()` singleton via `@lru_cache` in `env.py`, imported across modules
- **Database access**: Always use Tortoise ORM methods (`Photo.all()`, `Photo.create()`, `Photo.filter()`) - no raw SQL
- **Logging**: Loguru configured in `logging_config.py` (not standard logging), use `logger.info/debug/warning`
- **File organization**: Service layer (`services/`) for business logic, routes call services, no logic in route handlers beyond validation
- **EXIF handling**: All image operations MUST call `_fix_orientation()` to respect camera rotation metadata

### TypeScript/Web
- **Router**: TanStack Router with file-based routing (`src/routes/`) - `routeTree.gen.ts` is auto-generated
- **State**: TanStack Query for server state, no Redux/Zustand - queries in `src/lib/hooks.ts`
- **Styling**: Tailwind CSS v4 with shadcn/ui components in `src/components/ui/`
- **API integration**: Environment var `VITE_API_URL` for API base (falls back to `http://localhost:8000/api`)
- **Formatting**: Biome (not Prettier/ESLint) - `bun run check` runs all formatting/linting

### Build System Quirks
- **Wheel packaging**: Web frontend build outputs (`src/web/dist/`) are included in Python package via hatch force-include
- **Multi-process dev**: `honcho` (Python Foreman) manages concurrent API + web servers via `Procfile.dev`
- **Package manager**: `uv` for Python (not pip/poetry), `bun` for Node (not npm/yarn/pnpm)

## Common Tasks

### Adding a New API Endpoint
1. Define Pydantic response model in `api/routes/photos.py` (or new router file)
2. Add route handler to existing router or create new router in `api/routes/`
3. Include router in `api/app.py` with `app.include_router(router, prefix="/api")`
4. Update TypeScript types in `src/web/src/lib/api.ts` to match
5. Create TanStack Query hook in `src/web/src/lib/hooks.ts` if needed

### Modifying Image Processing
- Edit functions in `services/images.py`
- All PIL operations should use context managers (`with Image.open()`)
- Always seek to position 0 before reading BinaryIO streams
- Preserve transparency for RGBA/P modes when converting formats
- Test EXIF orientation handling with rotated images

### Database Schema Changes
1. Modify model in `models/photo.py`
2. Run app once to trigger `Tortoise.generate_schemas()` (auto-applies changes in dev)
3. For production, consider migration tools (not currently configured)

## External Dependencies

- **Database**: SQLite via Tortoise ORM (async), default path `fotacos.db` in project root
- **Image processing**: Pillow (PIL) for conversion/thumbnails
- **File storage**: Local filesystem in `public/picts/` (configurable via `Settings.upload_dir`)
- **CORS**: Configured for `http://localhost:3000` by default (see `env.py`)

## What NOT to Change
- Don't add `requirements.txt` or `poetry.lock` - use `uv` and `pyproject.toml` only
- Don't install `eslint` or `prettier` - web uses Biome exclusively
- Don't create separate `config.py` files - all settings via `env.py` Pydantic Settings
- Don't use `flask` or `django` patterns - this is FastAPI with async/await throughout
