#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seed script to populate 50 spots across various countries."""

import os
import random
import requests

API_URL = "http://localhost:8000/api"
IMAGES_DIR = "/Users/bodda/Desktop/spotdrop-images"

# Login credentials
EMAIL = "abdallah@gmail.com"
PASSWORD = "pass@1234"

# Categories matching the web app
CATEGORIES = ["cafe", "viewpoint", "activity", "shop", "bar", "restaurant"]

# Spots data: 50 places across specified countries
# Format: (title, description, category, lat, lng, country, best, best_time, price_level, rating)
SPOTS_DATA = [
    # Egypt (4 spots)
    ("Cafe Riche", "Historic cafe in downtown Cairo, serving traditional Egyptian coffee since 1908", "cafe", 30.0444, 31.2357, "Egypt", "Turkish Coffee", "Morning", 2, 4.3),
    ("Pyramids of Giza Viewpoint", "Iconic view of the ancient pyramids from the Giza plateau", "viewpoint", 29.9792, 31.1342, "Egypt", "Sunrise photos", "Early morning", 1, 4.9),
    ("Khan el-Khalili Bazaar", "Historic bazaar with traditional crafts and souvenirs", "shop", 30.0477, 31.2625, "Egypt", "Handmade jewelry", "Afternoon", 2, 4.2),
    ("Nile Felucca Ride", "Traditional sailboat experience on the Nile River", "activity", 30.0561, 31.2243, "Egypt", "Sunset cruise", "Evening", 2, 4.5),

    # UAE (4 spots)
    ("Arabian Tea House", "Traditional Emirati cafe in Al Fahidi historic district", "cafe", 25.2637, 55.2972, "UAE", "Karak chai", "Afternoon", 2, 4.4),
    ("Burj Khalifa Observation Deck", "World's tallest building with panoramic city views", "viewpoint", 25.1972, 55.2744, "UAE", "Night views", "Sunset", 4, 4.8),
    ("Dubai Mall", "One of the world's largest shopping destinations", "shop", 25.1985, 55.2796, "UAE", "Luxury brands", "Evening", 4, 4.3),
    ("Level 43 Sky Lounge", "Rooftop bar with stunning Dubai Marina views", "bar", 25.0762, 55.1332, "UAE", "Signature cocktails", "Night", 4, 4.5),

    # Italy (4 spots)
    ("Caffe Florian", "Historic cafe in Venice's St. Mark's Square since 1720", "cafe", 45.4341, 12.3388, "Italy", "Espresso", "Morning", 4, 4.6),
    ("Piazzale Michelangelo", "Panoramic viewpoint overlooking Florence", "viewpoint", 43.7629, 11.2650, "Italy", "Sunset views", "Evening", 1, 4.7),
    ("Trattoria da Enzo", "Authentic Roman cuisine in Trastevere", "restaurant", 41.8879, 12.4699, "Italy", "Cacio e Pepe", "Dinner", 2, 4.5),
    ("Libreria Acqua Alta", "Unique bookshop in Venice with books in bathtubs and boats", "shop", 45.4385, 12.3456, "Italy", "Rare books", "Afternoon", 2, 4.4),

    # Spain (4 spots)
    ("El Nacional Barcelona", "Stunning food hall in a converted parking garage", "restaurant", 41.3925, 2.1700, "Spain", "Tapas selection", "Evening", 3, 4.4),
    ("Park Guell Viewpoint", "Gaudi's colorful park with city views", "viewpoint", 41.4145, 2.1527, "Spain", "Mosaic art", "Morning", 2, 4.6),
    ("Mercado de San Miguel", "Historic glass market with gourmet Spanish food", "shop", 40.4154, -3.7090, "Spain", "Iberian ham", "Afternoon", 3, 4.3),
    ("El Xampanyet", "Traditional cava bar in Barcelona's El Born", "bar", 41.3847, 2.1828, "Spain", "Cava and anchovies", "Evening", 2, 4.5),

    # Sweden (4 spots)
    ("Fotografiska Cafe", "Cafe in Stockholm's famous photography museum", "cafe", 59.3178, 18.0856, "Sweden", "Kanelbullar", "Afternoon", 3, 4.3),
    ("Skinnarviksberget", "Rocky hill with the best sunset views over Stockholm", "viewpoint", 59.3186, 18.0503, "Sweden", "Sunset picnic", "Evening", 1, 4.7),
    ("Sturehof", "Classic Swedish seafood restaurant since 1897", "restaurant", 59.3358, 18.0756, "Sweden", "Toast Skagen", "Dinner", 4, 4.4),
    ("Kayaking Stockholm Archipelago", "Paddle through Stockholm's beautiful islands", "activity", 59.3500, 18.1200, "Sweden", "Island hopping", "Summer morning", 3, 4.6),

    # Switzerland (4 spots)
    ("Sprungli Confiserie", "Legendary Swiss chocolate and cafe in Zurich", "cafe", 47.3696, 8.5392, "Switzerland", "Luxemburgerli", "Morning", 4, 4.7),
    ("Harder Kulm", "Mountain viewpoint above Interlaken with Alpine panorama", "viewpoint", 46.6986, 7.8500, "Switzerland", "Alpine sunset", "Evening", 2, 4.8),
    ("Zeughauskeller", "Historic beer hall in Zurich's old town", "bar", 47.3722, 8.5389, "Switzerland", "Local beer", "Evening", 3, 4.3),
    ("Swiss Knife Shop Interlaken", "Premium Swiss army knives and watches", "shop", 46.6863, 7.8632, "Switzerland", "Custom knives", "Afternoon", 4, 4.4),

    # France (4 spots)
    ("Cafe de Flore", "Iconic Parisian cafe frequented by artists and writers", "cafe", 48.8540, 2.3325, "France", "Cafe Creme", "Morning", 4, 4.5),
    ("Sacre Coeur Steps", "Stunning views of Paris from Montmartre", "viewpoint", 48.8867, 2.3431, "France", "City panorama", "Sunset", 1, 4.6),
    ("Le Comptoir du Pantheon", "Classic French bistro near the Pantheon", "restaurant", 48.8462, 2.3458, "France", "Duck confit", "Dinner", 3, 4.4),
    ("Shakespeare and Company", "Historic English bookshop on the Left Bank", "shop", 48.8526, 2.3471, "France", "Rare editions", "Afternoon", 2, 4.7),

    # Turkey (4 spots)
    ("Mandabatmaz", "Tiny legendary Turkish coffee spot in Istanbul", "cafe", 41.0315, 28.9744, "Turkey", "Turkish coffee", "Afternoon", 1, 4.6),
    ("Galata Tower", "Medieval tower with 360-degree Istanbul views", "viewpoint", 41.0256, 28.9741, "Turkey", "Bosphorus views", "Sunset", 2, 4.5),
    ("Mikla Restaurant", "Fine dining with stunning views over Istanbul", "restaurant", 41.0317, 28.9772, "Turkey", "Anatolian tasting menu", "Dinner", 4, 4.7),
    ("Grand Bazaar", "One of the world's oldest and largest covered markets", "shop", 41.0106, 28.9680, "Turkey", "Turkish carpets", "Morning", 2, 4.4),

    # Greece (4 spots)
    ("Little Kook", "Fairytale-themed cafe in Athens' Psyrri district", "cafe", 37.9780, 23.7249, "Greece", "Themed desserts", "Afternoon", 2, 4.3),
    ("Santorini Sunset Point", "Famous caldera viewpoint in Oia", "viewpoint", 36.4618, 25.3753, "Greece", "Sunset", "Evening", 1, 4.9),
    ("Ta Karamanlidika tou Fani", "Traditional Greek deli and meze restaurant", "restaurant", 37.9799, 23.7256, "Greece", "Cold cuts platter", "Lunch", 2, 4.5),
    ("Cine Paris", "Open-air rooftop cinema with Acropolis views", "activity", 37.9722, 23.7268, "Greece", "Classic films", "Night", 2, 4.6),

    # Iran (3 spots)
    ("Cafe Naderi", "Historic Tehran cafe from the 1920s", "cafe", 35.6997, 51.4150, "Iran", "Persian tea", "Afternoon", 2, 4.2),
    ("Tabiat Bridge", "Stunning pedestrian bridge with city views", "viewpoint", 35.7580, 51.4086, "Iran", "Night lights", "Evening", 1, 4.5),
    ("Tehran Grand Bazaar", "Ancient bazaar with traditional Persian goods", "shop", 35.6762, 51.4231, "Iran", "Saffron and carpets", "Morning", 2, 4.4),

    # Russia/Moscow (3 spots)
    ("Cafe Pushkin", "Ornate 19th-century style Russian restaurant", "restaurant", 55.7647, 37.6047, "Russia", "Beef Stroganoff", "Dinner", 4, 4.5),
    ("Sparrow Hills Viewpoint", "Panoramic Moscow view from university hill", "viewpoint", 55.7100, 37.5425, "Russia", "City skyline", "Sunset", 1, 4.4),
    ("GUM Department Store", "Historic shopping arcade on Red Square", "shop", 55.7546, 37.6215, "Russia", "Soviet nostalgia", "Afternoon", 3, 4.3),

    # Germany (4 spots)
    ("Cafe Einstein Stammhaus", "Classic Viennese-style cafe in a Berlin villa", "cafe", 52.5027, 13.3487, "Germany", "Apfelstrudel", "Morning", 3, 4.4),
    ("Reichstag Dome", "Glass dome with 360-degree Berlin views", "viewpoint", 52.5186, 13.3761, "Germany", "Sunset views", "Evening", 1, 4.6),
    ("Hofbrauhaus Munich", "World-famous Bavarian beer hall since 1589", "bar", 48.1376, 11.5799, "Germany", "Weissbier", "Evening", 2, 4.3),
    ("Currywurst at Konnopke", "Berlin's most famous currywurst stand since 1930", "restaurant", 52.5391, 13.4125, "Germany", "Currywurst", "Lunch", 1, 4.5),

    # Algeria (2 spots)
    ("Cafe Tantonville", "Historic cafe in Algiers with sea views", "cafe", 36.7538, 3.0588, "Algeria", "Mint tea", "Afternoon", 1, 4.1),
    ("Notre-Dame d'Afrique Viewpoint", "Basilica hilltop with Mediterranean views", "viewpoint", 36.8065, 3.0420, "Algeria", "Bay panorama", "Sunset", 1, 4.3),

    # Morocco (4 spots)
    ("Cafe Clock", "Cultural cafe in Fez medina with rooftop terrace", "cafe", 34.0620, -4.9784, "Morocco", "Camel burger", "Afternoon", 2, 4.4),
    ("Jardin Majorelle", "Stunning blue gardens created by Yves Saint Laurent", "viewpoint", 31.6417, -8.0035, "Morocco", "Blue architecture", "Morning", 2, 4.6),
    ("Le Jardin Restaurant", "Hidden garden restaurant in Marrakech medina", "restaurant", 31.6295, -7.9811, "Morocco", "Tagine", "Lunch", 3, 4.5),
    ("Souk Semmarine", "Main bazaar street in Marrakech medina", "shop", 31.6310, -7.9890, "Morocco", "Leather goods", "Morning", 2, 4.3),
]


def login() -> str:
    """Login and return access token."""
    response = requests.post(
        f"{API_URL}/auth/login",
        json={"email": EMAIL, "password": PASSWORD}
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_spot(token: str, spot_data: dict) -> dict:
    """Create a spot and return the response."""
    response = requests.post(
        f"{API_URL}/spots",
        json=spot_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()


def upload_image(token: str, spot_id: int, image_path: str) -> dict:
    """Upload an image to a spot."""
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

    print(f"\nCreating {len(SPOTS_DATA)} spots...")

    for i, (title, description, category, lat, lng, country, best, best_time, price_level, rating) in enumerate(SPOTS_DATA, 1):
        # Create spot
        spot_data = {
            "title": title,
            "description": description,
            "category": category,
            "latitude": lat,
            "longitude": lng,
            "address": country,
            "best": best,
            "best_time": best_time,
            "price_level": price_level,
            "rating": rating,
        }

        try:
            spot = create_spot(token, spot_data)
            spot_id = spot["id"]

            # Upload category-matching image
            image_path = os.path.join(IMAGES_DIR, f"{category}.jpeg")
            if os.path.exists(image_path):
                upload_image(token, spot_id, image_path)
                print(f"[{i}/{len(SPOTS_DATA)}] Created: {title} ({category}) with image")
            else:
                print(f"[{i}/{len(SPOTS_DATA)}] Created: {title} ({category}) - no image found")

        except Exception as e:
            print(f"[{i}/{len(SPOTS_DATA)}] Failed: {title} - {e}")

    print("\nDone! All spots created.")


if __name__ == "__main__":
    main()
