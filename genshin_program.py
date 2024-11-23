import genshin
import asyncio
import json
import csv
import os
from collections import Counter
import matplotlib.pyplot as plt
from colorama import Fore, init
import aiohttp
import time
from pydantic import BaseModel, Field

# Initialize colorama
init(autoreset=True)

# URLs pour Hoyolab, SG Public API et Minor API
base_url_hoyolab = "https://bbs-api-os.hoyolab.com/community/user/wapi/getUserFullInfo?gid=1"
base_url_sg = "https://sg-public-api.hoyolab.com"
base_url_minor = "https://minor-api-os.hoyoverse.com/"

# Function to log messages with different levels
def log_message(message, level="INFO"):
    colors = {
        "INFO": Fore.GREEN,
        "ERROR": Fore.RED,
        "WARNING": Fore.YELLOW,
        "SUCCESS": Fore.GREEN,
        "DEBUG": Fore.CYAN,
    }

    color = colors.get(level, Fore.WHITE)
    print(color + f"[{level}] {message}")

# Export data to JSON file
def export_to_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        log_message(f"Data exported to {filename}", "SUCCESS")
    except Exception as e:
        log_message(f"Error exporting to JSON: {e}", "ERROR")

# Export data to CSV file
def export_to_csv(data, filename, headers):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        log_message(f"Data exported to {filename}", "SUCCESS")
    except Exception as e:
        log_message(f"Error exporting to CSV: {e}", "ERROR")

# Save character data to file
def save_characters(characters):
    character_data = [
        {
            "Name": char.name,
            "Level": char.level,
            "Element": char.element,
            "Rarity": char.rarity,
            "Icon": char.icon,
        }
        for char in characters
    ]
    export_to_json(character_data, "characters.json")
    export_to_csv(character_data, "characters.csv", headers=["Name", "Level", "Element", "Rarity", "Icon"])

# Save wish history to file
def save_wishes(wishes):
    wish_data = [
        {
            "Name": wish.name,
            "Rarity": wish.rarity,
            "Type": wish.type,
            "Date": wish.time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for wish in wishes
    ]
    export_to_json(wish_data, "wishes.json")
    export_to_csv(wish_data, "wishes.csv", headers=["Name", "Rarity", "Type", "Date"])

# Save a user report to file
def save_report(user, wishes):
    report = {
        "Player Name": user.info.nickname,
        "Adventure Level": user.info.level,
        "Region": user.info.region,
        "Number of Characters": len(user.characters),
        "Number of Wishes": len(wishes),
        "Last Daily Reward Claimed": user.daily_reward.claimed,
    }
    export_to_json(report, "user_report.json")

# Analyze wish history
def analyze_wishes(wishes):
    if not wishes:
        log_message("No wishes found. There may be an issue with retrieving the data.", "ERROR")
        return

    rarity_count = Counter(wish.rarity for wish in wishes)
    top_items = Counter(wish.name for wish in wishes).most_common(5)

    log_message("--- Wish History Analysis ---", "SUCCESS")
    log_message(f"Rarity Distribution: {dict(rarity_count)}", "SUCCESS")
    log_message("Top 5 Items Obtained:", "SUCCESS")
    for item, count in top_items:
        log_message(f"{item}: {count} times", "SUCCESS")

# Plot pie chart for rarity distribution
def plot_rarity_distribution(wishes):
    if not wishes:
        log_message("No wishes to generate rarity distribution.", "ERROR")
        return

    rarity_count = Counter(wish.rarity for wish in wishes)
    labels = [f"{key}★" for key in rarity_count.keys()]
    sizes = rarity_count.values()

    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Rarity Distribution in Wishes")
    plt.show()

# Plot bar chart for top 10 most frequent items
def plot_top_items(wishes):
    if not wishes:
        log_message("No wishes to generate the top items chart.", "ERROR")
        return

    top_items = Counter(wish.name for wish in wishes).most_common(10)
    items = [item[0] for item in top_items]
    counts = [item[1] for item in top_items]

    plt.barh(items, counts, color="skyblue")
    plt.xlabel("Number of Occurrences")
    plt.ylabel("Items")
    plt.title("Top 10 Items Obtained")
    plt.gca().invert_yaxis()  # Invert order to have the highest on top
    plt.show()

# Check user data validity
def check_user_validity(user):
    if not user or not user.info:
        log_message("Invalid user data. Stopping process.", "ERROR")
        return False
    return True

# Pydantic models for data validation
class Character(BaseModel):
    id: int
    name: str
    element: str
    rarity: int
    icon: str
    level: int = Field(..., description="Character's level")

class Wish(BaseModel):
    name: str
    rarity: int
    type: str
    time: str  # Will store the datetime as string for simplicity

class UserInfo(BaseModel):
    nickname: str
    level: int
    region: str
    daily_reward_claimed: bool

# Retry mechanism with exponential backoff
async def fetch_with_retry(url, headers, retries=3, delay=2):
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        log_message(f"Failed attempt {attempt+1} for {url}, Status code: {response.status}", "ERROR")
                        raise Exception(f"Request failed with status {response.status}")
        except Exception as e:
            log_message(f"Attempt {attempt+1} failed: {str(e)}", "ERROR")
            if attempt < retries - 1:
                await asyncio.sleep(delay)  # wait before retrying
                delay *= 2  # exponential backoff

    log_message("Max retries reached. Request failed.", "ERROR")
    return None

# Function to send requests to Hoyolab, SG Public API, and Minor API
async def fetch_data_from_apis(uid, ltuid, ltoken):
    headers = {
        "x-rpc-uid": uid,
        "x-rpc-ltuid": ltuid,
        "x-rpc-ltoken": ltoken
    }
    
    hoyolab_url = f"{base_url_hoyolab}/community/user/wapi/getUserFullInfo?gid=2"
    hoyolab_data = await fetch_with_retry(hoyolab_url, headers)
    if hoyolab_data:
        log_message(f"Fetched Hoyolab data successfully: {json.dumps(hoyolab_data, indent=4)}", "SUCCESS")
    
    # Add additional requests as necessary for other APIs

# Main async function
async def main():
    # Request ltuid, ltoken, and UID from user input
    ltuid = input("Enter your ltuid: ")
    ltoken = input("Enter your ltoken: ")
    uid = input("Enter your UID of Genshin Impact: ")

    if not ltuid or not ltoken or not uid:
        log_message("Error: ltuid, ltoken, and UID must be provided!", "ERROR")
        return

    # Process user data and fetch from APIs
    await fetch_data_from_apis(uid, ltuid, ltoken)

# Run the program
if __name__ == "__main__":
    asyncio.run(main())
