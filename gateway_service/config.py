class Config:
    AUTH_SERVICE_URL = "http://auth_service:8001"  # Authentication Service
    QUESTION_SERVICE_URL = "http://question_service:8002"  # Question Generation Service
    QUESTIONS_HISTORY_SERVICE_URL = "http://questions_history_service:8003"  # Questions History Service

class Config_dev:
    AUTH_SERVICE_URL = "http://localhost:8001"  # Authentication Service
    QUESTION_SERVICE_URL = "http://localhost:8002"  # Question Generation Service
    QUESTIONS_HISTORY_SERVICE_URL = "http://localhost:8003"  # Questions History Service