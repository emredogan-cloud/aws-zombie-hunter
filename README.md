# 🕵️ AWS Zombie Resource Hunter

AWS hesabında "unutulmuş" ve maliyet oluşturan kullanılmayan (Available durumdaki) EBS disklerini otomatik olarak tespit eden ve raporlayan bir otomasyon aracıdır.

## 🚀 Özellikler

- **Otomatik Keşif:** AWS API'sini kullanarak sahipsiz diskleri saniyeler içinde bulur.
- **Akıllı Filtreleme:** Sadece `available` durumundaki kaynakları hedefler.
- **Raporlama:** Bulunan kaynakları detaylarıyla birlikte (ID, Boyut, Tarih) `CSV` formatında dışa aktarır.
- **Güvenli:** AWS kimlik bilgilerini `.env` dosyasından okur, kod içine gömmez.
- **Loglama:** Her adımı tarih ve önem derecesiyle loglar.

## 🛠️ Kullanılan Teknolojiler

- **Python 3.x**
- **Boto3** (AWS SDK)
- **CSV** (Raporlama)
- **Dotenv** (Çevre Değişkenleri Yönetimi)

## ⚙️ Kurulum

1. Projeyi bilgisayarınıza indirin:
   ```bash
   git clone [https://github.com/emredogan-cloud/aws-zombie-hunter.git](https://github.com/emredogan-cloud/aws-zombie-hunter.git)

   cd aws-zombie-hunter
