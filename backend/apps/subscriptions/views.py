from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.utils import success_response
from django.utils import timezone
from datetime import timedelta
from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """List available billing plans."""
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)
    permission_classes = []  # Public


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Manage active subscription."""
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        plan_id = request.data.get('plan_id')
        plan = Plan.objects.filter(id=plan_id, is_active=True).first()
        if not plan:
            return Response({'success': False, 'error': {'message': 'Invalid plan selected.'}}, status=status.HTTP_400_BAD_REQUEST)

        # Upsert subscription
        now = timezone.now()
        sub, created = Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                'plan': plan,
                'status': 'active',
                'starts_at': now,
                'expires_at': now + timedelta(days=30),
                'cancel_at_period_end': False,
            }
        )

        # Update profile premium status
        profile = request.user.profile
        profile.is_premium = True
        profile.premium_expires_at = sub.expires_at
        profile.save(update_fields=['is_premium', 'premium_expires_at'])

        return Response(success_response(data=SubscriptionSerializer(sub).data, message='Subscribed successfully.'))

    @action(detail=False, methods=['post'])
    def cancel(self, request):
        sub = self.get_queryset().first()
        if not sub:
            return Response({'success': False, 'error': {'message': 'No active subscription found.'}}, status=status.HTTP_404_NOT_FOUND)

        sub.cancel_at_period_end = True
        sub.status = 'canceled'
        sub.save(update_fields=['cancel_at_period_end', 'status'])
        return Response(success_response(data=SubscriptionSerializer(sub).data, message='Subscription set to cancel.'))
