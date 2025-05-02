# NeuroNest-AI Frontend

This is the frontend for the NeuroNest-AI project, built with Next.js and Tailwind CSS.

## Getting Started

First, install the dependencies:

```bash
npm install
# or
yarn install
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Features

- Modern UI with Tailwind CSS
- State management with Zustand
- Authentication with JWT
- Real-time chat with WebSockets
- Multi-device support

## Project Structure

```
frontend/
├── app/                  # Next.js app directory
│   ├── (auth)/           # Authentication pages
│   ├── (dashboard)/      # Dashboard pages
│   ├── api/              # API routes
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page
├── components/           # React components
│   ├── ui/               # UI components
│   ├── chat/             # Chat components
│   └── layout/           # Layout components
├── lib/                  # Utility functions
│   ├── api.ts            # API client
│   ├── auth.ts           # Authentication utilities
│   └── utils.ts          # General utilities
├── store/                # Zustand store
│   ├── auth-store.ts     # Authentication store
│   ├── chat-store.ts     # Chat store
│   └── index.ts          # Store exports
├── styles/               # Global styles
├── public/               # Static assets
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── package.json          # Dependencies and scripts
```

## Deployment

The frontend can be deployed using Docker. See the Dockerfile and docker-compose.yml in the root directory for more information.