#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seed script to populate 50 more spots across Europe and North Africa."""

import os
import requests

API_URL = "http://localhost:8000/api"
IMAGES_DIR = "/Users/bodda/Desktop/spotdrop-images"

EMAIL = "abdallah@gmail.com"
PASSWORD = "pass@1234"

# 50 new spots in cities not covered before
# Avoiding: Cairo, Dubai, Venice/Florence/Rome, Barcelona/Madrid, Stockholm,
# Zurich/Interlaken, Paris, Istanbul, Athens/Santorini, Tehran, Moscow,
# Berlin/Munich, Algiers, Fez/Marrakech

SPOTS_DATA = [
    # Portugal (3 spots)
    ("Time Out Market", "Vibrant food hall in a historic market building", "restaurant", 38.7069, -9.1456, "Lisbon, Portugal", "Seafood selection", "Lunch", 2, 4.5),
    ("Livraria Lello", "Stunning neo-Gothic bookshop that inspired Harry Potter", "shop", 41.1469, -8.6148, "Porto, Portugal", "Architecture", "Morning", 2, 4.6),
    ("Miradouro da Senhora do Monte", "Highest viewpoint in Lisbon with panoramic views", "viewpoint", 38.7196, -9.1332, "Lisbon, Portugal", "Sunset views", "Evening", 1, 4.7),

    # Netherlands (3 spots)
    ("Cafe de Klos", "Famous spare ribs restaurant in Amsterdam", "restaurant", 52.3651, 4.8828, "Amsterdam, Netherlands", "Spare ribs", "Dinner", 2, 4.4),
    ("A'DAM Lookout", "Observation deck with swing over Amsterdam", "viewpoint", 52.3843, 4.9016, "Amsterdam, Netherlands", "Over the Edge swing", "Afternoon", 3, 4.5),
    ("Wynand Fockink", "Historic tasting room for Dutch jenever since 1679", "bar", 52.3728, 4.8963, "Amsterdam, Netherlands", "Jenever tasting", "Evening", 2, 4.6),

    # Belgium (3 spots)
    ("Delirium Cafe", "World record holder for most beers on menu", "bar", 50.8484, 4.3538, "Brussels, Belgium", "Belgian ales", "Night", 2, 4.5),
    ("De Halve Maan Brewery", "Historic brewery with rooftop views of Bruges", "activity", 51.2044, 3.2247, "Bruges, Belgium", "Beer tasting tour", "Afternoon", 2, 4.6),
    ("Chocolatier Mary", "Royal warrant chocolatier since 1919", "shop", 50.8467, 4.3571, "Brussels, Belgium", "Pralines", "Morning", 3, 4.4),

    # Austria (3 spots)
    ("Cafe Central", "Grand Viennese coffeehouse since 1876", "cafe", 48.2106, 16.3656, "Vienna, Austria", "Apfelstrudel", "Afternoon", 3, 4.6),
    ("Stiftskeller St. Peter", "Europe's oldest restaurant dating to 803 AD", "restaurant", 47.7975, 13.0450, "Salzburg, Austria", "Traditional Austrian", "Dinner", 3, 4.5),
    ("Schonbrunn Palace Gardens", "Imperial palace gardens with city views", "viewpoint", 48.1846, 16.3122, "Vienna, Austria", "Gloriette views", "Morning", 2, 4.7),

    # Czech Republic (3 spots)
    ("Cafe Louvre", "Historic Prague cafe frequented by Einstein and Kafka", "cafe", 50.0819, 14.4183, "Prague, Czech Republic", "Czech pastries", "Morning", 2, 4.4),
    ("Letna Beer Garden", "Hillside beer garden with Prague panorama", "bar", 50.0963, 14.4194, "Prague, Czech Republic", "Czech lager", "Evening", 1, 4.6),
    ("Prague Astronomical Clock", "Medieval clock tower in Old Town Square", "viewpoint", 50.0870, 14.4208, "Prague, Czech Republic", "Hourly show", "Any time", 1, 4.5),

    # Poland (3 spots)
    ("Starka Restaurant", "Traditional Polish cuisine in Krakow's Jewish Quarter", "restaurant", 50.0517, 19.9461, "Krakow, Poland", "Pierogi", "Dinner", 2, 4.5),
    ("St. Mary's Basilica Tower", "Gothic church tower with city views", "viewpoint", 50.0617, 19.9392, "Krakow, Poland", "Old Town panorama", "Morning", 2, 4.6),
    ("E.Wedel Chocolate Lounge", "Historic Polish chocolate house since 1851", "cafe", 52.2319, 21.0178, "Warsaw, Poland", "Hot chocolate", "Afternoon", 2, 4.4),

    # Hungary (3 spots)
    ("Szimpla Kert", "Original ruin bar in Budapest's Jewish Quarter", "bar", 47.4965, 19.0654, "Budapest, Hungary", "Craft cocktails", "Night", 2, 4.5),
    ("New York Cafe", "Opulent 19th-century cafe called most beautiful in world", "cafe", 47.4965, 19.0731, "Budapest, Hungary", "Cake selection", "Afternoon", 4, 4.7),
    ("Fisherman's Bastion", "Neo-Gothic terrace with Danube and Parliament views", "viewpoint", 47.5019, 19.0344, "Budapest, Hungary", "Sunset panorama", "Evening", 2, 4.8),

    # Croatia (3 spots)
    ("Buza Bar", "Cliffside bar with Adriatic Sea views", "bar", 42.6394, 18.1075, "Dubrovnik, Croatia", "Sunset drinks", "Evening", 2, 4.7),
    ("Diocletian's Palace Cellars", "Ancient Roman underground market", "shop", 43.5082, 16.4402, "Split, Croatia", "Local crafts", "Morning", 1, 4.4),
    ("Mount Srd Cable Car", "Panoramic views over Dubrovnik and islands", "viewpoint", 42.6508, 18.1064, "Dubrovnik, Croatia", "Sunset views", "Evening", 2, 4.6),

    # Denmark (2 spots)
    ("Nyhavn Waterfront", "Colorful harbor district with outdoor cafes", "cafe", 55.6797, 12.5897, "Copenhagen, Denmark", "Danish pastries", "Morning", 2, 4.5),
    ("Tivoli Gardens", "Historic amusement park in city center", "activity", 55.6738, 12.5681, "Copenhagen, Denmark", "Evening lights", "Night", 3, 4.6),

    # Norway (2 spots)
    ("Floyen Mountain", "Funicular viewpoint over Bergen", "viewpoint", 60.3960, 5.3434, "Bergen, Norway", "Fjord views", "Afternoon", 2, 4.7),
    ("Mathallen Oslo", "Indoor food hall with Nordic cuisine", "restaurant", 59.9225, 10.7522, "Oslo, Norway", "Seafood dishes", "Lunch", 3, 4.4),

    # Finland (2 spots)
    ("Cafe Regatta", "Cozy red cottage cafe by the sea", "cafe", 60.1756, 24.9050, "Helsinki, Finland", "Cinnamon buns", "Afternoon", 1, 4.6),
    ("Loyly Sauna", "Public sauna with sea swimming and restaurant", "activity", 60.1530, 24.9156, "Helsinki, Finland", "Sauna experience", "Evening", 3, 4.5),

    # Ireland (2 spots)
    ("Temple Bar District", "Iconic Dublin pub area", "bar", 53.3454, -6.2644, "Dublin, Ireland", "Guinness", "Night", 2, 4.3),
    ("Grafton Street Shopping", "Premier shopping street with buskers", "shop", 53.3418, -6.2597, "Dublin, Ireland", "Irish crafts", "Afternoon", 3, 4.4),

    # Scotland (2 spots)
    ("Arthur's Seat Summit", "Ancient volcano with Edinburgh panorama", "viewpoint", 55.9443, -3.1618, "Edinburgh, Scotland", "City views", "Morning", 1, 4.7),
    ("The Witchery Restaurant", "Gothic dining near Edinburgh Castle", "restaurant", 55.9489, -3.1958, "Edinburgh, Scotland", "Scottish cuisine", "Dinner", 4, 4.5),

    # UK - London (2 spots)
    ("Sky Garden", "Free public garden with London skyline views", "viewpoint", 51.5113, -0.0836, "London, UK", "City panorama", "Sunset", 1, 4.5),
    ("Borough Market", "Historic food market under railway arches", "shop", 51.5055, -0.0910, "London, UK", "Artisan foods", "Morning", 2, 4.6),

    # Slovenia (2 spots)
    ("Ljubljana Castle", "Hilltop fortress with old town views", "viewpoint", 46.0489, 14.5083, "Ljubljana, Slovenia", "Dragon views", "Afternoon", 2, 4.5),
    ("Open Kitchen Market", "Weekly street food market in city center", "restaurant", 46.0512, 14.5064, "Ljubljana, Slovenia", "Local dishes", "Friday lunch", 2, 4.4),

    # Montenegro (1 spot)
    ("Kotor Old Town", "Medieval walled town on the Adriatic", "activity", 42.4247, 18.7712, "Kotor, Montenegro", "Walking tour", "Morning", 1, 4.7),

    # Tunisia (3 spots)
    ("Cafe des Nattes", "Traditional cafe in the blue village of Sidi Bou Said", "cafe", 36.8689, 10.3417, "Sidi Bou Said, Tunisia", "Mint tea", "Afternoon", 1, 4.5),
    ("Carthage Ruins", "Ancient Phoenician city archaeological site", "viewpoint", 36.8528, 10.3233, "Carthage, Tunisia", "Roman ruins", "Morning", 2, 4.6),
    ("Medina of Tunis", "UNESCO World Heritage souk", "shop", 36.7992, 10.1706, "Tunis, Tunisia", "Carpets and ceramics", "Morning", 1, 4.4),

    # Morocco - new cities (3 spots)
    ("Rick's Cafe", "Casablanca cafe inspired by the classic film", "cafe", 33.5981, -7.6114, "Casablanca, Morocco", "Atmosphere", "Evening", 3, 4.3),
    ("Chefchaouen Blue Medina", "Famous blue-painted mountain town", "viewpoint", 35.1714, -5.2636, "Chefchaouen, Morocco", "Blue streets", "Any time", 1, 4.8),
    ("Tangier Kasbah", "Historic fortress with strait views", "activity", 35.7875, -5.8131, "Tangier, Morocco", "Strait of Gibraltar", "Afternoon", 1, 4.5),

    # Egypt - new cities (3 spots)
    ("Alexandria Library", "Modern library on ancient library site", "activity", 31.2089, 29.9092, "Alexandria, Egypt", "Architecture", "Morning", 1, 4.5),
    ("Luxor Temple at Night", "Ancient temple illuminated after dark", "viewpoint", 25.6997, 32.6390, "Luxor, Egypt", "Night illumination", "Evening", 2, 4.7),
    ("Nubian Village", "Traditional colorful village near Aswan", "activity", 24.0908, 32.8994, "Aswan, Egypt", "Cultural experience", "Afternoon", 1, 4.6),

    # Malta (1 spot)
    ("Valletta Waterfront", "Historic harbor promenade with restaurants", "restaurant", 35.8933, 14.5147, "Valletta, Malta", "Seafood", "Dinner", 3, 4.4),
]


def login() -> str:
    response = requests.post(
        f"{API_URL}/auth/login",
        json={"email": EMAIL, "password": PASSWORD}
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_spot(token: str, spot_data: dict) -> dict:
    response = requests.post(
        f"{API_URL}/spots",
        json=spot_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()


def upload_image(token: str, spot_id: int, image_path: str) -> dict:
    with open(image_path, "rb") as f:
        response = requests.post(
            f"{API_URL}/spots/{spot_id}/images",
            files={"file": (os.path.basename(image_path), f, "image/jpeg")},
            data={"is_primary": "true"},
            headers={"Authorization": f"Bearer {token}"}
        )
    response.raise_for_status()
    return response.json()


def main():
    print("Logging in...")
    token = login()
    print("Logged in successfully!")

    print(f"\nCreating {len(SPOTS_DATA)} new spots...")

    for i, (title, description, category, lat, lng, address, best, best_time, price_level, rating) in enumerate(SPOTS_DATA, 1):
        spot_data = {
            "title": title,
            "description": description,
            "category": category,
            "latitude": lat,
            "longitude": lng,
            "address": address,
            "best": best,
            "best_time": best_time,
            "price_level": price_level,
            "rating": rating,
        }

        try:
            spot = create_spot(token, spot_data)
            spot_id = spot["id"]

            image_path = os.path.join(IMAGES_DIR, f"{category}.jpeg")
            if os.path.exists(image_path):
                upload_image(token, spot_id, image_path)
                print(f"[{i}/{len(SPOTS_DATA)}] Created: {title} ({category})")
            else:
                print(f"[{i}/{len(SPOTS_DATA)}] Created: {title} ({category}) - no image")

        except Exception as e:
            print(f"[{i}/{len(SPOTS_DATA)}] Failed: {title} - {e}")

    print("\nDone! All spots created.")


if __name__ == "__main__":
    main()
