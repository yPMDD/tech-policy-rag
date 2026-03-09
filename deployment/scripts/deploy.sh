#!/bin/bash
# Tech Policy RAG - Deployment Script

echo "🚀 Starting Deployment..."

# 1. Pull latest code (if in git)
# git pull origin main

# 2. Build and restart containers
echo "📦 Building Docker images..."
docker-compose build

echo "🔄 Restarting services..."
docker-compose up -d

echo "📥 Pulling Llama3 model (this may take a few minutes)..."
docker exec -it tech-policy-rag-ollama-1 ollama pull llama3

echo "✅ Deployment complete! App is running at http://localhost"
