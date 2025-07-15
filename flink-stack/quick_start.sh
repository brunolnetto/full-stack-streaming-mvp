#!/bin/bash

echo "🚀 Starting Flink Stack Quick Start"
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if the network exists
if ! docker network ls | grep -q "livestream-net"; then
    echo "⚠️  Network 'livestream-net' not found. Creating it..."
    docker network create livestream-net
fi

# Start the Flink stack
echo "📦 Starting Flink services..."
docker compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
if docker ps | grep -q "jobmanager" && docker ps | grep -q "taskmanager"; then
    echo "✅ Flink services are running"
else
    echo "❌ Flink services failed to start"
    echo "Check logs with: docker compose logs"
    exit 1
fi

# Run health check
echo "🏥 Running health check..."
docker exec taskmanager python3 /opt/src/health_check.py

echo ""
echo "🎉 Flink Stack is ready!"
echo ""
echo "📋 Next steps:"
echo "1. Access Flink UI: http://localhost:8081"
echo "2. Run a job: docker exec -it taskmanager python3 /opt/src/start_job.py"
echo "3. Generate test data: docker exec -it taskmanager python3 /opt/src/test_data_generator.py"
echo "4. Check logs: docker compose logs"
echo ""
echo "📚 For more information, see README.md" 