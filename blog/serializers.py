from rest_framework import serializers

class BrokerageCalculationInputSerializer(serializers.Serializer):
    broker = serializers.CharField()
    segment = serializers.CharField()
    order_type = serializers.CharField()
    buy_price = serializers.FloatField()
    sell_price = serializers.FloatField()
    quantity = serializers.IntegerField()
