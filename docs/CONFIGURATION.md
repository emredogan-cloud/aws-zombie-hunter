# Configuration Guide

## AWS Credentials Setup

### .env File (Recommended)

Create `.env` file in project root:

```env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
```

**Security Note:** Add `.env` to `.gitignore` to prevent credential leakage.

```bash
echo ".env" >> .gitignore
```

### Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
```

### AWS CLI Configuration

```bash
aws configure
# Interactive setup:
# AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name [None]: us-east-1
# Default output format [None]: json
```

## IAM Permissions

Minimum required IAM policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeVolumes",
        "ec2:DescribeRegions"
      ],
      "Resource": "*"
    }
  ]
}
```

## Command-Line Options

### Scan All Regions

```bash
python main.py
```

### Scan Specific Regions

```bash
python main.py --regions us-east-1 eu-west-1 ap-southeast-1
```

### Control Parallel Workers

```bash
python main.py --workers 10
# Default: 5 workers
# Range: 1-20 recommended
```

### Generate JSON Reports

```bash
python main.py --json-output
```

Outputs both `zombie_volumes.csv` and `zombie_volumes.json`

## Output Files

### CSV Report

`zombie_volumes.csv` — Consolidated report

Columns:
- Region
- VolumeId
- Size (GB)
- CreateTime
- AvailabilityZone
- IOPS
- Throughput

### JSON Report (Optional)

`zombie_volumes.json` — Regional breakdown

```json
{
  "us-east-1": [
    {
      "VolumeId": "vol-12345678",
      "Size": 100,
      "CreateTime": "2024-01-15T10:30:00",
      "AvailabilityZone": "us-east-1a",
      "Encrypted": false,
      "Iops": 3000
    }
  ]
}
```

## Performance Tuning

### For Large Organizations (10K+ volumes)

```bash
python main.py --workers 15
```

### For Resource-Constrained Environments

```bash
python main.py --workers 2
```

### Balanced Configuration (Default)

```bash
python main.py --workers 5
```

## Logging Configuration

Edit logging level in `main.py` if needed:

```python
logging.basicConfig(level=logging.DEBUG)  # More verbose
# or
logging.basicConfig(level=logging.WARNING)  # Less verbose
```

## Next Steps

- Read [USAGE.md](./USAGE.md) for practical examples
- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues
- Check [ARCHITECTURE.md](./ARCHITECTURE.md) for technical details
