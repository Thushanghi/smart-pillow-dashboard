import asyncio
import random
import time
from datetime import datetime
import httpx
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://fwmzofkktwsctcgkrpcg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3bXpvZmtrdHdzY3RjZ2tycGNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzMzk3MzQsImV4cCI6MjA3NzkxNTczNH0.Ch6zMq40cuUdWZ00H3JUb_gq4iHVoiTcCQBNKpWpqro"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Device ID (you can change or randomize this)
DEVICE_ID = "sensor_device_001"

# Realistic value ranges
FSR_MIN, FSR_MAX = 0, 1023
PIEZO_MIN, PIEZO_MAX = 0, 1023
TEMP_MIN, TEMP_MAX = 15.0, 40.0
IR_MIN, IR_MAX = 0, 100000

async def generate_and_insert():
    """Generate a single random row and insert into Supabase"""
    data = {
        "device_id": DEVICE_ID,
        "fsr_value": random.randint(FSR_MIN, FSR_MAX),
        "piezo_value": random.randint(PIEZO_MIN, PIEZO_MAX),
        "object_temperature": round(random.uniform(TEMP_MIN, TEMP_MAX), 2),
        "ambient_temperature": round(random.uniform(TEMP_MIN, TEMP_MAX), 2),
        "ir_value": random.randint(IR_MIN, IR_MAX),
        "device_timestamp": int(time.time() * 1000)  # milliseconds
    }

    try:
        response = supabase.table("sensor_readings").insert(data).execute()
        if response.data:
            print(f"Inserted: {data['device_timestamp']}")
        else:
            print(f"Error: {response}")
    except Exception as e:
        print(f"Exception: {e}")

async def main():
    """Send 10 rows per second"""
    print("Starting data generator: 10 inserts/second...")
    while True:
        start_time = time.time()

        # Fire 10 async inserts
        tasks = [generate_and_insert() for _ in range(10)]
        await asyncio.gather(*tasks)

        # Sleep to maintain ~10 inserts per second
        elapsed = time.time() - start_time
        sleep_time = max(0, 1.0 - elapsed)
        await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user.")