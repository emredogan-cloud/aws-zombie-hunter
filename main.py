import boto3
import os
import logging
import csv
from dotenv import load_dotenv

# Loglama ayarları (Ekrana renkli ve tarihli bilgi basar)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AWSResourceManager:
    def __init__(self):
        # 1. Ortam değişkenlerini yükle
        load_dotenv()
        
        # 2. Şifreleri çek
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_key = os.getenv("AWS_SECRET_KEY")
        self.region = os.getenv("REGION")

        try:
            # 3. AWS Bağlantısını Kur
            self.ec2 = boto3.client(
                'ec2',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.region
            )
            logging.info("AWS bağlantısı başarıyla kuruldu! 🚀")

        except Exception as e:
            logging.error(f"Bağlantı hatası: {e}")

    def get_zombie_volumes(self) -> list:
        """Kullanılmayan (Available) durumdaki diskleri bulur."""
        logging.info("Sahipsiz diskler aranıyor...")
        try:
            response = self.ec2.describe_volumes(
                Filters=[
                    {
                        'Name': 'status',
                        'Values': ['available']
                    }
                ]
            )
            diskler = response['Volumes']
            logging.info(f"Tarama bitti. Bulunan sahipsiz disk sayısı: {len(diskler)}")
            return diskler

        except Exception as e:
            logging.error(f"Diskler listelenemedi: {e}")
            return []

    def save_to_csv(self, volumes : list) -> None:
        """Disk listesini CSV dosyasına kaydeder."""
        dosya_adi = 'zombie_diskler.csv'
        basliklar = ['VolumeId', 'Size', 'CreateTime', 'AvailabilityZone']

        try:
            with open(dosya_adi, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=basliklar)
                writer.writeheader()

                for vol in volumes:
                    satir = {
                        'VolumeId': vol['VolumeId'],
                        'Size': vol['Size'],
                        'CreateTime': vol['CreateTime'],
                        'AvailabilityZone': vol['AvailabilityZone']
                    }
                    writer.writerow(satir)
            
            logging.info(f"✅ Rapor başarıyla kaydedildi: {dosya_adi}")
            print(f"\nDosya konumu: {os.getcwd()}/{dosya_adi}")

        except Exception as e:
            logging.error(f"CSV hatası: {e}")

# --- ANA ÇALIŞTIRMA BLOĞU ---
if __name__ == "__main__":
    # Nesneyi oluştur
    bot = AWSResourceManager()
    
    # Diskleri bul
    diskler = bot.get_zombie_volumes()
    
    # Varsa kaydet
    if diskler:
        bot.save_to_csv(diskler)
    else:
        logging.info("Sistem temiz, kaydedilecek disk yok.")