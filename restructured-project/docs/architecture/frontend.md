# Frontend Architecture

NeuroNest-AI uses Next.js and React to provide a modern, responsive user interface. This document describes the frontend architecture, components, and state management.

## Frontend Structure

The frontend follows a component-based architecture using Next.js and React:

### Directory Structure

```
frontend/
│
├── app/                      # Next.js app directory
│   ├── page.tsx              # Home page
│   ├── layout.tsx            # Root layout
│   ├── login/                # Login page
│   ├── register/             # Registration page
│   └── dashboard/            # Dashboard pages
│
├── components/               # React components
│   ├── ui/                   # UI components
│   ├── chat/                 # Chat-related components
│   └── layout/               # Layout components
│
├── lib/                      # Utility functions
│
├── store/                    # State management
│
├── styles/                   # CSS styles
│
├── public/                   # Static assets
│
├── next.config.js            # Next.js configuration
└── tailwind.config.js        # Tailwind CSS configuration
```

## Pages

NeuroNest-AI uses Next.js App Router for routing. The main pages include:

- **Home Page**: Landing page for unauthenticated users
- **Login Page**: User login form
- **Registration Page**: User registration form
- **Dashboard**: Main application dashboard
- **Conversations**: List of user conversations
- **Chat**: Chat interface for interacting with agents
- **Agents**: Information about available agents
- **Settings**: User settings and preferences

## Components

The frontend is built using reusable React components:

### UI Components

Basic UI components that implement the design system:

- **Button**: Styled button component
- **Input**: Form input component
- **Card**: Container component with styling
- **Modal**: Dialog component for overlays
- **Dropdown**: Dropdown menu component
- **Tabs**: Tabbed interface component
- **Toast**: Notification component

### Chat Components

Components specific to the chat interface:

- **ChatWindow**: Main chat interface container
- **MessageList**: List of chat messages
- **MessageItem**: Individual chat message
- **MessageInput**: Input field for sending messages
- **AgentSelector**: Component for selecting an agent
- **TypingIndicator**: Indicator for when an agent is "typing"

### Layout Components

Components for page layout:

- **Navbar**: Top navigation bar
- **Sidebar**: Side navigation menu
- **Footer**: Page footer
- **Container**: Page container with responsive width
- **Grid**: Grid layout component

## State Management

NeuroNest-AI uses Zustand for state management. The main stores include:

### Auth Store

Manages authentication state:

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  username: string;
  email: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (token, user) => set({ token, user, isAuthenticated: true }),
      logout: () => set({ token: null, user: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

### Chat Store

Manages chat state:

```typescript
import { create } from 'zustand';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  agent?: string;
  createdAt: string;
}

interface Conversation {
  id: string;
  title: string;
  messages: Message[];
}

interface ChatState {
  conversations: Conversation[];
  currentConversation: Conversation | null;
  isLoading: boolean;
  setConversations: (conversations: Conversation[]) => void;
  setCurrentConversation: (conversation: Conversation | null) => void;
  addMessage: (conversationId: string, message: Message) => void;
  setLoading: (isLoading: boolean) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  conversations: [],
  currentConversation: null,
  isLoading: false,
  setConversations: (conversations) => set({ conversations }),
  setCurrentConversation: (conversation) => set({ currentConversation: conversation }),
  addMessage: (conversationId, message) =>
    set((state) => ({
      conversations: state.conversations.map((conv) =>
        conv.id === conversationId
          ? { ...conv, messages: [...conv.messages, message] }
          : conv
      ),
      currentConversation:
        state.currentConversation?.id === conversationId
          ? {
              ...state.currentConversation,
              messages: [...state.currentConversation.messages, message],
            }
          : state.currentConversation,
    })),
  setLoading: (isLoading) => set({ isLoading }),
}));
```

## API Integration

The frontend communicates with the backend API using Axios:

```typescript
import axios from 'axios';
import { useAuthStore } from '@/store/auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

## WebSocket Integration

The frontend uses WebSockets for real-time chat:

```typescript
import { useEffect, useRef } from 'react';
import { useAuthStore } from '@/store/auth';
import { useChatStore } from '@/store/chat';

export function useChatWebSocket(conversationId: string) {
  const socket = useRef<WebSocket | null>(null);
  const token = useAuthStore((state) => state.token);
  const addMessage = useChatStore((state) => state.addMessage);

  useEffect(() => {
    if (!token || !conversationId) return;

    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'}/api/v1/ws/chat/${conversationId}?token=${token}`;
    socket.current = new WebSocket(wsUrl);

    socket.current.onopen = () => {
      console.log('WebSocket connected');
    };

    socket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'message') {
        addMessage(conversationId, {
          id: data.message_id,
          content: data.content,
          role: data.role,
          agent: data.agent,
          createdAt: data.created_at,
        });
      }
    };

    socket.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    socket.current.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      if (socket.current) {
        socket.current.close();
      }
    };
  }, [token, conversationId, addMessage]);

  const sendMessage = (content: string, agent?: string) => {
    if (socket.current && socket.current.readyState === WebSocket.OPEN) {
      socket.current.send(
        JSON.stringify({
          type: 'message',
          content,
          agent,
          conversation_id: conversationId,
        })
      );
    }
  };

  return { sendMessage };
}
```

## Styling

NeuroNest-AI uses Tailwind CSS for styling:

```typescript
// tailwind.config.js
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        secondary: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
        },
      },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')],
};
```

## Responsive Design

NeuroNest-AI is designed to be responsive and work well on all device sizes:

- **Mobile**: Optimized for small screens (< 640px)
- **Tablet**: Optimized for medium screens (640px - 1024px)
- **Desktop**: Optimized for large screens (> 1024px)

## Accessibility

NeuroNest-AI follows accessibility best practices:

- **Semantic HTML**: Using appropriate HTML elements
- **ARIA Attributes**: Adding ARIA attributes where needed
- **Keyboard Navigation**: Supporting keyboard navigation
- **Color Contrast**: Ensuring sufficient color contrast
- **Screen Reader Support**: Making the UI accessible to screen readers

## Performance Optimization

NeuroNest-AI implements several performance optimizations:

- **Code Splitting**: Splitting code into smaller chunks
- **Image Optimization**: Using Next.js Image component
- **Lazy Loading**: Loading components only when needed
- **Memoization**: Memoizing expensive computations
- **Server-Side Rendering**: Pre-rendering pages on the server

## Best Practices

When working with the frontend:

1. **Component Reusability**: Create reusable components
2. **Type Safety**: Use TypeScript for type safety
3. **State Management**: Use Zustand for global state
4. **Error Handling**: Implement proper error handling
5. **Testing**: Write tests for components and hooks
6. **Documentation**: Document components and their props