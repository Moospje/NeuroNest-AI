import React from 'react';
import { cn } from '../../lib/utils';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import remarkGfm from 'remark-gfm';

interface MessageItemProps {
  content: string;
  role: 'user' | 'assistant' | 'system';
  agent?: string;
  timestamp?: string;
}

export const MessageItem: React.FC<MessageItemProps> = ({
  content,
  role,
  agent,
  timestamp,
}) => {
  const isUser = role === 'user';

  return (
    <div
      className={cn(
        'flex w-full mb-4',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={cn(
          'max-w-[80%] rounded-lg p-4',
          isUser
            ? 'bg-primary text-primary-foreground'
            : 'bg-secondary text-secondary-foreground'
        )}
      >
        {agent && !isUser && (
          <div className="text-xs font-semibold mb-1">{agent}</div>
        )}
        <div className="prose dark:prose-invert max-w-none">
          <ReactMarkdown
            rehypePlugins={[rehypeHighlight]}
            remarkPlugins={[remarkGfm]}
          >
            {content}
          </ReactMarkdown>
        </div>
        {timestamp && (
          <div className="text-xs opacity-70 mt-2 text-right">{timestamp}</div>
        )}
      </div>
    </div>
  );
};

export default MessageItem;