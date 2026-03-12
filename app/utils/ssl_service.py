import os
import httpx
from typing import Optional, Dict, Any

class SSLCommerzService:
    def __init__(self):
        self.store_id = os.getenv("SSL_STORE_ID")
        self.store_pass = os.getenv("SSL_STORE_PASS")
        self.is_sandbox = os.getenv("SSL_IS_SANDBOX", "True").lower() == "true"
        self.base_url = "https://sandbox.sslcommerz.com" if self.is_sandbox else "https://securepay.sslcommerz.com"
        self.backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8001")

    async def initiate_payment(
        self, 
        total_amount: float, 
        tran_id: str, 
        cus_name: str, 
        cus_email: str, 
        cus_phone: str,
        product_name: str = "Food Order"
    ) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/gwprocess/v4/api.php"
        
        payload = {
            "store_id": self.store_id,
            "store_passwd": self.store_pass,
            "total_amount": total_amount,
            "currency": "BDT",
            "tran_id": tran_id,
            "success_url": f"{self.backend_url}/payments/success",
            "fail_url": f"{self.backend_url}/payments/fail",
            "cancel_url": f"{self.backend_url}/payments/cancel",
            "ipn_url": f"{self.backend_url}/payments/ipn",
            "cus_name": cus_name,
            "cus_email": cus_email,
            "cus_add1": "Dhaka",
            "cus_city": "Dhaka",
            "cus_postcode": "1000",
            "cus_country": "Bangladesh",
            "cus_phone": cus_phone,
            "shipping_method": "NO",
            "product_name": product_name,
            "product_category": "Food",
            "product_profile": "general"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload)
            if response.status_code == 200:
                return response.json()
            return None

    async def validate_payment(self, val_id: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/validator/api/validationserverAPI.php"
        params = {
            "val_id": val_id,
            "store_id": self.store_id,
            "store_passwd": self.store_pass,
            "format": "json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            return None

ssl_service = SSLCommerzService()
