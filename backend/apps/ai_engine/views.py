from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.core.utils import success_response
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer
from django.conf import settings
import requests
import json


class ChatSessionViewSet(viewsets.ModelViewSet):
    """Manage AI conversation sessions and ask weather queries."""
    serializer_class = ChatSessionSerializer

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Create standard session
        session = ChatSession.objects.create(user=request.user)
        # Add initial prompt / system greeting if wanted
        return Response(success_response(data=ChatSessionSerializer(session).data, message='Conversation started.'))


class ChatMessageViewSet(viewsets.ModelViewSet):
    """Manage messages within a conversation and trigger AI responses."""
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return ChatMessage.objects.filter(session__user=self.request.user)

    def create(self, request, *args, **kwargs):
        session_id = request.data.get('session')
        content = request.data.get('content')

        if not session_id or not content:
            return Response({'success': False, 'error': {'message': 'Session and content are required.'}}, status=status.HTTP_400_BAD_REQUEST)

        session = ChatSession.objects.filter(id=session_id, user=request.user).first()
        if not session:
            return Response({'success': False, 'error': {'message': 'Session not found.'}}, status=status.HTTP_404_NOT_FOUND)

        # 1. Save user message
        user_message = ChatMessage.objects.create(session=session, role='user', content=content)

        # 2. Get AI response (mock responses with weather context if API key is not active)
        ai_reply = self._get_ai_response(content)

        # 3. Save assistant message
        assistant_message = ChatMessage.objects.create(session=session, role='assistant', content=ai_reply)

        # Update session title if default
        if session.title == 'New Conversation':
            session.title = content[:30] + '...' if len(content) > 30 else content
            session.save(update_fields=['title', 'updated_at'])

        return Response(success_response(
            data={
                'user_message': ChatMessageSerializer(user_message).data,
                'assistant_message': ChatMessageSerializer(assistant_message).data
            },
            message='AI Reply generated'
        ))

    def _get_ai_response(self, user_query):
        """Invoke LLM API or fallback to rule-based mock responses."""
        api_key = getattr(settings, 'OPENAI_API_KEY', '')
        if not api_key:
            return self._get_fallback_reply(user_query)

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": getattr(settings, 'AI_MODEL', 'gpt-4'),
                "messages": [
                    {"role": "system", "content": "You are a professional weather assistant. Provide direct, helpful advice about weather conditions, activities, agricultural impacts, health suggestions, and clothing recommendations."},
                    {"role": "user", "content": user_query}
                ]
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            return self._get_fallback_reply(user_query)
        except Exception:
            return self._get_fallback_reply(user_query)

    def _get_fallback_reply(self, user_query):
        q = user_query.lower()
        if 'rain' in q:
            return "Based on your current region, light rain is expected in the afternoon. Carrying an umbrella is advised, and outdoor activities should be planned for the morning."
        if 'hot' in q or 'summer' in q or 'temp' in q:
            return "Temperatures are relatively high (around 32-35°C). Ensure you stay hydrated, limit physical activity outdoors during peak hours (12 PM - 3 PM), and apply sunscreen."
        if 'crop' in q or 'farm' in q:
            return "The current moderate soil moisture and light wind are ideal for sowing crops. However, please ensure your irrigation is managed before the light rainfall forecast for tomorrow."
        return "Hello! I am your AI Weather Companion. I can help analyze current weather trends, predict conditions, suggest activities, and offer health tips. Feel free to ask me anything about the weather!"
