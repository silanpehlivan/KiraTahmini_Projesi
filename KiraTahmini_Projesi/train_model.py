import pandas as pd
import numpy as np
import pickle

# Modelleme ve değerlendirme için gerekli sklearn bileşenleri
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# Gradient Boosting tabanlı modeller
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

import warnings

# Gereksiz uyarıları kapat
warnings.filterwarnings('ignore')

def train():
    """
    İstanbul kira verisi ile modeli eğiten,
    performansı ölçen ve modeli diske kaydeden ana fonksiyon
    """

    print("Veri yükleniyor...")

    
    # VERİ OKUMA (ENCODING SORUNLARI İÇİN)
    
    # Türkçe karakterler nedeniyle farklı encoding'ler denenir
    try:
        df = pd.read_csv('data/istanbulApartmentForRent.csv', encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv('data/istanbulApartmentForRent.csv', encoding='iso-8859-9')
        except:
            df = pd.read_csv('data/istanbulApartmentForRent.csv', encoding='cp1254')

    print(f"Veri boyutu: {df.shape}")

    
    # ÖN İŞLEME (PREPROCESSING)
    
    # CSV kolonları:
    # district, neighborhood, room, living room, area (m2), age, floor, price

    # Aynı satırları (duplicate) kaldır
    df = df.drop_duplicates()

   
    # OUTLIER TEMİZLEME
    
    # Aşırı uç değerler modeli bozabileceği için
    # mantıksız fiyat ve metrekare değerleri filtrelenir
    df = df[df['price'] < 200000]       # Çok yüksek fiyatlar çıkarılır
    df = df[df['area (m2)'] < 500]      # Çok büyük daireler çıkarılır

    
    # KATEGORİK DEĞİŞKENLERİN ENCODE EDİLMESİ
    
    # İlçe ve mahalle için Label Encoding kullanılır
    le_district = LabelEncoder()
    le_neighborhood = LabelEncoder()

    # String temizliği (boşluklar vb.) + encoding
    df['district'] = le_district.fit_transform(
        df['district'].astype(str).str.strip()
    )
    df['neighborhood'] = le_neighborhood.fit_transform(
        df['neighborhood'].astype(str).str.strip()
    )

   
    # FEATURE / TARGET AYRIMI
    
    X = df[
        ['district', 'neighborhood', 'room',
         'living room', 'area (m2)', 'age', 'floor']
    ]
    y = df['price']

    # Eğitim ve test verisini ayır (80% - 20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Modeller eğitiliyor...")

    
    # BASE MODELLER
    

    # Random Forest Regressor
    rf = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    # XGBoost Regressor
    xgb = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        n_jobs=-1,
        random_state=42
    )

    # CatBoost Regressor
    cat = CatBoostRegressor(
        iterations=500,
        learning_rate=0.05,
        verbose=0,
        random_state=42
    )

   
    # STACKING REGRESSOR
    
    # Birden fazla güçlü modeli birleştirerek
    # daha yüksek doğruluk elde edilir
    estimators = [
        ('rf', rf),
        ('xgb', xgb),
        ('cat', cat)
    ]

    stacking_regressor = StackingRegressor(
        estimators=estimators,
        final_estimator=LinearRegression(),
        n_jobs=-1
    )

    # Modeli eğit
    stacking_regressor.fit(X_train, y_train)

    
    # MODEL DEĞERLENDİRME
   
    y_pred = stacking_regressor.predict(X_test)

    # R² skoru ve Ortalama Mutlak Hata
    score = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Stacking R2 Skoru: {score:.4f}")
    print(f"MAE: {mae:.2f}")

    # BASE MODELLERİN AYRI AYRI PERFORMANSI
  
    rf.fit(X_train, y_train)
    print(f"RandomForest R2: {r2_score(y_test, rf.predict(X_test)):.4f}")

    xgb.fit(X_train, y_train)
    print(f"XGBoost R2: {r2_score(y_test, xgb.predict(X_test)):.4f}")

    cat.fit(X_train, y_train)
    print(f"CatBoost R2: {r2_score(y_test, cat.predict(X_test)):.4f}")

  
    # MODEL VE ENCODER'LARI KAYDET
   
    print("Model ve encoder'lar kaydediliyor...")

    # Eğitilmiş stacking modeli kaydet
    with open('model.pkl', 'wb') as f:
        pickle.dump(stacking_regressor, f)

    # Encoder nesnelerini kaydet
    encoders = {
        'district': le_district,
        'neighborhood': le_neighborhood
    }
    with open('encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)

    print("Eğitim tamamlandı!")

# Script doğrudan çalıştırılırsa train() fonksiyonunu çağır
if __name__ == "__main__":
    train()

