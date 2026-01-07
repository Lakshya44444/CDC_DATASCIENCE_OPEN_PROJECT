import os
import time
import requests
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv() # Ensure .env has MAPBOX_TOKEN

# --- CONFIGURATION ---
# POINT THIS TO YOUR RAW TEST FILE
DATA_PATH = r"C:\Users\Lakshya Gupta\Downloads\test2(test(1)).csv"

# UPDATED: Create a 'test' subfolder inside the main image folder
BASE_IMAGE_DIR = "images_mapbox_zoom18"
IMAGE_DIR = os.path.join(BASE_IMAGE_DIR, "test") 

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN") # Or paste string here directly
ZOOM = 18

if not MAPBOX_TOKEN:
    print("❌ Error: MAPBOX_TOKEN not found.")
    exit()

def fetch_test_images():
    # 1. Create the Directory if it doesn't exist
    if not os.path.exists(IMAGE_DIR):
        try:
            os.makedirs(IMAGE_DIR)
            print(f"📁 Created new directory: {IMAGE_DIR}")
        except OSError as e:
            print(f"❌ Error creating directory: {e}")
            return

    print(f"Reading {DATA_PATH}...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"❌ Error: CSV file not found at {DATA_PATH}")
        return

    df['id'] = df['id'].astype(str).replace(r'\.0$', '', regex=True)
    
    # Ensure columns exist
    lon_col = 'long' if 'long' in df.columns else 'lon'
    
    print(f"Checking {len(df)} test properties...")
    
    downloaded = 0
    for index, row in tqdm(df.iterrows(), total=len(df)):
        img_path = os.path.join(IMAGE_DIR, f"{row['id']}.jpg")
        
        # SKIP IF EXISTS (Saves Credits)
        if os.path.exists(img_path):
            continue
            
        # DOWNLOAD
        url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{row[lon_col]},{row['lat']},{ZOOM}/600x600?access_token={MAPBOX_TOKEN}"
        
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(img_path, "wb") as f:
                    f.write(r.content)
                downloaded += 1
                time.sleep(0.05) # Rate limit
            else:
                print(f"Failed {row['id']}: {r.status_code}")
        except Exception as e:
            print(f"Error {row['id']}: {e}")

    print(f"\n✨ Done. Downloaded {downloaded} new images into '{IMAGE_DIR}'.")

if __name__ == "__main__":
    fetch_test_images()