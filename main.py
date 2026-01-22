import boto3
import os
import logging
import csv
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AWSResourceManager:
    def __init__(self):
        load_dotenv()
        
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_key = os.getenv("AWS_SECRET_KEY")
        self.region = os.getenv("REGION")

        try:
            self.ec2 = boto3.client(
                'ec2',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.region
            )
            logging.info("AWS connection established successfully.")

        except Exception as e:
            logging.error(f"Connection error: {e}")

    def get_zombie_volumes(self) -> list:
        logging.info("Scanning for unattached (available) volumes...")
        try:
            response = self.ec2.describe_volumes(
                Filters=[
                    {
                        'Name': 'status',
                        'Values': ['available']
                    }
                ]
            )
            volumes = response['Volumes']
            logging.info(f"Scan complete. Found {len(volumes)} unattached volumes.")
            return volumes

        except Exception as e:
            logging.error(f"Failed to list volumes: {e}")
            return []

    def save_to_csv(self, volumes: list) -> None:
        filename = 'zombie_volumes.csv'
        headers = ['VolumeId', 'Size', 'CreateTime', 'AvailabilityZone']

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()

                for vol in volumes:
                    row = {
                        'VolumeId': vol['VolumeId'],
                        'Size': vol['Size'],
                        'CreateTime': vol['CreateTime'],
                        'AvailabilityZone': vol['AvailabilityZone']
                    }
                    writer.writerow(row)
            
            logging.info(f"Report successfully saved: {filename}")
            print(f"\nFile path: {os.path.join(os.getcwd(), filename)}")

        except Exception as e:
            logging.error(f"CSV error: {e}")

if __name__ == "__main__":
    bot = AWSResourceManager()
    
    volumes = bot.get_zombie_volumes()
    
    if volumes:
        bot.save_to_csv(volumes)
    else:
        logging.info("System is clean. No orphan volumes to save.")
