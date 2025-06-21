from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import feedparser
from config import STUDENT_ID, SOURCES


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "http://127.0.0.1:8001"],  # ✅ обидва варіанти
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




# Глобальні сховища
store = {STUDENT_ID: SOURCES.copy()}
news_store = {STUDENT_ID: []}
sentiment_store = {STUDENT_ID: {}}


@app.get("/sources/{student_id}")
def get_sources(student_id: str):
    if student_id != STUDENT_ID:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"sources": store[student_id]}


@app.post("/sources/{student_id}")
def add_source(student_id: str, payload: dict):
    if student_id != STUDENT_ID:
        raise HTTPException(status_code=404, detail="Student not found")
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    store[student_id].append(url)
    return {"sources": store[student_id]}


@app.post("/fetch/{student_id}")
def fetch_news(student_id: str):
    if student_id != STUDENT_ID:
        raise HTTPException(status_code=404, detail="Student not found")
    news_store[student_id].clear()
    for url in store[student_id]:
        feed = feedparser.parse(url)
        for entry in getattr(feed, "entries", []):
            news_store[student_id].append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", "")
            })
    return {"fetched": len(news_store[student_id])}


@app.get("/news/{student_id}")
def get_news(student_id: str):
    if student_id not in news_store:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"articles": news_store[student_id]}


@app.post("/analyze/{student_id}")
def analyze_news(student_id: str):
    if student_id not in news_store:
        raise HTTPException(status_code=404, detail="Student not found")

    analyzer = SentimentIntensityAnalyzer()
    scores = {"positive": 0, "neutral": 0, "negative": 0}

    for item in news_store[student_id]:
        sentiment = analyzer.polarity_scores(item["title"])
        compound = sentiment["compound"]
        if compound >= 0.05:
            scores["positive"] += 1
        elif compound <= -0.05:
            scores["negative"] += 1
        else:
            scores["neutral"] += 1

    sentiment_store[student_id] = scores
    return scores


@app.get("/sentiment/{student_id}")
def get_sentiment(student_id: str):
    if student_id not in sentiment_store:
        raise HTTPException(status_code=404, detail="Student not found")
    return sentiment_store[student_id]
