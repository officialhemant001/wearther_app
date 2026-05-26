import React, { useState, useEffect, useRef } from 'react';
import { Sparkles, Send, ArrowRight, CloudRain, ShieldCheck } from 'lucide-react';
import api from '../services/api';
import DashboardLayout from '../layouts/DashboardLayout';

export const Assistant = () => {
  const [session, setSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [starting, setStarting] = useState(true);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    const initChat = async () => {
      try {
        // Create a new session
        const res = await api.post('/ai/sessions/');
        setSession(res.data);
        setMessages([
          {
            id: 'welcome',
            role: 'assistant',
            content: "Hello! I am Aether, your AI weather companion. I can help analyze current weather trends, predict upcoming patterns, recommend activities, or suggest crop scheduling. Ask me anything!"
          }
        ]);
      } catch (err) {
        console.error('Failed to create chat session', err);
      } finally {
        setStarting(false);
      }
    };
    initChat();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !session) return;

    const userText = input.trim();
    setInput('');
    setLoading(true);

    // Optimistically add user message
    setMessages((prev) => [...prev, { id: Date.now().toString(), role: 'user', content: userText }]);

    try {
      const res = await api.post('/ai/messages/', {
        session: session.id,
        content: userText
      });
      if (res.data) {
        setMessages((prev) => [...prev, res.data.assistant_message]);
      }
    } catch (err) {
      console.error('Failed to get AI response', err);
      setMessages((prev) => [
        ...prev,
        {
          id: 'error-' + Date.now(),
          role: 'assistant',
          content: "Sorry, I am facing connectivity issues resolving that request. Please try again in a moment."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickPrompt = (promptText) => {
    setInput(promptText);
  };

  if (starting) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
          <div className="w-10 h-10 border-4 border-slate-200 border-t-brand-500 rounded-full animate-spin"></div>
          <span className="text-sm font-medium text-slate-400">Syncing AI Brain...</span>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto flex flex-col h-[78vh]">
        {/* Chat Header */}
        <div className="border-b border-slate-200/50 dark:border-slate-800/50 pb-4 mb-6 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-brand-500" />
            <h1 className="text-xl font-display font-bold text-slate-900 dark:text-white">Aether Neural Advisor</h1>
          </div>
          <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-brand-500/10 text-brand-500 flex items-center gap-1">
            <ShieldCheck className="h-3 w-3" /> GPT-4 Active
          </span>
        </div>

        {/* Conversation Dialogue Bubble Stream */}
        <div className="flex-1 overflow-y-auto pr-2 space-y-4 mb-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-lg rounded-2xl px-4 py-3 text-xs leading-relaxed ${
                  message.role === 'user'
                    ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-medium'
                    : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200/40 dark:border-slate-800/80 shadow-premium'
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800/80 rounded-2xl px-4 py-3 text-xs flex gap-1.5 items-center">
                <span className="h-1.5 w-1.5 bg-slate-400 rounded-full animate-bounce"></span>
                <span className="h-1.5 w-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                <span className="h-1.5 w-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick prompt suggestions (when conversation is empty or welcome state) */}
        {messages.length === 1 && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6">
            {[
              { text: "What should I wear in New Delhi today?", icon: "👕" },
              { text: "Are winds optimal for sowing seeds?", icon: "🌾" },
              { text: "Rain probability next week?", icon: "🌧️" },
            ].map((prompt, idx) => (
              <button
                key={idx}
                onClick={() => handleQuickPrompt(prompt.text)}
                className="p-3 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-xl text-[11px] text-left hover:border-brand-500/50 hover:bg-slate-50 dark:hover:bg-slate-950 transition-all font-medium text-slate-500 dark:text-slate-400 flex items-center gap-2"
              >
                <span>{prompt.icon}</span>
                <span>{prompt.text}</span>
              </button>
            ))}
          </div>
        )}

        {/* Entry Input Form */}
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Aether about the weather..."
            className="flex-1 premium-input"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="p-3.5 bg-slate-900 dark:bg-white text-white dark:text-slate-900 rounded-xl disabled:opacity-50 hover:opacity-90 transition-all"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
      </div>
    </DashboardLayout>
  );
};
export default Assistant;
