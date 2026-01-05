# fotacos

[![Release](https://img.shields.io/github/v/release/MonsignorEduardo/fotacos)](https://img.shields.io/github/v/release/MonsignorEduardo/fotacos)
[![Build status](https://img.shields.io/github/actions/workflow/status/MonsignorEduardo/fotacos/main.yml?branch=main)](https://github.com/MonsignorEduardo/fotacos/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/MonsignorEduardo/fotacos/branch/main/graph/badge.svg)](https://codecov.io/gh/MonsignorEduardo/fotacos)
[![Commit activity](https://img.shields.io/github/commit-activity/m/MonsignorEduardo/fotacos)](https://img.shields.io/github/commit-activity/m/MonsignorEduardo/fotacos)
[![License](https://img.shields.io/github/license/MonsignorEduardo/fotacos)](https://img.shields.io/github/license/MonsignorEduardo/fotacos)

Multi-interface photo album application for Raspberry Pi with web, desktop GUI, and REST API.

- **📦 Github repository**: <https://github.com/MonsignorEduardo/fotacos/>
- **📚 Documentation**: <https://MonsignorEduardo.github.io/fotacos/>

## Features

- 🌐 **Web Interface**: React-based photo gallery with modern UI
- 🖥️ **Desktop GUI**: PySide6/Qt QML application for slideshow mode
- 🔌 **REST API**: FastAPI backend for photo management
- 🖼️ **Image Processing**: Automatic WebP conversion and thumbnail generation
- 📱 **Responsive**: Works on desktop, tablet, and mobile devices

## Quick Start

### Development

Install dependencies and run the development server:

```bash
make install
make dev
```

The web interface will be available at `http://localhost:3000` and the API at `http://localhost:8000`.

### Desktop GUI

Run the desktop application:

fotacos gui
```

### Raspberry Pi Setup

For detailed Raspberry Pi installation instructions, see [RASPBERRY_PI_SETUP.md](RASPBERRY_PI_SETUP.md).

## Development

### Running Tests

```bash
make test
```

### Code Quality Checks

```bash
make check
```

### Building for Production

```bash
make build
```

## Documentation

Full documentation is available at <https://MonsignorEduardo.github.io/fotacos/>

## License

This project is licensed under the terms of the license specified in the [LICENSE](LICENSE) file.


---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
