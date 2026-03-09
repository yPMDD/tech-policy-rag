import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Plus, History, ShieldAlert, LogIn, ExternalLink, ChevronRight, LogOut, Github, Chrome } from 'lucide-react';
import ChatWindow from './components/ChatWindow';

// API Base configuration
const API_BASE = "http://localhost:8001";

const GoogleIcon = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.66l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
  </svg>
);

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [conversations, setConversations] = useState([]);
  const [currentConvId, setCurrentConvId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);

  // Configure axios with token
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchConversations();
      fetchUserProfile();
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const fetchUserProfile = async () => {
    try {
      console.log("Fetching user profile...");
      const res = await axios.get(`${API_BASE}/auth/me`);
      console.log("Profile received:", res.data);
      setUser(res.data);
    } catch (err) {
      console.error("Error fetching user profile:", err.response?.data || err.message);
    }
  };

  // Handle OAuth Callback
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = urlParams.get('token');
    if (tokenFromUrl) {
      localStorage.setItem('token', tokenFromUrl);
      setToken(tokenFromUrl);
      // Clean URL
      window.history.replaceState({}, document.title, "/");
    }
  }, []);

  // Handle OAuth Callback
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = urlParams.get('token');
    if (tokenFromUrl) {
      localStorage.setItem('token', tokenFromUrl);
      setToken(tokenFromUrl);
      // Clean URL
      window.history.replaceState({}, document.title, "/");
    }
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/conversations`);
      setConversations(res.data);
    } catch (err) {
      console.error("Error fetching conversations:", err);
      if (err.response?.status === 401) handleLogout();
    }
  };

  const loadHistory = async (convId) => {
    setCurrentConvId(convId);
    try {
      const res = await axios.get(`${API_BASE}/api/conversations/${convId}/history`);
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
      const res = await axios.post(`${API_BASE}/api/chat`, {
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
        content: "I'm sorry, I encountered an error connecting to the legal engine." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setMessages([]);
    setConversations([]);
    setCurrentConvId(null);
  };

  const handleLogin = (provider) => {
    window.location.href = `${API_BASE}/auth/login/${provider}`;
  };

  if (!token) {
    return (
      <div className="login-container">
        <div className="login-card glass">
          <ShieldAlert size={48} className="cyan-glow" style={{marginBottom: '20px'}} />
          <h1 className="cyan-glow">PolicyLens <span style={{color: '#fff'}}>Auth</span></h1>
          <p className="text-secondary">Secure access to EU Tech Policy Intelligence</p>
          
          <div className="login-buttons">
            <button className="auth-btn github" onClick={() => handleLogin('github')}>
              <Github size={20} /> Login with GitHub
            </button>
            <button className="auth-btn google" onClick={() => handleLogin('google')}>
              <GoogleIcon size={20} /> Login with Google
            </button>
          </div>
          
          <p className="footer-note">By logging in, you agree to our Terms of Service.</p>
        </div>
        <style jsx>{`
          .login-container {
            height: 100vh;
            width: 100vw;
            display: flex;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle at center, #1a1a1a 0%, #0d0d0d 100%);
          }
          .login-card {
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
          }
          .login-buttons {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: 30px;
          }
          .auth-btn {
            padding: 12px;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            background: var(--bg-secondary);
            color: white;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            cursor: pointer;
            transition: var(--transition);
          }
          .auth-btn:hover {
            background: var(--bg-tertiary);
            border-color: var(--accent-cyan);
            box-shadow: 0 0 10px var(--accent-cyan-dim);
          }
          .footer-note {
            margin-top: 25px;
            font-size: 0.75rem;
            color: var(--text-secondary);
          }
        `}</style>
      </div>
    );
  }

  return (
    <div className="app-container">
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
          {user && (
            <div className="user-info-display">
              <div className="avatar">
                {user.oauth_provider === 'github' ? <Github size={18} /> : <GoogleIcon size={18} />}
              </div>
              <div className="user-details">
                <span className="username">{user.username || user.full_name}</span>
                <span className="user-email">{user.email}</span>
              </div>
            </div>
          )}
          <div className="user-profile" onClick={handleLogout} style={{cursor: 'pointer'}}>
            <LogOut size={18} className="text-secondary" />
            <span>Sign Out</span>
          </div>
        </div>
      </aside>

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

        .user-info-display {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 10px;
          margin-bottom: 10px;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 12px;
          border: 1px solid var(--border-color);
        }

        .user-details {
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        .username {
          font-size: 0.9rem;
          font-weight: 600;
          color: white;
          white-space: nowrap;
          text-overflow: ellipsis;
          overflow: hidden;
        }

        .user-email {
          font-size: 0.7rem;
          color: var(--text-secondary);
          white-space: nowrap;
          text-overflow: ellipsis;
          overflow: hidden;
        }

        .avatar {
          width: 36px;
          height: 36px;
          background: var(--bg-tertiary);
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.8rem;
          font-weight: bold;
          color: var(--accent-cyan);
          border: 1px solid var(--accent-cyan-dim);
          flex-shrink: 0;
        }
      `}</style>
    </div>
  );
}

export default App;
