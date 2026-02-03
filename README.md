AWS Zombie Resource Hunter

## Architecture Diagram

![Architecture](docs/ZombieHunter.png)


An automation tool designed to automatically detect and report "forgotten," cost-incurring, and unused (Available state) EBS volumes within an AWS account.
🚀 Features

    Automatic Discovery: Scans and identifies orphaned disks in seconds using the AWS API.

    Smart Filtering: Specifically targets resources stuck in the available state.

    Detailed Reporting: Exports discovered resources into a CSV format including details such as ID, Size, and Creation Date.

    Secure: Loads AWS credentials from a .env file to ensure no sensitive data is hardcoded.

    Logging: Tracks every operation with timestamps and severity levels for better debugging.

🛠️ Tech Stack

    Python 3.x

    Boto3 (AWS SDK for Python)

    CSV (Reporting)

    Dotenv (Environment Variable Management)

    ⚙️ Installation

    Clone the repository to your local machine:
    Bash

    git clone https://github.com/emredogan-cloud/aws-zombie-hunter.git
    cd aws-zombie-hunter

    Install the required dependencies:

pip install -r requirements.txt

Configure your environment variables: Create a .env file in the root directory and add your AWS credentials:
Kod snippet'i

AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_preferred_region


Configure your environment variables: Create a .env file in the root directory and add your AWS credentials:
    Kod snippet'i

    AWS_ACCESS_KEY_ID=your_access_key
    AWS_SECRET_ACCESS_KEY=your_secret_key
    AWS_REGION=your_preferred_region

📋 Usage

Run the main script to start the discovery process:
Bash

python app.py

Upon completion, a zombie_resources.csv file will be generated in the project folder.
