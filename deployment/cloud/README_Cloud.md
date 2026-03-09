# Cloud Deployment Guide - Tech Policy RAG

This guide provides instructions for deploying the PolicyLens RAG system to major cloud providers.

## Pre-requisites
1. A virtual machine (VPS) with at least 4GB RAM (needed for SentenceTransformers).
2. Docker and Docker Compose installed.
3. Domain name with A-record pointing to your IP.

## 1. DigitalOcean / AWS EC2 / GCP Compute Engine
The simplest way to deploy is using Docker Compose.

1. **Clone the repository**: `git clone https://github.com/yPMDD/tech-policy-rag.git`
2. **Setup environment**: `bash deployment/scripts/setup.sh`
3. **Configure SSL**: 
   - Install Certbot: `sudo apt install certbot`
   - Use Certbot with Nginx: `certbot --nginx -d yourdomain.com`
4. **Deploy**: `bash deployment/scripts/deploy.sh`
5. **GPU Support**: If your VPS has an NVIDIA GPU, uncomment the `deploy` section in `docker-compose.yml` and ensure `nvidia-container-toolkit` is installed.

## 2. Infrastructure Tuning
- **Vector Store**: For high-availability, consider using a managed Pinecone or Weaviate instance instead of local ChromaDB.
- **Embeddings**: If performance is a bottleneck, offload embedding generation to an external GPU-accelerated microservice or use a cloud API (like OpenAI Ada).

## 3. Environment Variables (Production)
| Variable | Value |
| :--- | :--- |
| `FRONTEND_URL` | `https://yourdomain.com` |
| `DATABASE_URL` | Use a managed Postgres if scaling (RDS, CloudSQL) |
| `JWT_SECRET` | Generate a long random string |
