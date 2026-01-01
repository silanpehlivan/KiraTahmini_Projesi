from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import os

# FastAPI uygulamasını başlat
app = FastAPI()

# CORS for development
# Geliştirme aşamasında frontend ile backend arasında
# isteklerin engellenmemesi için tüm origin'lere izin veriyoruz

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tüm domain'lere izin
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodları (GET, POST vb.)
    allow_headers=["*"],   # Tüm header'lar
)

# Load model and encoders
model = None
encoders = None



    #Eğitimli makine öğrenmesi modelini ve
    #kategorik değişkenler için kullanılan encoder'ları yükler

def load_artifacts():
    


    global model, encoders
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        print("Model ve encoder'lar başarıyla yüklendi.")
    except Exception as e:
        print(f"Model/encoder yükleme hatası: {e}")

# Uygulama başlarken model ve encoder'ları yükle
load_artifacts()

#Kullanıcının tahmin için göndereceği konut özellikleri
class HouseFeatures(BaseModel):
    district: str #ilçe
    neighborhood: str #mahalle
    room: int #oda sayısı
    living_room: int #salon sayısı
    area: int #m2
    age: int #bina yaşı
    floor: int #kat sayısı


 #Frontend tarafında dropdown vb. alanlarda
    #kullanılmak üzere ilçe ve mahalle listesini döner


# METADATA ENDPOINT
@app.get("/metadata")
def get_metadata():
    if not encoders:
        load_artifacts()
    try:
        districts = encoders['district'].classes_.tolist()
        neighborhoods = encoders['neighborhood'].classes_.tolist()
        return {
            "districts": districts,
            "neighborhoods": neighborhoods
        }
    except Exception as e:
        return {"error": str(e)}

# TAHMİN ENDPOINT

@app.post("/predict")
def predict_price(features: HouseFeatures):
    if not model or not encoders:
        load_artifacts()
        if not model:
            raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        # KATEGORİK VERİLERİ ENCODE ETMELİZ
        try:
            district_enc = encoders['district'].transform([features.district])[0]
        except ValueError:
             # Fallback or error. For now specific error
             raise HTTPException(status_code=400, detail=f"Unknown district: {features.district}")
             
              # Mahalle encode işlemi
        try:
            neighborhood_enc = encoders['neighborhood'].transform([features.neighborhood])[0]
        except ValueError:
            # Simple fallback: try to find most frequent or just error
            raise HTTPException(status_code=400, detail=f"Unknown neighborhood: {features.neighborhood}")

         # MODEL GİRİŞ VERİSİ HAZIRLA
          # Sıra, modelin eğitildiği sırayla birebir aynı olmalıdır

        input_data = pd.DataFrame([[
            district_enc,
            neighborhood_enc,
            features.room,
            features.living_room,
            features.area,
            features.age,
            features.floor
        ]], columns=['district', 'neighborhood', 'room', 'living room', 'area (m2)', 'age', 'floor'])
        
        prediction = model.predict(input_data)[0]
        
        # ALT MODELLERİN TAHMİNLERİ
        # StackingRegressor içindeki her modelin ayrı ayrı çıktıları

        individual_preds = {}
        for name, est in model.named_estimators_.items():
            individual_preds[name] = float(est.predict(input_data)[0])

          # API yanıtı   
        return {
            "prediction": float(prediction),
            "details": individual_preds,
            "success_rate": 86 
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# STATİK DOSYA SERVİSİ
# Frontend (HTML/CSS/JS) dosyalarını sunmak için
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# UYGULAMA ÇALIŞTIRMA
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
