#!/bin/bash
# Tech Policy RAG - Setup Script

echo "🛠️  Setting up environment..."

# 1. Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Creating .env template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your real OAuth credentials!"
fi

# 2. Setup storage permissions
echo "📁 Setting up volumes..."
mkdir -p chromadb_data postgres_data

echo "✨ Setup complete. Run ./deployment/scripts/deploy.sh to start."
