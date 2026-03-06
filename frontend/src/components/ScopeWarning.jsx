import React from 'react';
import { ShieldAlert } from 'lucide-react';

function ScopeWarning({ reason }) {
  if (!reason) return null;

  return (
    <div className="scope-warning-container glass">
      <div className="warning-content">
        <ShieldAlert size={24} className="error-red" />
        <div className="warning-text">
          <h4>Policy Guard Alert</h4>
          <p>{reason}</p>
        </div>
      </div>
      <style jsx>{`
        .scope-warning-container {
          margin: 20px auto;
          max-width: 600px;
          padding: 20px;
          border-left: 4px solid var(--error-red);
          border-radius: 8px;
          background: rgba(255, 77, 77, 0.05);
        }

        .warning-content {
          display: flex;
          align-items: flex-start;
          gap: 20px;
        }

        .warning-text h4 {
          color: var(--error-red);
          margin-bottom: 5px;
          font-family: var(--font-display);
        }

        .warning-text p {
          color: var(--text-secondary);
          font-size: 0.9rem;
          line-height: 1.4;
        }

        .error-red {
          color: var(--error-red);
        }
      `}</style>
    </div>
  );
}

export default ScopeWarning;
