import requests
from django.conf import settings
import requests
PRODUCT_SERVICE_URLS = settings.PRODUCT_SERVICE_URLS

def get_product_url(product_type, product_id):
    """Get correct product API URL based on product type"""
    base_url = PRODUCT_SERVICE_URLS.get(product_type)
    if base_url:
        return f"{base_url}{product_id}/"
    return None

def check_product_stock(product_type, product_id, quantity):
    """Check if product stock is available"""
    url = get_product_url(product_type, product_id)
    if not url:
        return False
    
    response = requests.get(url)
    if response.status_code == 200:
        product = response.json()
        return product["stock"] >= quantity
    return False



def update_product_stock(product_type, product_id, quantity):
    """Update stock in product service"""
    url = get_product_url(product_type, product_id)
    if not url:
        return False

    # Make a request to get product details
    response = requests.get(url)
    if response.status_code != 200:
        return False

    product = response.json()  # Convert response to dictionary
    if "stock" not in product:
        return False
    print(quantity)
    soluong = int(product["stock"]) - int(quantity)
    
    # Update stock with PATCH request
    response = requests.patch(url, json={"stock": soluong})
    print(response.json())
    
    return response.status_code == 200

