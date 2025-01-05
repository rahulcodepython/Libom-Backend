from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Subscribe
from .serializers import SubscriptionSerializer
from authentication.models import Profile
from datetime import date
from backend.message import Message
from backend.decorators import catch_exception


class SubscriptionView(APIView):
    def get(self, request):
        subscriptions = Subscribe.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @catch_exception
    def get(self, request, id):
        plan = Subscribe.objects.get(id=id)
        plan.subscriber.add(request.user)
        profile = Profile.objects.get(user=request.user)
        profile.subscription = plan
        profile.subscription_date = date.today()
        profile.save()
        plan.save()
        return Message.success("Subscribed successfully")
