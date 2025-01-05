from rest_framework import serializers
from .models import Subscribe


class SubscriptionSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = "__all__"
        read_only_fields = ["subscriber"]

    def get_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False

        return user in obj.subscriber.all()
