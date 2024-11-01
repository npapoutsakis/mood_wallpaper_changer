import requests
import os
from datetime import datetime
from PIL import Image
from io import BytesIO
import subprocess

# Constants
FACT_API_URL = "https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/"
IMAGE_API_URL = "https://api.unsplash.com/photos/random"
IMAGE_API_KEY = "--------"  # Replace with your Unsplash API Key
WALLPAPER_PATH = os.path.join(os.path.expanduser("~"), "daily_wallpaper.jpg")

def get_daily_fact():
    today = datetime.now().strftime("%m/%d")
    response = requests.get(f"{FACT_API_URL}{today}")
    if response.status_code == 200:
        data = response.json()
        if data["selected"] and data["selected"][0]["text"]:
            fact = data["selected"][0]["text"]
            return fact
    return "Fun fact of the day!"

def search_image(fact):
    headers = {"Authorization": f"Client-ID {IMAGE_API_KEY}"}
    params = {"query": fact, "orientation": "landscape"}
    response = requests.get(IMAGE_API_URL, headers=headers, params=params)
    if response.status_code == 200:
        img_url = response.json()["urls"]["full"]
        return img_url
    return None

def set_wallpaper(image_path):
    # Convert the path to a file URI format
    file_uri = f"file://{image_path}"
    
    # Set wallpaper for both dark mode and light mode on GNOME
    subprocess.run(["dconf", "write", "/org/gnome/desktop/background/picture-uri-dark", f"'{file_uri}'"])
    subprocess.run(["dconf", "write", "/org/gnome/desktop/background/picture-uri", f"'{file_uri}'"])

def main():
    fact = get_daily_fact()
    print(f"Today's Fact: {fact}")
    
    img_url = search_image(fact)
    if img_url:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        img.save(WALLPAPER_PATH)
        
        set_wallpaper(WALLPAPER_PATH)
        print("Wallpaper updated successfully!")
    else:
        print("Couldn't find a relevant image.")

if __name__ == "__main__":
    main()
