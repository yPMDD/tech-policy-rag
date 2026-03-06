import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Plus, History, ShieldAlert, LogIn, ExternalLink, ChevronRight } from 'lucide-react';
import ChatWindow from './components/ChatWindow';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [conversations, setConversations] = useState([]);
  const [currentConvId, setCurrentConvId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState(null); // Mock user for now

  // Placeholder for user ID since we are in dev/mock phase
  const userId = 1; 

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await axios.get(`/api/conversations?user_id=${userId}`);
      setConversations(res.data);
    } catch (err) {
      console.error("Error fetching conversations:", err);
    }
  };

  const loadHistory = async (convId) => {
    setCurrentConvId(convId);
    try {
      const res = await axios.get(`/api/conversations/${convId}/history?user_id=${userId}`);
      setMessages(res.data.map(m => ({
        role: m.role,
        content: m.content,
        citations: m.citations
      })));
    } catch (err) {
      console.error("Error loading history:", err);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await axios.post('/api/chat', {
        user_id: userId,
        query: input,
        conversation_id: currentConvId
      });

      const aiMsg = { 
        role: 'assistant', 
        content: res.data.answer,
        citations: res.data.citations 
      };
      
      setMessages(prev => [...prev, aiMsg]);
      
      if (!currentConvId) {
        setCurrentConvId(res.data.conversation_id);
        fetchConversations();
      }
    } catch (err) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "I'm sorry, I encountered an error connecting to the legal engine. Please check if the server is running." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar glass">
        <div className="sidebar-header">
          <button className="new-chat-btn" onClick={() => {
            setCurrentConvId(null);
            setMessages([]);
          }}>
            <Plus size={18} /> New Chat
          </button>
        </div>
        
        <div className="history-list">
          <h3>Recent Chats</h3>
          {conversations.map(c => (
            <div 
              key={c.id} 
              className={`history-item ${currentConvId === c.id ? 'active' : ''}`}
              onClick={() => loadHistory(c.id)}
            >
              <History size={14} />
              <span>{c.title}</span>
            </div>
          ))}
        </div>

        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="avatar">JD</div>
            <span>John Doe</span>
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="main-content">
        <header className="main-header top-glass">
          <div className="brand">
            <h1 className="cyan-glow">Tech Policy <span className="text-secondary">RAG</span></h1>
          </div>
          <div className="header-actions">
             <ShieldAlert size={18} className="text-secondary" />
             <span className="text-secondary" style={{fontSize: '0.8rem'}}>EU Policy Guard Active</span>
          </div>
        </header>

        <ChatWindow messages={messages} isLoading={isLoading} />

        <div className="input-container">
          <div className="input-wrapper glass">
            <input 
              type="text" 
              placeholder="Ask about GDPR, AI Act, or NIS2..." 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            />
            <button className="send-btn" onClick={handleSend} disabled={isLoading}>
              <Send size={20} />
            </button>
          </div>
          <p className="disclaimer">
            This AI provides guidance based on regulatory documents but is not a substitute for professional legal advice.
          </p>
        </div>
      </main>

      <style jsx>{`
        .app-container {
          display: flex;
          height: 100vh;
          width: 100vw;
          background-color: var(--bg-primary);
        }

        .sidebar {
          width: 260px;
          height: 100%;
          display: flex;
          flex-direction: column;
          padding: 15px;
          border-right: 1px solid var(--border-color);
        }

        .new-chat-btn {
          width: 100%;
          padding: 12px;
          border: 1px solid var(--border-color);
          background: transparent;
          color: white;
          border-radius: 8px;
          display: flex;
          align-items: center;
          gap: 10px;
          cursor: pointer;
          transition: var(--transition);
          margin-bottom: 20px;
        }

        .new-chat-btn:hover {
          background: var(--bg-tertiary);
        }

        .history-list {
          flex: 1;
          overflow-y: auto;
        }

        .history-list h3 {
          font-size: 0.7rem;
          color: var(--text-secondary);
          text-transform: uppercase;
          margin-bottom: 15px;
          letter-spacing: 1px;
        }

        .history-item {
          padding: 10px;
          border-radius: 6px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 12px;
          color: var(--text-secondary);
          font-size: 0.9rem;
          margin-bottom: 4px;
          transition: var(--transition);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .history-item:hover, .history-item.active {
          background: var(--bg-secondary);
          color: white;
        }

        .history-item.active {
          border-left: 2px solid var(--accent-cyan);
        }

        .main-content {
          flex: 1;
          display: flex;
          flex-direction: column;
          position: relative;
        }

        .main-header {
          height: 60px;
          padding: 0 40px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          z-index: 10;
        }

        .input-container {
          padding: 20px 40px 40px;
          max-width: 900px;
          width: 100%;
          margin: 0 auto;
        }

        .input-wrapper {
          display: flex;
          padding: 8px 15px;
          border-radius: 12px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }

        .input-wrapper input {
          flex: 1;
          background: transparent;
          border: none;
          color: white;
          padding: 10px;
          font-size: 1rem;
          outline: none;
        }

        .send-btn {
          background: transparent;
          border: none;
          color: var(--text-secondary);
          cursor: pointer;
          padding: 5px;
          transition: var(--transition);
        }

        .send-btn:hover:not(:disabled) {
          color: var(--accent-cyan);
        }

        .disclaimer {
          font-size: 0.75rem;
          color: var(--text-secondary);
          text-align: center;
          margin-top: 15px;
        }

        .user-profile {
          display: flex;
          align-items: center;
          gap: 12px;
          padding-top: 15px;
          border-top: 1px solid var(--border-color);
        }

        .avatar {
          width: 32px;
          height: 32px;
          background: var(--bg-tertiary);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.8rem;
          font-weight: bold;
        }
      `}</style>
    </div>
  );
}

export default App;
