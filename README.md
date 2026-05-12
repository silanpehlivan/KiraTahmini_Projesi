🏠 İstanbul Kiralık Konut Piyasası

Bu proje, İstanbul’daki kiralık konut piyasasına ait veriler kullanılarak makine öğrenmesi yöntemleriyle kira fiyatlarının tahmin edilmesini amaçlamaktadır.  
Bu çalışma, Bitlis Eren Üniversitesi bünyesinde Şilan Pehlivan ve Sevgi Golgiyaz tarafından hazırlanmış bir Makine Öğrenmesi proje raporu kapsamında geliştirilmiştir.

---

🚀 Proje Hakkında

İstanbul gibi dinamik ve heterojen bir konut piyasasında doğru kira tahmini yapmak; kiracılar için adil fiyat değerlendirmesi, ev sahipleri için gerçekçi fiyatlandırma ve piyasa analizi için veriye dayalı kararlar sağlamaktadır.

Bu çalışmada, geleneksel istatistiksel yöntemlerin ötesine geçilerek doğrusal olmayan ve karmaşık ilişkileri yakalayabilen gelişmiş makine öğrenmesi modelleri kullanılmıştır.

---

🧠 Kullanılan Teknolojiler ve Model Mimarisi

Projenin temelini **Yığınlama Regresyonu (Stacking Regressor)** mimarisi oluşturmaktadır.

### 🔹 Temel Öğreniciler (Base Learners)

- Random Forest Regressor  
- XGBoost Regressor  
- CatBoost Regressor  

### 🔹 Meta Öğrenici (Meta Learner)

- Linear Regression  

Temel modellerin çıktıları kullanılarak nihai kira tahmini yapılır.

---

### 🔹 Web Arayüzü

- FastAPI  

Eğitilen modelin son kullanıcıya sunulması amacıyla API tabanlı bir web arayüzü geliştirilmiştir.

---

📊 Model Performansı

Yapılan deneyler sonucunda Stacking Regressor mimarisinin tekil modellere kıyasla daha yüksek performans sunduğu gözlemlenmiştir.

| Model              | R² Skoru | MAE (Ortalama Mutlak Hata) |
|-------------------|----------|-----------------------------|
| Random Forest      | 0.33     | 1.017 TL                    |
| XGBoost            | 0.36     | 1.216 TL                    |
| CatBoost           | 0.37     | 1.416 TL                    |
| Stacking Regressor | 0.40     | 1.616 TL                    |

📌 Modelin genel tahmin başarısı %86 olarak hesaplanmıştır.

---

🔍 Önemli Bulgular (Özellik Önem Analizi)

Model çıktılarının analizine göre İstanbul’da kira fiyatlarını etkileyen en önemli faktörler:

- **Alan (m²):** Konutun büyüklüğü fiyat üzerinde en belirleyici etkendir.  
- **Konum (İlçe & Mahalle):** Coğrafi konum kira değerini doğrudan etkilemektedir.  
- **Bina Yaşı:** Yapının yaşı ve durumu fiyatlandırmada önemli rol oynar.  

---

📂 Veri Seti Özellikleri

Çalışmada kullanılan veri seti 11.627 kayıttan oluşmaktadır.

### 🔹 Girdi Özellikleri

**Coğrafi:**
- İlçe (District)
- Mahalle (Neighborhood)

**Fiziksel:**
- Oda Sayısı
- Salon Sayısı
- Metrekare (Area)
- Bina Yaşı
- Bulunduğu Kat

### 🔹 Hedef Değişken

- Kira Fiyatı (Price)

---

🛠️ Kurulum ve Kullanım

Proje, yerel makinede çalıştırılmak üzere aşağıdaki dosya yapısına sahiptir:

```
├── main.py              # FastAPI uygulaması ve API endpointleri
├── train_model.py       # Model eğitimi ve veri ön işleme
├── static/              # Web arayüzü (HTML, CSS, JS)
└── README.md
```

---

▶️ Model Eğitimi

```bash
python train_model.py
```

---

▶️ API’yi Çalıştırma

```bash
uvicorn main:app --reload
```

---

🎓 Akademik Not

Bu çalışma, Bitlis Eren Üniversitesi akademik gereklilikleri doğrultusunda hazırlanmış olup eğitim ve araştırma amaçlıdır.
