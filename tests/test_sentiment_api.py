from fastapi.testclient import TestClient
from backend.app import app, news_store, sentiment_store
from config import STUDENT_ID

client = TestClient(app)

def test_analyze_and_get_sentiment():
    # Наповнюємо новинами
    news_store[STUDENT_ID] = [
        {"title": "Great success!", "link": "", "published": ""},
        {"title": "Terrible disaster", "link": "", "published": ""},
        {"title": "This is something", "link": "", "published": ""}
    ]

    # Аналіз
    res = client.post(f"/analyze/{STUDENT_ID}")
    assert res.status_code == 200
    assert res.json() == {"positive": 1, "neutral": 1, "negative": 1}

    # Отримання
    res2 = client.get(f"/sentiment/{STUDENT_ID}")
    assert res2.status_code == 200
    assert res2.json() == {"positive": 1, "neutral": 1, "negative": 1}
