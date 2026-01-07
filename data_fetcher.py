import os
import time
import json
import requests
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# --- SAFETY CONFIGURATION ---
# Mapbox Free Tier: 50,000 requests/month
MONTHLY_LIMIT = 50000       
SAFETY_BUFFER = 2000        
MAX_ALLOWED_REQUESTS = MONTHLY_LIMIT - SAFETY_BUFFER

USAGE_FILE = "mapbox_usage_log.json"

# UPDATED: Using raw string for Windows path and new Zoom Level
DATA_PATH = r"C:\Users\Lakshya Gupta\Downloads\train(1)(train(1)).csv"
IMAGE_DIR = "images_mapbox_zoom18"  # New folder for Zoom 18 images
ZOOM = 18                           # The "Sweet Spot" zoom level

# --- MAPBOX SPECIFIC SETTINGS ---
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN") 
STYLE_ID = "mapbox/satellite-v9" 
WIDTH = 600
HEIGHT = 600

if not MAPBOX_TOKEN:
    raise ValueError("MAPBOX_TOKEN NOT FOUND. Please add it to your .env file.")

def get_current_usage():
    """Reads the total usage from a local file."""
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            return json.load(f).get("count", 0)
    return 0

def update_usage(count):
    """Updates the usage count in the local file."""
    with open(USAGE_FILE, "w") as f:
        json.dump({"count": count}, f)

def build_mapbox_url(lat, lon):
    """
    Constructs the Mapbox Static Image URL.
    """
    base_url = "https://api.mapbox.com/styles/v1"
    return f"{base_url}/{STYLE_ID}/static/{lon},{lat},{ZOOM}/{WIDTH}x{HEIGHT}?access_token={MAPBOX_TOKEN}"

def fetch_image(lat, lon, property_id):
    image_path = os.path.join(IMAGE_DIR, f"{property_id}.jpg")

    # 1. DISK CHECK
    if os.path.exists(image_path):
        return "skipped"

    url = build_mapbox_url(lat, lon)

    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code in [403, 429]:
            print(f"\n[STOP] API Error: {response.status_code}. Checking quota or token.")
            return "stop"
        
        response.raise_for_status()

        with open(image_path, "wb") as f:
            f.write(response.content)
            
        return "downloaded"

    except Exception as e:
        print(f"[ERROR] ID {property_id}: {e}")
        return "error"

def fetch_all_images():
    # Create the specific folder for Zoom 18
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print(f"Created new directory: {IMAGE_DIR}")
    
    print(f"Loading Dataset from: {DATA_PATH}")
    try:
        # Check file extension to use correct loader
        if DATA_PATH.endswith('.xlsx'):
            df = pd.read_excel(DATA_PATH)
        else:
            df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print("Error: File not found. Check the path.")
        return

    # Clean ID column
    df['id'] = df['id'].astype(str).replace(r'\.0$', '', regex=True)
    
    # Check Usage
    total_api_calls = get_current_usage()
    print(f"Previous Mapbox Usage: {total_api_calls}")
    
    if total_api_calls >= MAX_ALLOWED_REQUESTS:
        print("Limit reached! Reset 'mapbox_usage_log.json' if this is a new month.")
        return

    print(f"Processing {len(df)} locations at Zoom {ZOOM}...")

    for index, row in tqdm(df.iterrows(), total=len(df)):
        
        if total_api_calls >= MAX_ALLOWED_REQUESTS:
            print(f"\n[SAFETY STOP] Limit reached.")
            break
            
        # Flexible column name check (long vs lon)
        lon_col = 'long' if 'long' in df.columns else 'lon'
        if 'longitude' in df.columns: lon_col = 'longitude'

        status = fetch_image(
            lat=row['lat'],
            lon=row[lon_col], 
            property_id=row['id']
        )
        
        if status == "stop":
            break
        elif status == "downloaded":
            total_api_calls += 1
            if total_api_calls % 10 == 0:
                update_usage(total_api_calls)
            time.sleep(0.05) 

    update_usage(total_api_calls)
    print(f"\nBatch finished. Images saved to /{IMAGE_DIR}")

if __name__ == "__main__":
    fetch_all_images()