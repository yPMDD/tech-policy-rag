import React from 'react';
import { BookOpen } from 'lucide-react';

function CitationCard({ citations }) {
  if (!citations) return null;

  return (
    <div className="citation-card glass">
      <div className="card-header">
        <BookOpen size={16} />
        <span>Legal References</span>
      </div>
      <div className="citation-content">
        <p>{citations}</p>
      </div>
      <style jsx>{`
        .citation-card {
          padding: 15px;
          border-radius: 10px;
          max-width: 400px;
          font-size: 0.85rem;
        }

        .card-header {
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 10px;
          color: var(--accent-cyan);
          font-weight: 600;
        }

        .citation-content p {
          color: var(--text-secondary);
          line-height: 1.4;
          white-space: pre-wrap;
        }
      `}</style>
    </div>
  );
}

export default CitationCard;
