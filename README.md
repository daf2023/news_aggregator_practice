
Цей проєкт — навчальний **агрегатор новин**, який:
- отримує новини з RSS-джерел
- проводить аналіз тональності заголовків
- виводить дані на простий веб-інтерфейс
- реалізований із використанням **FastAPI**, **JavaScript**, **Docker**, **CI/CD**

---

##  Технології

-  **Python 3.10+**, **FastAPI**
-  `feedparser` — для читання RSS
-  `vaderSentiment` — для аналізу тональності
-  **HTML/CSS/JS (frontend)**
-  **Docker** + `docker-compose`
-  **GitHub Actions** — автоматичне тестування

---

## 🚀 Запуск

### 🔧 Локальний запуск (без Docker)

 **Backend:**
   ```bash
   uvicorn backend.app:app --reload

Запуск у Docker

docker compose up --build
 http://localhost:8001 — інтерфейс

 http://localhost:8000/docs — Swagger UI

pytest tests

Структура проєкту

news_aggregator_practice/
 backend/
 app.py
 frontend/
  index.html
canvas.js
tests/
test_sources_api.py
 test_sentiment_api.py
config.py
requirements.txt
 docker-compose.yml
.github/workflows/ci.yml

Автор
 Артем Філоненко
 Студентська робота з предмету “Основи розробки програмних систем”