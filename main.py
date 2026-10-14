from fastapi import FastAPI

app = FastAPI(
    title="Sahte Site Avcıları API",
    description="4 Modüllü Tespit Sistemi Backend İskeleti"
)

@app.get("/")
def read_root():
    return {"mesaj": "Sahte Site Avcıları API başarıyla çalışıyor!"}

@app.post("/api/analyze")
def analyze_url(url: str):
    return {
        "durum": "basarili",
        "analiz_edilen_url": url,
        "mesaj": "Analiz motoru (XGBoost/Random Forest) buraya entegre edilecek."
    }