# Installation Guide

## Prerequisites

- Python 3.7+
- AWS Account with valid credentials
- pip (Python package manager)

## Step 1: Clone Repository

```bash
git clone https://github.com/emredogan-cloud/aws-zombie-hunter.git
cd aws-zombie-hunter
```

## Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure AWS Credentials

### Option 1: `.env` File (Recommended for Development)

Create a `.env` file in the project root:

```env
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=us-east-1
```

### Option 2: AWS CLI Configuration

```bash
aws configure
```

### Option 3: Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
```

## Step 5: Verify Installation

```bash
python main.py --help
```

Expected output:
```
usage: main.py [-h] [--regions REGIONS [REGIONS ...]] [--workers WORKERS] [--json-output]

optional arguments:
  -h, --help            show this help message and exit
  --regions REGIONS     Specific regions to scan (default: all)
  --workers WORKERS     Parallel worker threads (default: 5)
  --json-output         Generate JSON + CSV reports
```

## Troubleshooting Installation

### `ModuleNotFoundError: No module named 'boto3'`

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### `aws: command not found`

Install AWS CLI:
```bash
pip install awscli
```

### AWS Credential Errors

Verify your credentials are properly configured:
```bash
aws sts get-caller-identity
```

This should return your AWS account information.

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.7 | 3.10+ |
| RAM | 256MB | 512MB |
| Disk | 50MB | 100MB |
| Network | 1 Mbps | 10 Mbps |

## Next Steps

- Read [CONFIGURATION.md](./CONFIGURATION.md) for detailed setup
- Check [USAGE.md](./USAGE.md) for command examples
- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues
