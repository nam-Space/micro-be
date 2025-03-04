from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True) 

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        # Update Order fields
        instance.customer_id = validated_data.get('customer_id', instance.customer_id)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()

        # Update Order Items
        instance.items.all().delete()  # Remove old items
        for item in items_data:
            item.pop('order', None)
            OrderItem.objects.create(order=instance, **item)

        return instance
