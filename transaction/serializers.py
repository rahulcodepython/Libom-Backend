from rest_framework import serializers
from .models import Subscribe


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        exclude = ["subscriber"]
