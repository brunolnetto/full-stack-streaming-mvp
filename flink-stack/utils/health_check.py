#!/usr/bin/env python3
"""
Health check script for Flink stack
"""

import os
import requests
import json
from datetime import datetime

def check_flink_ui():
    """Check if Flink UI is accessible"""
    try:
        response = requests.get("http://jobmanager:8081", timeout=5)
        if response.status_code == 200:
            print("✅ Flink UI is accessible")
            return True
        else:
            print(f"❌ Flink UI returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Flink UI check failed: {e}")
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = [
        "POSTGRES_URL",
        "POSTGRES_USER", 
        "POSTGRES_PASSWORD",
        "KAFKA_URL",
        "KAFKA_TOPIC",
        "KAFKA_GROUP"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def check_postgres_connection():
    """Check PostgreSQL connection"""
    try:
        import psycopg2
        
        url = os.environ.get("POSTGRES_URL")
        if not url:
            print("❌ POSTGRES_URL environment variable not set")
            return False
            
        if url.startswith("jdbc:postgresql://"):
            # Convert JDBC URL to psycopg2 format
            url = url.replace("jdbc:postgresql://", "")
            host_port, database = url.split("/")
            host, port = host_port.split(":")
            
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD")
            )
            conn.close()
            print("✅ PostgreSQL connection successful")
            return True
        else:
            print("❌ Invalid PostgreSQL URL format")
            return False
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def check_kafka_connection():
    """Check Kafka connection (basic check)"""
    try:
        # This is a basic check - in a real scenario you'd use kafka-python
        kafka_url = os.environ.get("KAFKA_URL")
        if not kafka_url:
            print("❌ KAFKA_URL environment variable not set")
            return False
        print(f"✅ Kafka URL configured: {kafka_url}")
        return True
    except Exception as e:
        print(f"❌ Kafka configuration check failed: {e}")
        return False

def check_job_files():
    """Check if job files exist"""
    import glob
    from pathlib import Path
    
    src_dir = Path(__file__).parent
    job_files = list(src_dir.glob("*_job.py"))
    
    if job_files:
        print(f"✅ Found {len(job_files)} job files:")
        for job_file in job_files:
            print(f"   - {job_file.name}")
        return True
    else:
        print("❌ No job files found")
        return False

def main():
    """Run all health checks"""
    print("=" * 50)
    print("FLINK STACK HEALTH CHECK")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("Job Files", check_job_files),
        ("Flink UI", check_flink_ui),
        ("PostgreSQL Connection", check_postgres_connection),
        ("Kafka Configuration", check_kafka_connection),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\nChecking {check_name}...")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed with exception: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 50)
    print("HEALTH CHECK SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All health checks passed! Flink stack is ready.")
        return 0
    else:
        print("⚠️  Some health checks failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    exit(main()) 