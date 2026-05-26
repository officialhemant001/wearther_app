"""
AI Engine models — chat sessions and messages.
"""

from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel


class ChatSession(UUIDModel):
    """User conversation session with the AI weather assistant."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=255, default='New Conversation')

    class Meta:
        db_table = 'ai_chat_sessions'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.email} - {self.title}"


class ChatMessage(UUIDModel):
    """Conversation messages."""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('assistant', 'AI')])
    content = models.TextField()

    class Meta:
        db_table = 'ai_chat_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.session.id} - {self.role}"
