# NeuroNest-AI Desktop Application

This directory contains the Electron-based desktop application for NeuroNest-AI.

## Features

- Native desktop application for Windows, macOS, and Linux
- System tray integration
- Native notifications
- Automatic updates
- Offline capabilities
- Keyboard shortcuts

## Development

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Setup

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm start
```

This will launch the Electron application in development mode.

### Building

To build the application for your current platform:

```bash
npm run build
```

To build for specific platforms:

```bash
# Windows
npm run build:win

# macOS
npm run build:mac

# Linux
npm run build:linux
```

The built applications will be available in the `dist` directory.

## Architecture

The desktop application is built using Electron and communicates with the NeuroNest-AI backend API. It provides a native wrapper around the web application with additional desktop-specific features.

### Main Process

The main process (`main.js`) is responsible for:

- Creating and managing application windows
- Handling application lifecycle events
- Managing the application menu
- Implementing auto-updates
- Communicating with the renderer process via IPC

### Renderer Process

The renderer process is the web application loaded in the Electron window. It communicates with the main process via IPC to access native features.

## Distribution

The application is packaged and distributed using electron-builder. The configuration for the build process is defined in the `package.json` file under the `build` key.