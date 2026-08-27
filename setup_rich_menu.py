"""
Script to create, upload image, and set default LINE Rich Menu for Starbug Assistant.
Usage: python setup_rich_menu.py
"""
import os
import sys
import json
import requests

from config import LINE_CHANNEL_ACCESS_TOKEN
from line_ui.rich_menu import generate_rich_menu_image, get_rich_menu_payload, RICH_MENU_IMG_PATH

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def setup_rich_menu():
    print("============================================================")
    print("  STARBUG THAILAND - LINE RICH MENU AUTO SETUP")
    print("============================================================")

    if not LINE_CHANNEL_ACCESS_TOKEN:
        print("[ERROR] LINE_CHANNEL_ACCESS_TOKEN is missing in .env")
        return False

    headers_json = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # 1. Generate Rich Menu Image (2500x1686)
    print("[1/4] Generating 2500x1686 Rich Menu Image...")
    img_path = generate_rich_menu_image(RICH_MENU_IMG_PATH)
    print(f"      Image saved at: {img_path}")

    # 2. Create Rich Menu Object on LINE Platform
    print("[2/4] Registering Rich Menu Schema with LINE Messaging API...")
    payload = get_rich_menu_payload()
    res = requests.post("https://api.line.me/v2/bot/richmenu", headers=headers_json, json=payload)
    
    if res.status_code != 200:
        print(f"[ERROR] Failed to create rich menu: {res.status_code} -> {res.text}")
        return False

    rich_menu_id = res.json().get("richMenuId")
    print(f"      Created Rich Menu ID: {rich_menu_id}")

    # 3. Upload Image to the created Rich Menu
    print("[3/4] Uploading Rich Menu Image to LINE CDN...")
    headers_img = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "image/png"
    }
    with open(img_path, "rb") as f:
        img_data = f.read()

    upload_url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"
    res_upload = requests.post(upload_url, headers=headers_img, data=img_data)
    if res_upload.status_code != 200:
        print(f"[ERROR] Failed to upload image: {res_upload.status_code} -> {res_upload.text}")
        return False
    print("      Image uploaded successfully!")

    # 4. Set as Default Rich Menu for all users
    print("[4/4] Activating as Default Rich Menu for all chat users...")
    default_url = f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}"
    res_default = requests.post(default_url, headers=headers_json)
    if res_default.status_code != 200:
        print(f"[ERROR] Failed to set default rich menu: {res_default.status_code} -> {res_default.text}")
        return False

    print("\n🎉 SUCCESS! Starbug Rich Menu is now ACTIVE on your LINE Official Account!")
    print(f"   Rich Menu ID: {rich_menu_id}")
    print("   Users can now tap the 6 menu buttons at the bottom of the chat anytime!")
    return True


if __name__ == "__main__":
    setup_rich_menu()
