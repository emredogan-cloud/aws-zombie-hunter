AWS Zombie Resource Hunter

## Architecture Diagram

![Architecture](docs/ZombieHunter.png)


## Features
- **Automatic Discovery:** Scans and identifies orphaned disks in seconds using the AWS API.
- **Smart Filtering:** Specifically targets resources stuck in the `available` state.
- **Detailed Reporting:** Exports discovered resources into a CSV format (VolumeId, Size, Region, etc.).
- **Secure:** Loads AWS credentials from a `.env` file (don’t hardcode secrets).
- **Logging:** Tracks every operation with timestamps and severity levels.

## Tech Stack
- Python 3.x
- boto3 (AWS SDK for Python)
- python-dotenv
- CSV reporting

## Installation
```bash
git clone https://github.com/emredogan-cloud/aws-zombie-hunter.git
cd aws-zombie-hunter
pip install -r requirements.txt


python app.py

Upon completion, a zombie_resources.csv file will be generated in the project folder.

