from flask import Flask, render_template
import redis
import os
import time

app = Flask(__name__)

def get_redis_client():
    """Get Redis client with retry logic"""
    redis_host = os.environ.get('REDIS_HOST', 'redis')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    
    for attempt in range(5):
        try:
            client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
            # Test connection
            client.ping()
            return client
        except redis.ConnectionError:
            print(f"Redis connection attempt {attempt + 1} failed, retrying...")
            time.sleep(2)
    
    raise Exception("Could not connect to Redis after 5 attempts")

# Initialize Redis client
redis_client = get_redis_client()

# Initialize counter if it doesn't exist
if not redis_client.exists('visit_count'):
    redis_client.set('visit_count', 0)

@app.route('/')
def index():
    try:
        # Increment counter
        count = redis_client.incr('visit_count')
        return render_template('index.html', count=count)
    except Exception as e:
        print(f"Error: {e}")
        return f"Error connecting to Redis: {e}", 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        redis_client.ping()
        return "OK", 200
    except Exception as e:
        return f"Redis connection failed: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
