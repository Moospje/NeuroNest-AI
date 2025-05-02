import Link from 'next/link';
import Image from 'next/image';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm flex flex-col">
        <div className="flex flex-col items-center justify-center">
          <h1 className="text-4xl md:text-6xl font-bold text-center mb-6 bg-gradient-to-r from-primary-500 to-secondary-500 text-transparent bg-clip-text">
            NeuroNest-AI
          </h1>
          <p className="text-xl md:text-2xl text-center mb-12 max-w-2xl">
            Advanced AI Agent Orchestration Platform
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
          <Link
            href="/login"
            className="group rounded-lg border border-neutral-200 dark:border-neutral-800 px-5 py-4 transition-colors hover:border-primary-300 hover:bg-primary-50 dark:hover:border-primary-700 dark:hover:bg-primary-900/30"
          >
            <h2 className="mb-3 text-2xl font-semibold">
              Login{' '}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                →
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-70">
              Sign in to your account to access your conversations.
            </p>
          </Link>

          <Link
            href="/register"
            className="group rounded-lg border border-neutral-200 dark:border-neutral-800 px-5 py-4 transition-colors hover:border-secondary-300 hover:bg-secondary-50 dark:hover:border-secondary-700 dark:hover:bg-secondary-900/30"
          >
            <h2 className="mb-3 text-2xl font-semibold">
              Register{' '}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                →
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-70">
              Create a new account to get started with NeuroNest-AI.
            </p>
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-4xl">
          <div className="flex flex-col items-center text-center">
            <div className="rounded-full bg-primary-100 dark:bg-primary-900 p-4 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-primary-600 dark:text-primary-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Multiple AI Agents</h3>
            <p className="text-sm opacity-70">
              Interact with specialized agents for different tasks.
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="rounded-full bg-secondary-100 dark:bg-secondary-900 p-4 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-secondary-600 dark:text-secondary-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Intelligent Orchestration</h3>
            <p className="text-sm opacity-70">
              Automatically routes requests to the most appropriate agent.
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="rounded-full bg-primary-100 dark:bg-primary-900 p-4 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-primary-600 dark:text-primary-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Multi-Device Support</h3>
            <p className="text-sm opacity-70">
              Access your conversations from any device securely.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}