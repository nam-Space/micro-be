import httpx
import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Define service URLs
import os

SERVICES = {
    "customer": os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:8003"),
    "order": os.getenv("ORDER_SERVICE_URL", "http://localhost:8004"),
    "product": os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8006"),
    "cart": os.getenv("CART_SERVICE_URL", "http://localhost:8002"),
    "payment": os.getenv("PAYMENT_SERVICE_URL", "http://localhost:8005"),
}


@method_decorator(csrf_exempt, name="dispatch")  # Disable CSRF for API proxying
class ProxyView(View):
    def dispatch_request(self, request, service, path, method):
        """Handles GET, POST, PUT, PATCH, DELETE requests and proxies them."""
        if service not in SERVICES:
            return JsonResponse({"error": "Unknown service"}, status=400)

        url = f"{SERVICES[service]}/{path}"
        print(f"Proxying {method} request to: {url}")

        # Forward headers (except Host & Content-Length)
        headers = {
            key: value for key, value in request.headers.items()
            if key.lower() not in ["host", "content-length"]
        }
        
        # Ensure CSRF token is forwarded if present
        if "X-CSRFTOKEN" in request.headers:
            headers["X-CSRFTOKEN"] = request.headers["X-CSRFTOKEN"]

        # Handle request body correctly
        data = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                data = json.loads(request.body.decode("utf-8")) if request.body else {}
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        try:
            with httpx.Client() as client:
                response = client.request(method, url, json=data, headers=headers)

            if not response.text.strip():
                return HttpResponse(status=204)  

            if "application/json" not in response.headers.get("Content-Type", ""):
                return JsonResponse(
                    {"error": "Backend did not return JSON", "raw_response": response.text},
                    status=response.status_code or 502
                )

            return JsonResponse(response.json(), safe= False, status=response.status_code)

        except httpx.RequestError as e:
            print(f"Request error: {e}")   
            return JsonResponse({"error": "Failed to reach backend service", "details": str(e)}, status=502)

        except json.JSONDecodeError:
            print(f"JSON Decode Error: Invalid response from {url}")  # Debugging
            return JsonResponse({"error": "Invalid JSON response from backend"}, status=502)

    def get(self, request, service, path):
        return self.dispatch_request(request, service, path, "GET")

    def post(self, request, service, path):
        return self.dispatch_request(request, service, path, "POST")

    def put(self, request, service, path):
        return self.dispatch_request(request, service, path, "PUT")

    def patch(self, request, service, path):
        return self.dispatch_request(request, service, path, "PATCH")

    def delete(self, request, service, path):
        return self.dispatch_request(request, service, path, "DELETE")
