import requests
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

API_KEY = "00c4cc9109af69133528cc76d0bdb290e4704f38091a12f915ca2e587c33eb94"

def fetch_product_details(product_id, source_seller, gl="in", hl="en", google_domain="google.co.in"):
    """
    Fetch product details using google_product engine to get direct links, images, and description.
    """
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_product",
        "product_id": product_id,
        "gl": gl,
        "hl": hl,
        "google_domain": google_domain,
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error fetching product details:", response.status_code, response.text)
        return None, [], ""

    data = response.json()
    product_results = data.get("product_results", {})
    sellers_results = data.get("sellers_results", {}).get("online_sellers", [])

    # Get multiple images
    image_urls = [media.get("link", "") for media in product_results.get("media", []) if media.get("type") == "image"]
    image_urls = list(filter(None, set(image_urls)))  # Remove duplicates/empties

    # Find direct link for the matching seller (e.g., "Myntra")
    direct_link = ""
    for seller in sellers_results:
        if seller.get("name", "").lower() == source_seller.lower():
            direct_link = seller.get("direct_link") or parse_direct_link(seller.get("link", ""))
            break
    if not direct_link and sellers_results:  # Fallback to first seller
        direct_link = sellers_results[0].get("direct_link") or parse_direct_link(seller[0].get("link", ""))

    # Get short description
    description = product_results.get("description", "") or product_results.get("snippet", "")
    if not description:  # Fallback if no description in product_results
        description = "No description available."
    # Truncate to 150 characters for brevity
    description = (description[:147] + "...") if len(description) > 150 else description

    return direct_link, image_urls, description

def parse_direct_link(google_link):
    """
    Fallback: Parse the 'q' parameter from Google's redirect URL.
    """
    if "google.com/url" in google_link:
        parsed_url = urlparse(google_link)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("q", [""])[0]
    return google_link

def search_products(query, filename="products.json"):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "engine": "google_shopping",
        "gl": "in",
        "hl": "en",
        "google_domain": "google.co.in",
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching results:", response.status_code, response.text)
        return
    
    data = response.json()

    if "shopping_results" not in data or not data["shopping_results"]:
        print("No shopping results found")
        return

    results = []
    for item in data["shopping_results"]:
        source = item.get("source", "Unknown")
        product_id = item.get("product_id")  # For detailed fetch

        # Initialize defaults
        direct_link = item.get("link") or item.get("product_link", "")
        image_urls = [item.get("thumbnail", "")]
        description = item.get("snippet", "") or "No description available."

        # Fetch details if product_id available
        if product_id:
            fetched_link, fetched_images, fetched_description = fetch_product_details(product_id, source)
            if fetched_link:
                direct_link = fetched_link
            if fetched_images:
                image_urls = fetched_images
            if fetched_description:
                description = fetched_description

        # Fallback description using extensions if still empty
        if description == "No description available." and item.get("extensions"):
            extensions = item.get("extensions", [])
            description = f"{item.get('title', 'Product')} - {', '.join(extensions[:3])}"  # Use first 3 extensions
            description = (description[:147] + "...") if len(description) > 150 else description

        product = {
            "name": item.get("title", "Unknown Product"),
            "category": "Printed T-Shirts",
            "color": item.get("color", "Unknown"),
            "price": item.get("extracted_price", 0),
            "image_urls": image_urls,
            "brand": source,
            "link": direct_link,
            "description": description,
            "gender_target": "Unisex",
            "style": "Casual",
            "created_at": datetime.utcnow().isoformat()
        }
        results.append(product)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"✅ Saved {len(results)} products into {filename}")

# Example
search_products(" printed tshirt the soul store")