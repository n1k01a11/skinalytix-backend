"""
SKINALYTIX — Seed script for the 30-product OTC database.

Run this AFTER your FastAPI server is up and the /products/ endpoint works.
It POSTs each product one at a time so you can see exactly which ones
succeed/fail in the console.

Usage:
    python seed_products.py
"""

import requests

# Change this if your API is running elsewhere (use your laptop's local IP
# if you're testing this script from a different machine than the server).
BASE_URL = "https://skinalytix-api.onrender.com"

PRODUCTS = [
    # ---------------- CLEANSERS ----------------
    {
        "brand": "Cetaphil", "product_name": "Gentle Skin Cleanser", "category": "Cleanser",
        "skin_types": ["All", "Sensitive"], "skin_concerns": ["Dryness", "Sensitivity", "Redness"],
        "key_ingredients": ["Glycerin", "Niacinamide", "Panthenol"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Cetaphil", "product_name": "Daily Facial Cleanser", "category": "Cleanser",
        "skin_types": ["Normal", "Combination", "Oily"], "skin_concerns": ["Excess oil", "Clogged pores"],
        "key_ingredients": ["Niacinamide", "Glycerin"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Celeteque", "product_name": "Acne Solutions Facial Wash", "category": "Cleanser",
        "skin_types": ["Oily", "Acne-Prone"], "skin_concerns": ["Acne-prone skin", "Clogged pores"],
        "key_ingredients": ["Salicylic Acid"], "time_of_use": ["PM"],
    },
    {
        "brand": "CeraVe", "product_name": "Foaming Facial Cleanser", "category": "Cleanser",
        "skin_types": ["Normal", "Oily", "Combination"], "skin_concerns": ["Excess oil", "Barrier support"],
        "key_ingredients": ["Ceramides", "Hyaluronic Acid", "Niacinamide"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Senka", "product_name": "Perfect Whip Cleanser", "category": "Cleanser",
        "skin_types": ["All"], "skin_concerns": ["Daily cleansing", "Excess oil"],
        "key_ingredients": ["Glycerin", "Sericin", "Hyaluronic Acid"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Garnier", "product_name": "Micellar Water / Bright Complete", "category": "Cleanser",
        "skin_types": ["All"], "skin_concerns": ["Makeup buildup", "Uneven tone"],
        "key_ingredients": ["Micellar agents", "Vitamin C"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Human Nature", "product_name": "Nourishing Facial Wash", "category": "Cleanser",
        "skin_types": ["Normal", "Dry"], "skin_concerns": ["Daily cleansing", "Dryness"],
        "key_ingredients": ["Glycerin", "Plant-derived cleansing agents"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Simple", "product_name": "Kind to Skin Refreshing Facial Wash", "category": "Cleanser",
        "skin_types": ["All", "Sensitive"], "skin_concerns": ["Sensitivity", "Dryness"],
        "key_ingredients": ["Panthenol", "Vitamin E", "Glycerin"], "time_of_use": ["AM", "PM"],
    },

    # ---------------- SERUMS / ESSENCES ----------------
    {
        "brand": "Luxe Organix", "product_name": "Power Glow Vita Glow C Serum", "category": "Serum",
        "skin_types": ["All"], "skin_concerns": ["Dullness", "Uneven tone"],
        "key_ingredients": ["Vitamin C derivatives", "Brightening ingredients"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Fresh Skinlab", "product_name": "Tomato Glass Skin 3-in-1 Vitamin C Brightening Serum",
        "category": "Serum", "skin_types": ["All"], "skin_concerns": ["Dullness", "Uneven tone"],
        "key_ingredients": ["Vitamin C", "Tomato-derived ingredients"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Kojie.san", "product_name": "Skin Lightening Super Serum", "category": "Serum",
        "skin_types": ["All"], "skin_concerns": ["Dark spots", "Uneven tone"],
        "key_ingredients": ["Kojic Acid", "Niacinamide", "Vitamin C", "Vitamin E", "Panthenol"],
        "time_of_use": ["PM"],
    },
    {
        "brand": "Luxelle PH", "product_name": "Centella Sun Serum SPF50", "category": "Serum/Sunscreen",
        "skin_types": ["All", "Sensitive"], "skin_concerns": ["UV exposure"],
        "key_ingredients": ["Centella Asiatica", "UV filters"], "time_of_use": ["AM"],
        "validation_status": "Needs verification",
        "selection_notes": "Could not confirm exact current formulation from manufacturer sources; keep only if this matches the exact physical product the dermatologist reviewed.",
    },
    {
        "brand": "Human Nature", "product_name": "Vitamin C + Hya Calamansi Radiance Serum", "category": "Serum",
        "skin_types": ["All"], "skin_concerns": ["Dullness", "Uneven tone"],
        "key_ingredients": ["Ascorbyl Glucoside", "Ascorbic Acid", "Hyaluronic Acid", "Zinc"],
        "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "The Ordinary", "product_name": "Niacinamide 10% + Zinc 1%", "category": "Serum",
        "skin_types": ["Oily", "Combination"], "skin_concerns": ["Blemishes", "Excess oil"],
        "key_ingredients": ["Niacinamide", "Zinc PCA"], "time_of_use": ["AM", "PM"],
        "ingredient_overlap_group": "niacinamide-serums",
    },
    {
        "brand": "COSRX", "product_name": "Advanced Snail 96 Mucin Power Essence", "category": "Essence",
        "skin_types": ["All", "Sensitive"], "skin_concerns": ["Dryness", "Uneven texture", "Post-breakout marks"],
        "key_ingredients": ["Snail Secretion Filtrate", "Sodium Hyaluronate", "Panthenol", "Allantoin"],
        "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "La Roche-Posay", "product_name": "Hyalu B5 Serum", "category": "Serum",
        "skin_types": ["All", "Sensitive"], "skin_concerns": ["Dryness", "Barrier support"],
        "key_ingredients": ["Hyaluronic Acid", "Panthenol", "Madecassoside"], "time_of_use": ["AM", "PM"],
    },

    # ---------------- SUNSCREENS ----------------
    {
        "brand": "Luxe Organix", "product_name": "Aqua Daily Sunscreen SPF50+ PA+++", "category": "Sunscreen",
        "skin_types": ["All", "Sensitive"], "skin_concerns": ["UV exposure", "Dryness"],
        "key_ingredients": ["UV filters", "Aloe Vera", "Panthenol"], "time_of_use": ["AM"],
    },
    {
        "brand": "QuickFX", "product_name": "Sun Screen SPF50 PA++", "category": "Sunscreen",
        "skin_types": ["All"], "skin_concerns": ["UV exposure", "Discoloration"],
        "key_ingredients": ["Titanium Dioxide", "Zinc Oxide", "Niacinamide"], "time_of_use": ["AM"],
        "ingredient_overlap_group": "niacinamide-sunscreens",
    },
    {
        "brand": "Face Republic", "product_name": "Purity Sun Essence SPF50+ PA++++", "category": "Sunscreen",
        "skin_types": ["Normal", "Combination", "Dry"], "skin_concerns": ["UV exposure", "Uneven tone"],
        "key_ingredients": ["UV filters", "Niacinamide", "Glycerin"], "time_of_use": ["AM"],
        "ingredient_overlap_group": "niacinamide-sunscreens",
    },
    {
        "brand": "Belo", "product_name": "SunExpert Tinted Sunscreen SPF50", "category": "Sunscreen",
        "skin_types": ["Normal", "Combination"], "skin_concerns": ["UV exposure", "Uneven tone"],
        "key_ingredients": ["UV filters", "Niacinamide"], "time_of_use": ["AM"],
        "ingredient_overlap_group": "niacinamide-sunscreens",
        "validation_status": "Needs verification",
        "selection_notes": "Formulation can vary by version; confirm current ingredient list against packaging before treating as complete.",
    },
    {
        "brand": "Watsons", "product_name": "Very High Protection Sunscreen Face Serum SPF50+ PA++++",
        "category": "Sunscreen", "skin_types": ["All"], "skin_concerns": ["UV exposure"],
        "key_ingredients": ["UV filters", "Vitamin E", "Antioxidants"], "time_of_use": ["AM"],
    },
    {
        "brand": "Dermplus", "product_name": "Moisturizing Sunscreen SPF60 PA++++", "category": "Sunscreen",
        "skin_types": ["Normal", "Dry"], "skin_concerns": ["UV exposure", "Dryness"],
        "key_ingredients": ["UV filters", "Moisturizing ingredients"], "time_of_use": ["AM"],
        "validation_status": "Needs verification",
        "selection_notes": "Could not obtain a sufficiently detailed current ingredient page to confidently confirm the full ingredient list.",
    },
    {
        "brand": "Cathy Doll", "product_name": "Aqua Sun Non-Greasy Body Sun Serum SPF50", "category": "Sunscreen",
        "skin_types": ["Normal", "Combination"], "skin_concerns": ["UV exposure"],
        "key_ingredients": ["Titanium Dioxide", "UV filters", "Niacinamide", "Hyaluronic Acid"],
        "time_of_use": ["AM"],
        "selection_notes": "This is a body sun serum, not a dedicated facial sunscreen — keep that distinction when matching to facial skin profiles.",
    },
    {
        "brand": "Luxe Organix", "product_name": "High Protection Aqua PDRN Soft Glow Serum Sunscreen SPF50",
        "category": "Sunscreen", "skin_types": ["Normal", "Dry", "Sensitive"],
        "skin_concerns": ["UV exposure", "Dryness", "Dullness"],
        "key_ingredients": ["UV filters", "Niacinamide", "PDRN/Sodium DNA", "Ceramides", "Panthenol"],
        "time_of_use": ["AM"],
    },

    # ---------------- MOISTURIZERS ----------------
    {
        "brand": "CeraVe", "product_name": "Moisturizing Cream", "category": "Moisturizer",
        "skin_types": ["Dry", "Normal", "Sensitive"], "skin_concerns": ["Dryness", "Barrier support"],
        "key_ingredients": ["Ceramides", "Hyaluronic Acid", "Glycerin", "Petrolatum"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Cetaphil", "product_name": "Moisturizing Cream", "category": "Moisturizer",
        "skin_types": ["Dry", "Very Dry", "Sensitive"], "skin_concerns": ["Dryness"],
        "key_ingredients": ["Glycerin", "Niacinamide", "Panthenol", "Vitamin E"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Neutrogena", "product_name": "Hydro Boost Water Gel", "category": "Gel Moisturizer",
        "skin_types": ["All", "Sensitive"], "skin_concerns": ["Dehydration"],
        "key_ingredients": ["Hyaluronic Acid", "Glycerin"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "The Ordinary", "product_name": "Natural Moisturizing Factors + HA", "category": "Moisturizer",
        "skin_types": ["Normal", "Dry", "Combination"], "skin_concerns": ["Dryness", "Dehydration"],
        "key_ingredients": ["Amino Acids", "Hyaluronic Acid", "Urea", "PCA"], "time_of_use": ["AM", "PM"],
    },
    {
        "brand": "Clinique", "product_name": "Dramatically Different Moisturizing Gel", "category": "Gel Moisturizer",
        "skin_types": ["Oily", "Combination"], "skin_concerns": ["Oiliness", "Dehydration"],
        "key_ingredients": ["Humectants", "Glycerin"], "time_of_use": ["AM", "PM"],
        "validation_status": "Needs verification",
        "selection_notes": "Verify exact current Philippine formulation from packaging/manufacturer before treating ingredient list as complete.",
    },
    {
        "brand": "Aveeno", "product_name": "Daily Moisturizing Lotion", "category": "Moisturizer",
        "skin_types": ["Normal", "Dry", "Sensitive"], "skin_concerns": ["Dryness", "Roughness"],
        "key_ingredients": ["Colloidal Oatmeal", "Glycerin"], "time_of_use": ["AM", "PM"],
    },
]


def seed():
    success_count = 0
    fail_count = 0

    for product in PRODUCTS:
        try:
            response = requests.post(f"{BASE_URL}/products/", json=product)
            if response.status_code == 200:
                success_count += 1
                print(f"✅ Added: {product['brand']} — {product['product_name']}")
            else:
                fail_count += 1
                print(f"❌ Failed: {product['brand']} — {product['product_name']} | {response.text}")
        except requests.exceptions.ConnectionError:
            print("Could not connect to the API. Is uvicorn running?")
            return

    print(f"\nDone. {success_count} added, {fail_count} failed.")


if __name__ == "__main__":
    seed()