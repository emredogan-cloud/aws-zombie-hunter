# Usage Guide

## Quick Examples

### Scan All Regions

```bash
python main.py
```

Output:
```
2024-02-25 21:45:12 - INFO - AWS connection established successfully.
2024-02-25 21:45:13 - INFO - Scanning region: us-east-1
2024-02-25 21:45:14 - INFO - Region us-east-1: Found 3 unattached volumes

✅ Report generated: zombie_volumes.csv
📊 Total zombie volumes: 15
```

### Scan Specific Regions

```bash
python main.py --regions us-east-1 eu-west-1 ap-southeast-1
```

### High-Speed Enterprise Audit

```bash
python main.py --workers 15
```

### Generate Both CSV and JSON Reports

```bash
python main.py --json-output
```

Creates:
- `zombie_volumes.csv` — Consolidated list
- `zombie_volumes.json` — Regional breakdown

## Real-World Scenarios

### Scenario 1: Weekly Cost Audit

```bash
# Run weekly scan and save results
python main.py --json-output > scan_$(date +%Y-%m-%d).log

# Extract total cost estimate
grep "Estimated Monthly Cost" zombie_volumes.csv
```

### Scenario 2: Production Region Compliance Check

```bash
python main.py --regions us-east-1 eu-west-1 \
  --workers 10 \
  --json-output
```

### Scenario 3: Disaster Recovery Validation

```bash
python main.py --regions us-west-2 eu-central-1
```

### Scenario 4: Automated Scheduled Scan

```bash
# Add to crontab for daily 2 AM scans
0 2 * * * cd /opt/aws-zombie-hunter && python main.py --json-output
```

## Understanding Output

### CSV Format

```csv
Region,VolumeId,Size (GB),CreateTime,AvailabilityZone,IOPS,Throughput
us-east-1,vol-12345678,100,2024-01-15T10:30:00,us-east-1a,3000,125
eu-west-1,vol-87654321,50,2024-02-10T15:20:00,eu-west-1a,1000,62
```

### Console Summary

```
======================================================================
🔍 AWS ZOMBIE HUNTER - SCAN SUMMARY
======================================================================

  📍 Region: us-east-1
     - Zombie Volumes: 3
     - Total Size: 250 GB

  📍 Region: eu-west-1
     - Zombie Volumes: 2
     - Total Size: 150 GB

----------------------------------------------------------------------
  📊 TOTAL ACROSS ALL REGIONS:
     - Zombie Volumes: 5
     - Total Wasted Storage: 400 GB
     - Estimated Monthly Cost: $40.00 USD (avg)
======================================================================
```

## Performance Tips

### Tip 1: Fast Multi-Region Scan

```bash
python main.py --workers 10
# Scans 15 regions in ~3-5 seconds
```

### Tip 2: Targeted Regional Audit

```bash
python main.py --regions us-east-1 eu-west-1
# Faster scan of critical regions only
```

### Tip 3: Batch Processing

```bash
# Run daily and archive
python main.py > results_$(date +%Y-%m-%d).txt
```

## Integration Examples

### GitHub Actions Workflow

```yaml
name: AWS Cost Audit
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly

jobs:
  zombie-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run scan
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET }}
        run: python main.py --json-output
      - name: Upload results
        run: aws s3 cp zombie_volumes.* s3://audit-bucket/
```

### CloudWatch Integration

```python
import boto3
from main import AWSZombieHunter

hunter = AWSZombieHunter()
results = hunter.scan_all_regions_parallel()
volumes = hunter.consolidate_results(results)

# Send metrics
cloudwatch = boto3.client('cloudwatch')
cloudwatch.put_metric_data(
    Namespace='CostOptimization',
    MetricData=[
        {
            'MetricName': 'ZombieVolumesCount',
            'Value': len(volumes),
            'Unit': 'Count'
        }
    ]
)
```

## Troubleshooting Usage

### No Results Found

```bash
# Check if volumes exist with explicit region
python main.py --regions us-east-1
```

### Slow Scanning

```bash
# Increase worker threads
python main.py --workers 20
```

### Out of Memory

```bash
# Use fewer workers and stream processing
python main.py --workers 2
```

### AWS Credential Error

```bash
# Verify credentials
aws sts get-caller-identity

# Or check environment
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
```

## Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) for technical details
- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues
- Check [CONFIGURATION.md](./CONFIGURATION.md) for detailed setup
