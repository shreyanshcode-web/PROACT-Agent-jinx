# Multi-stage Dockerfile for Jinx backend + React frontend

# ---------- Builder stage ----------
FROM node:20-alpine AS builder

# Set working directory for frontend
WORKDIR /frontend

# Copy package.json and lockfile
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci

# Copy the rest of the frontend source
COPY frontend/ .

# Build the React app
RUN npm run build

# ---------- Runtime stage ----------
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory for backend
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy backend source code
COPY . .

# Copy built frontend assets from builder stage
COPY --from=builder /frontend/dist ./frontend/dist

# Create log directory
RUN mkdir -p log

# Expose port (if backend serves on 8000)
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["python", "jinx.py"]
