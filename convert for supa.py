import json
import csv
import os
import sys

def json_to_csv(json_file_path, csv_file_path):
    try:
        # Read the JSON file
        print(f"Reading JSON file from: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as file:
            products_data = json.load(file)

        # Define CSV headers matching the Supabase table
        headers = [
            'name', 'category', 'color', 'price',
            'image_url1', 'image_url2', 'image_url3', 'image_url4', 'image_url5', 'image_url6',
            'brand', 'link', 'description', 'gender_target', 'style', 'created_at'
        ]

        # Prepare data for CSV
        rows = []
        for item in products_data:
            # Extract up to 6 image URLs, filling with empty string if fewer or missing
            image_urls = item.get('image_urls', []) or []
            image_urls = [url if url and url.strip() else '' for url in image_urls]
            while len(image_urls) < 6:
                image_urls.append('')

            row = {
                'name': item.get('name', ''),
                'category': item.get('category', ''),
                'color': item.get('color', ''),
                'price': item.get('price', 0),
                'image_url1': image_urls[0],
                'image_url2': image_urls[1],
                'image_url3': image_urls[2],
                'image_url4': image_urls[3],
                'image_url5': image_urls[4],
                'image_url6': image_urls[5],
                'brand': item.get('brand', ''),
                'link': item.get('link', ''),
                'description': item.get('description', ''),
                'gender_target': item.get('gender_target', ''),
                'style': item.get('style', ''),
                'created_at': item.get('created_at', '')
            }
            rows.append(row)

        # Write to CSV
        print(f"Writing CSV file to: {csv_file_path}")
        with open(csv_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        print(f"Successfully converted {len(rows)} products to CSV.")

    except FileNotFoundError as e:
        print(f"File error: {str(e)}")
        sys.exit(1)
    except KeyError as e:
        print(f"JSON key error: Missing key {str(e)} in product data")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting JSON to CSV conversion...")
    json_file_path = r'C:\Users\Amar shah\Desktop\Data Extraction Xaze\products.json'
    csv_file_path = r'C:\Users\Amar shah\Desktop\Data Extraction Xaze\products_converted.csv'
    json_to_csv(json_file_path, csv_file_path)
