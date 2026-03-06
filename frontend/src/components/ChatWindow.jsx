import React, { useRef, useEffect } from 'react';
import { Bot, User } from 'lucide-react';
import CitationCard from './CitationCard';

function ChatWindow({ messages, isLoading }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="chat-messages">
      <div className="welcome-section">
        {!messages.length && (
          <div className="welcome-content">
            <h2 className="cyan-glow">Welcome to PolicyLens</h2>
            <p>Your local assistant for EU tech regulations and digital law.</p>
          </div>
        )}
      </div>

      {messages.map((msg, i) => (
        <div key={i} className={`message-row ${msg.role}`}>
          <div className="message-container">
            <div className="message-icon">
              {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
            </div>
            <div className="message-text">
              <div className="role-label">{msg.role === 'user' ? 'You' : 'PolicyAdvisor'}</div>
              <div className="content">
                {msg.content.split('\n').map((line, j) => (
                  <p key={j}>{line}</p>
                ))}
              </div>
              {msg.citations && (
                <div className="citations-area">
                  <CitationCard citations={msg.citations} />
                </div>
              )}
            </div>
          </div>
        </div>
      ))}

      {isLoading && (
        <div className="message-row assistant">
          <div className="message-container">
            <div className="message-icon rotating">
              <Bot size={18} />
            </div>
            <div className="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      )}
      <div ref={scrollRef} />

      <style jsx>{`
        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 20px 0;
        }

        .welcome-section {
          height: 200px;
          display: flex;
          align-items: center;
          justify-content: center;
          text-align: center;
        }

        .welcome-content h2 {
          font-family: var(--font-display);
          font-size: 2.5rem;
          margin-bottom: 10px;
        }

        .message-row {
          width: 100%;
          padding: 30px 40px;
          border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .message-row.user {
          background: transparent;
        }

        .message-row.assistant {
          background: rgba(255, 255, 255, 0.02);
        }

        .message-container {
          max-width: 800px;
          margin: 0 auto;
          display: flex;
          gap: 20px;
        }

        .message-icon {
          width: 32px;
          height: 32px;
          min-width: 32px;
          background: var(--bg-tertiary);
          border-radius: 4px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: var(--text-secondary);
        }

        .message-row.assistant .message-icon {
          background: var(--accent-cyan-dim);
          color: var(--accent-cyan);
        }

        .role-label {
          font-size: 0.75rem;
          font-weight: bold;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 8px;
          color: var(--text-secondary);
        }

        .content p {
          margin-bottom: 15px;
          line-height: 1.6;
          font-size: 1.05rem;
        }

        .citations-area {
          margin-top: 20px;
        }

        .typing-indicator {
          display: flex;
          gap: 4px;
          align-items: center;
          height: 32px;
        }

        .typing-indicator span {
          width: 6px;
          height: 6px;
          background: var(--accent-cyan);
          border-radius: 50%;
          animation: bounce 1.4s infinite ease-in-out both;
        }

        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1.0); }
        }

        .rotating {
          animation: spin 2s linear infinite;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default ChatWindow;
