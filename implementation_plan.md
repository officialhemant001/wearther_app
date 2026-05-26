# Next Generation Weather Application — Implementation Plan

## Overview

Build a production-ready, enterprise-grade weather platform with a **Django REST backend** (20 modular apps, JWT auth, WebSocket, Celery, Redis, PostgreSQL) and a **React + Vite frontend** (Tailwind CSS v3, Framer Motion, glassmorphism UI, dark/light mode, mobile-first responsive design).

> [!IMPORTANT]
> This is an extremely large project (~150+ files). I will build it **incrementally in 6 phases**, delivering working code at each stage. Each phase builds on the previous one.

---

## User Review Required

> [!WARNING]
> **API Keys**: The weather features require API keys for real data. I will integrate with **OpenWeatherMap** (free tier available) as the primary weather data provider. For AI assistant, I'll build a pluggable interface (OpenAI/Gemini). Please confirm:
> 1. Do you have an OpenWeatherMap API key, or should I use mock/demo data for now?
> 2. For Google OAuth — do you have a Google Cloud project with OAuth credentials?
> 3. For OTP — Twilio or Firebase? Do you have credentials?
> 4. PostgreSQL — do you have it installed locally, or should I keep SQLite for development?

> [!IMPORTANT]
> **Tailwind CSS**: You requested Tailwind CSS explicitly. I will use **Tailwind CSS v3** with custom configuration for the glassmorphism design system. Confirming this is acceptable.

---

## Open Questions

1. **Payment Gateway**: For premium subscriptions — Stripe, Razorpay, or just a mock subscription system for now?
2. **Deployment Target**: Docker Compose for local dev? AWS/GCP/DigitalOcean for production?
3. **Email Provider**: For email verification and password reset — SMTP (Gmail), SendGrid, or console backend for dev?
4. **Weather Radar**: Real radar tile integration (OpenWeatherMap radar layers) or a visual simulation?

---

## Architecture Overview

```
d:\PROJECT ALL\Weather\
├── backend/                          # Django project
│   ├── backend/                      # Project config (settings, urls, asgi, wsgi)
│   ├── apps/                         # All 20 Django apps
│   │   ├── core/                     # Base models, mixins, utilities
│   │   ├── users/                    # Custom user model, profiles
│   │   ├── weather/                  # Current weather data
│   │   ├── forecasts/                # Weather forecasts (hourly, daily, weekly)
│   │   ├── alerts/                   # Smart weather alerts
│   │   ├── ai_engine/                # AI weather assistant
│   │   ├── radar/                    # Weather radar data
│   │   ├── locations/                # Saved locations, geolocation
│   │   ├── notifications/            # Push/email/in-app notifications
│   │   ├── analytics/                # User analytics, weather stats
│   │   ├── subscriptions/            # Premium plans, payments
│   │   ├── api_logs/                 # API request logging
│   │   ├── settings_manager/         # App-wide settings
│   │   ├── admin_panel/              # Custom admin dashboard
│   │   ├── websocket_server/         # Django Channels WebSocket
│   │   ├── recommendations/          # Personalized recommendations
│   │   ├── health_weather/           # Health-related weather data
│   │   ├── farming_weather/          # Agricultural weather
│   │   ├── reports/                  # Weather reports generation
│   │   └── cache_system/             # Redis cache management
│   ├── config/                       # Environment configs
│   ├── media/                        # User uploads
│   ├── static/                       # Static files
│   ├── requirements/                 # Pip requirements (base, dev, prod)
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
│
├── frontend/                         # React + Vite project
│   ├── public/
│   ├── src/
│   │   ├── assets/                   # Icons, images, fonts
│   │   ├── components/               # Reusable UI components
│   │   │   ├── ui/                   # Base UI (Button, Card, Input, Modal)
│   │   │   ├── layout/               # Header, Sidebar, Footer, MobileNav
│   │   │   ├── weather/              # Weather-specific components
│   │   │   ├── charts/               # Chart components (Recharts)
│   │   │   └── common/               # Shared components
│   │   ├── pages/                    # Route pages
│   │   ├── hooks/                    # Custom React hooks
│   │   ├── services/                 # API service layer (Axios)
│   │   ├── store/                    # Zustand state management
│   │   ├── utils/                    # Helper functions
│   │   ├── styles/                   # Global styles
│   │   ├── context/                  # React contexts (Theme, Auth)
│   │   └── constants/                # App constants
│   ├── index.html
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── package.json
│
├── docker-compose.yml                # Root orchestration
└── README.md
```

---

## Proposed Changes — Phase by Phase

---

### Phase 1: Foundation & Infrastructure

Set up the entire project skeleton, configuration, Docker, and development environment.

---

#### Backend Foundation

##### [MODIFY] [settings.py](file:///d:/PROJECT%20ALL/Weather/backend/backend/settings.py)
- Complete rewrite to production-ready settings with environment variable support
- Split into `base.py`, `development.py`, `production.py`
- Configure: DRF, JWT, CORS, Channels, Celery, Redis, PostgreSQL, media/static

##### [NEW] [base.py](file:///d:/PROJECT%20ALL/Weather/backend/backend/settings/base.py)
- Base settings shared across environments
- All 20 apps registered
- DRF configuration with JWT default auth
- CORS headers for frontend
- Celery configuration
- Channels configuration
- Media/static file handling

##### [NEW] [development.py](file:///d:/PROJECT%20ALL/Weather/backend/backend/settings/development.py)
- SQLite database (fallback), debug toolbar, console email backend

##### [NEW] [production.py](file:///d:/PROJECT%20ALL/Weather/backend/backend/settings/production.py)
- PostgreSQL, Redis cache, proper security headers, S3 storage ready

##### [MODIFY] [urls.py](file:///d:/PROJECT%20ALL/Weather/backend/backend/urls.py)
- API versioning: `/api/v1/`
- Include all app URL patterns
- Swagger/OpenAPI docs at `/api/docs/`

##### [NEW] [asgi.py](file:///d:/PROJECT%20ALL/Weather/backend/backend/asgi.py) (modify existing)
- Configure Django Channels ASGI application with WebSocket routing

##### [NEW] [celery.py](file:///d:/PROJECT%20ALL/Weather/backend/backend/celery.py)
- Celery app configuration with autodiscover

##### [NEW] requirements/
- `base.txt`: Django, DRF, SimpleJWT, Channels, Celery, Redis, Pillow, etc.
- `dev.txt`: Debug toolbar, factory_boy, pytest
- `prod.txt`: Gunicorn, psycopg2, whitenoise, sentry-sdk

##### [NEW] .env.example
- All environment variables documented

##### [NEW] Dockerfile & docker-compose.yml
- Multi-stage Docker build
- Services: Django, PostgreSQL, Redis, Celery worker, Celery beat

---

#### Frontend Foundation

##### [NEW] Frontend Vite Project
- Initialize with `npx create-vite@latest`
- Install: Tailwind CSS v3, Framer Motion, React Router, Axios, Zustand, Recharts, Lucide React icons
- Custom Tailwind config with glassmorphism design tokens
- Global CSS with custom properties for theme system

---

### Phase 2: Core Backend Apps (Models, Serializers, Views, URLs)

##### [NEW] apps/core/
- `models.py`: `TimeStampedModel` (abstract), `UUIDModel`
- `mixins.py`: `SerializerContextMixin`, `CacheMixin`
- `permissions.py`: `IsOwner`, `IsPremiumUser`, `IsAdminUser`
- `pagination.py`: `StandardResultsPagination`
- `exceptions.py`: Custom exception handler
- `utils.py`: Common utilities

##### [NEW] apps/users/
- `models.py`: Custom `User` model (extending `AbstractUser`), `UserProfile`, `UserDevice`, `OTPVerification`
- `serializers.py`: Registration, login, profile, device serializers
- `views.py`: Auth views (signup, login, logout, token refresh, OTP, Google OAuth, password reset, change password, email verify)
- `urls.py`: Auth and profile endpoints
- `managers.py`: Custom user manager
- `signals.py`: Auto-create profile on user creation
- `backends.py`: Custom auth backends (email + phone)
- `admin.py`: Custom user admin

##### [NEW] apps/weather/
- `models.py`: `WeatherData`, `CurrentWeather`, `WeatherSource`
- `serializers.py`: Weather data serializers
- `views.py`: Current weather, hyperlocal weather
- `services.py`: OpenWeatherMap API integration service
- `tasks.py`: Celery tasks for periodic weather fetching
- `urls.py`

##### [NEW] apps/forecasts/
- `models.py`: `HourlyForecast`, `DailyForecast`, `WeeklyForecast`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Forecast data aggregation

##### [NEW] apps/alerts/
- `models.py`: `WeatherAlert`, `AlertRule`, `AlertHistory`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Alert evaluation engine
- `tasks.py`: Periodic alert checking

##### [NEW] apps/ai_engine/
- `models.py`: `ChatSession`, `ChatMessage`, `AIInsight`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: AI service with pluggable LLM backend

##### [NEW] apps/radar/
- `models.py`: `RadarFrame`, `RadarLayer`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Radar tile fetching

##### [NEW] apps/locations/
- `models.py`: `SavedLocation`, `LocationSearch`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Geocoding service

##### [NEW] apps/notifications/
- `models.py`: `Notification`, `NotificationPreference`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Multi-channel notification delivery
- `tasks.py`: Async notification sending

##### [NEW] apps/analytics/
- `models.py`: `UserActivity`, `WeatherQuery`, `DashboardMetric`
- `serializers.py`, `views.py`, `urls.py`

##### [NEW] apps/subscriptions/
- `models.py`: `Plan`, `Subscription`, `Payment`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Subscription management

##### [NEW] apps/api_logs/
- `models.py`: `APILog`
- `middleware.py`: Request/response logging middleware

##### [NEW] apps/settings_manager/
- `models.py`: `AppSetting`, `FeatureFlag`
- `serializers.py`, `views.py`, `urls.py`

##### [NEW] apps/admin_panel/
- `views.py`: Admin dashboard API views
- `urls.py`: Admin-specific endpoints

##### [NEW] apps/websocket_server/
- `consumers.py`: Weather update consumer, alert consumer
- `routing.py`: WebSocket URL routing

##### [NEW] apps/recommendations/
- `models.py`: `Recommendation`, `ActivitySuggestion`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Recommendation engine

##### [NEW] apps/health_weather/
- `models.py`: `HealthIndex`, `PollenData`, `UVIndex`, `AQIData`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Health impact calculation

##### [NEW] apps/farming_weather/
- `models.py`: `CropWeather`, `SoilMoisture`, `FarmingAlert`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Agricultural weather analysis

##### [NEW] apps/reports/
- `models.py`: `WeatherReport`
- `serializers.py`, `views.py`, `urls.py`
- `services.py`: Report generation (PDF/JSON)

##### [NEW] apps/cache_system/
- `services.py`: Redis cache wrapper
- `decorators.py`: Cache decorators
- `management/commands/`: Cache management commands

---

### Phase 3: Authentication System (Complete)

Implement in `apps/users/`:

| Feature | Endpoint | Method |
|---------|----------|--------|
| Signup | `/api/v1/auth/signup/` | POST |
| Login | `/api/v1/auth/login/` | POST |
| Logout | `/api/v1/auth/logout/` | POST |
| Token Refresh | `/api/v1/auth/token/refresh/` | POST |
| OTP Request | `/api/v1/auth/otp/request/` | POST |
| OTP Verify | `/api/v1/auth/otp/verify/` | POST |
| Google OAuth | `/api/v1/auth/google/` | POST |
| Password Reset Request | `/api/v1/auth/password/reset/` | POST |
| Password Reset Confirm | `/api/v1/auth/password/reset/confirm/` | POST |
| Change Password | `/api/v1/auth/password/change/` | POST |
| Email Verify | `/api/v1/auth/email/verify/` | POST |
| Profile | `/api/v1/users/profile/` | GET/PUT/PATCH |
| Settings | `/api/v1/users/settings/` | GET/PUT |
| Devices | `/api/v1/users/devices/` | GET/DELETE |

---

### Phase 4: Weather Feature APIs

| Feature | Endpoint |
|---------|----------|
| Current Weather | `/api/v1/weather/current/` |
| Hyperlocal Weather | `/api/v1/weather/hyperlocal/` |
| Hourly Forecast | `/api/v1/forecasts/hourly/` |
| Daily Forecast | `/api/v1/forecasts/daily/` |
| Weekly Forecast | `/api/v1/forecasts/weekly/` |
| Weather Alerts | `/api/v1/alerts/` |
| AQI Data | `/api/v1/health/aqi/` |
| UV Index | `/api/v1/health/uv/` |
| Pollen Data | `/api/v1/health/pollen/` |
| Radar Frames | `/api/v1/radar/frames/` |
| AI Chat | `/api/v1/ai/chat/` |
| Saved Locations | `/api/v1/locations/` |
| Recommendations | `/api/v1/recommendations/` |
| Farming Weather | `/api/v1/farming/` |
| Reports | `/api/v1/reports/` |
| Notifications | `/api/v1/notifications/` |
| Subscriptions | `/api/v1/subscriptions/` |
| Analytics | `/api/v1/analytics/` |

WebSocket: `ws://host/ws/weather/<location_id>/`

---

### Phase 5: Frontend (React + Vite + Tailwind)

#### Design System
- Custom Tailwind config with glassmorphism tokens
- CSS custom properties for dark/light theme switching
- Google Fonts: **Inter** (body), **Outfit** (headings)
- Color palette: Deep blues, vibrant cyans, warm gradients
- Glass cards with `backdrop-blur`, subtle borders, and shadows

#### Pages
| Page | Route | Description |
|------|-------|-------------|
| Landing | `/` | Hero with live weather, feature showcase |
| Dashboard | `/dashboard` | Main weather dashboard (default after login) |
| Login | `/login` | Auth form with glass UI |
| Signup | `/signup` | Registration form |
| Forecast | `/forecast` | Detailed forecasts (hourly/daily/weekly) |
| Radar | `/radar` | Interactive weather radar map |
| Alerts | `/alerts` | Smart alert management |
| AQI | `/aqi` | Air quality monitoring |
| AI Assistant | `/assistant` | AI weather chatbot |
| Health | `/health` | Health weather dashboard |
| Farming | `/farming` | Agricultural weather |
| Settings | `/settings` | User preferences |
| Profile | `/profile` | User profile management |
| Subscription | `/premium` | Premium plans |

#### Key Components
- `GlassCard` — Glassmorphism card with blur and transparency
- `WeatherWidget` — Current weather display with animations
- `ForecastChart` — Recharts-based forecast visualization
- `TemperatureGauge` — Animated temperature display
- `AQIGauge` — Circular AQI indicator
- `RadarMap` — Interactive radar with Leaflet
- `AlertBanner` — Animated alert notifications
- `ChatBubble` — AI assistant chat interface
- `ThemeToggle` — Dark/light mode switch with animation
- `MobileNav` — Bottom navigation for mobile

#### State Management (Zustand)
- `useAuthStore` — Authentication state
- `useWeatherStore` — Weather data
- `useThemeStore` — Theme preferences
- `useNotificationStore` — Notifications
- `useLocationStore` — Location management

#### Key Features
- **Offline Support**: Service worker + localStorage caching
- **PWA**: Manifest, offline page, installable
- **Animations**: Page transitions, weather icon animations, loading skeletons
- **Responsive**: Mobile-first with breakpoints at sm/md/lg/xl

---

### Phase 6: Polish, DevOps & Documentation

- Docker Compose for full stack
- Environment configuration
- API documentation (Swagger)
- README with setup instructions
- Error handling and loading states
- Performance optimization
- Accessibility audit

---

## Verification Plan

### Automated Tests
```bash
# Backend
cd backend
python manage.py test --verbosity=2
python manage.py check --deploy

# Frontend
cd frontend
npm run build    # Verify production build succeeds
npm run lint     # Code quality check
```

### Manual Verification
- Run `python manage.py runserver` and verify API endpoints via browser/curl
- Run `npm run dev` and verify all pages render correctly
- Test dark/light mode toggle
- Test responsive layout at mobile/tablet/desktop breakpoints
- Verify JWT auth flow (signup → login → access protected endpoint)
- Test WebSocket connection for real-time updates

### Browser Testing
- Navigate through all pages
- Verify animations and transitions
- Test form submissions
- Verify error states and loading states
