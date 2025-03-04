from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
import paypalrestsdk
from django.conf import settings
from .models import Payment, PaymentStatus
from .serializers import PaymentSerializer
from .paypal_helper import paypalrestsdk

ORDER_API = "http://127.0.0.1:8004/order/orders/"

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=["post"])
    def create_paypal_payment(self, request):
        order_id = request.data.get("order_id")

        # Validate Order
        order_resp = requests.get(f"{ORDER_API}{order_id}/")
        if order_resp.status_code != 200:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order_data = order_resp.json()
        amount = order_data["total_price"]

        # Create PayPal Payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8005/payment/paypal/execute/",
                "cancel_url": "http://127.0.0.1:8005/payment/paypal/cancel/"
            },
            "transactions": [{
                "amount": {
                    "total": str(amount),
                    "currency": "USD"
                },
                "description": f"Payment for Order {order_id}"
            }]
        })

        if payment.create():
            approval_url = next(link["href"] for link in payment.links if link["rel"] == "approval_url")

            # Save Payment
            Payment.objects.create(
                order_id=order_id, amount=amount, method="PayPal", status=PaymentStatus.PENDING
            )

            return Response({"payment_url": approval_url}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Failed to create PayPal payment"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def execute_paypal_payment(self, request):
        payment_id = request.GET.get("paymentId")
        payer_id = request.GET.get("PayerID")

        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            order_id = payment.transactions[0]["description"].split()[-1]

            # Update Payment in DB
            payment_record = Payment.objects.get(order_id=order_id)
            payment_record.status = PaymentStatus.SUCCESS
            payment_record.save()

            # Update Order Status
            requests.post(f"{ORDER_API}{order_id}/update_status/", json={"status": "Completed"})

            return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Payment execution failed"}, status=status.HTTP_400_BAD_REQUEST)
