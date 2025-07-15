import json
import time
import random
from datetime import datetime, timedelta
import requests

# Sample data for testing
SAMPLE_HOSTS = [
    "example.com",
    "test.com", 
    "demo.org",
    "sample.net"
]

SAMPLE_URLS = [
    "/home",
    "/about",
    "/contact",
    "/products",
    "/services",
    "/blog",
    "/api/users",
    "/api/posts"
]

SAMPLE_REFERRERS = [
    "https://google.com",
    "https://bing.com",
    "https://facebook.com",
    "https://twitter.com",
    "https://linkedin.com",
    ""
]

SAMPLE_IPS = [
    "192.168.1.1",
    "10.0.0.1",
    "172.16.0.1",
    "8.8.8.8",
    "1.1.1.1"
]

def generate_sample_event():
    """Generate a sample web traffic event"""
    now = datetime.now()
    event_time = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    return {
        "url": random.choice(SAMPLE_URLS),
        "referrer": random.choice(SAMPLE_REFERRERS),
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "host": random.choice(SAMPLE_HOSTS),
        "ip": random.choice(SAMPLE_IPS),
        "headers": json.dumps({"User-Agent": "test-agent"}),
        "event_time": event_time
    }

def send_to_kafka(event_data):
    """Send event data to Kafka topic"""
    try:
        # This would normally send to Kafka, but for testing we'll just print
        print(f"Generated event: {json.dumps(event_data, indent=2)}")
        return True
    except Exception as e:
        print(f"Error sending to Kafka: {e}")
        return False

def generate_test_data(num_events=10, delay_seconds=1):
    """Generate test data for Flink jobs"""
    print(f"Generating {num_events} test events...")
    
    for i in range(num_events):
        event = generate_sample_event()
        success = send_to_kafka(event)
        
        if success:
            print(f"Event {i+1}/{num_events} generated successfully")
        
        if i < num_events - 1:  # Don't sleep after the last event
            time.sleep(delay_seconds)

if __name__ == "__main__":
    print("Starting test data generator...")
    generate_test_data(num_events=5, delay_seconds=2)
    print("Test data generation complete!") 