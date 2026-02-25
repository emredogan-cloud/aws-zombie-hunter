# Troubleshooting Guide

## Credential Issues

### Error: "Unable to locate credentials"

**Cause:** AWS credentials not configured

**Solution:**

```bash
# Option 1: Create .env file
echo "AWS_ACCESS_KEY_ID=your_key" > .env
echo "AWS_SECRET_ACCESS_KEY=your_secret" >> .env

# Option 2: Configure AWS CLI
aws configure

# Option 3: Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

**Verify:**
```bash
aws sts get-caller-identity
# Should output: Account, UserId, Arn
```

### Error: "Access Denied (InvalidUserID.NotFound)"

**Cause:** Invalid AWS credentials

**Solution:**

1. Check credentials in `.env` or environment:
```bash
cat .env | grep AWS_
echo "Key: $AWS_ACCESS_KEY_ID"
```

2. Generate new credentials:
   - Go to AWS IAM Console
   - Create new Access Key
   - Update `.env` file

3. Verify permissions:
```bash
aws ec2 describe-regions
```

### Error: "The security token included in the request is invalid"

**Cause:** Session token expired (if using temporary credentials)

**Solution:**

```bash
# Get new temporary credentials
aws sts assume-role \
  --role-arn arn:aws:iam::ACCOUNT:role/ROLE \
  --role-session-name zombie-scan

# Update environment with new token
export AWS_SECURITY_TOKEN=<SessionToken>
```

---

## Installation Issues

### Error: "ModuleNotFoundError: No module named 'boto3'"

**Cause:** Dependencies not installed

**Solution:**

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python -c "import boto3; print(boto3.__version__)"
```

### Error: "No module named 'python_dotenv'"

**Cause:** Missing python-dotenv package

**Solution:**

```bash
pip install python-dotenv
# or
pip install -r requirements.txt
```

### Error: "command not found: python"

**Cause:** Python not in PATH

**Solution:**

```bash
# Use python3 explicitly
python3 main.py

# Or create alias
alias python=python3
```

---

## Runtime Issues

### No Results Found

**Cause:** No unattached volumes in specified regions

**Solution:**

```bash
# Verify volumes exist
aws ec2 describe-volumes --region us-east-1

# Check for available volumes specifically
aws ec2 describe-volumes \
  --region us-east-1 \
  --filters "Name=status,Values=available"
```

### Slow Scanning

**Cause:** Too few worker threads

**Solution:**

```bash
# Increase workers
python main.py --workers 15

# Or scan specific regions
python main.py --regions us-east-1 eu-west-1
```

### High Memory Usage

**Cause:** Too many workers or large result set

**Solution:**

```bash
# Reduce workers
python main.py --workers 2

# Or scan regions separately
python main.py --regions us-east-1
```

### Timeout During Scan

**Cause:** API throttling or network issues

**Solution:**

```bash
# Reduce worker count (less parallel API calls)
python main.py --workers 2

# Or increase timeout (edit main.py if needed)
# Default paginator handles retries automatically
```

---

## Output Issues

### Error: "Permission denied" when writing CSV

**Cause:** Directory not writable

**Solution:**

```bash
# Check permissions
ls -l

# Make writable
chmod 755 .

# Or run from different directory
cd /tmp
python /path/to/main.py
```

### CSV file is empty

**Cause:** No volumes found or export failed

**Solution:**

```bash
# Check if scan actually found volumes
python main.py | grep "Found"

# Verify file was created
ls -la zombie_volumes.csv

# Check file permissions
cat zombie_volumes.csv | head -20
```

### JSON export not generated

**Cause:** Missing --json-output flag

**Solution:**

```bash
# Explicitly request JSON output
python main.py --json-output

# Verify both files created
ls -la zombie_volumes.*
```

---

## AWS API Issues

### Error: "InvalidParameterCombination"

**Cause:** Invalid filter or region combination

**Solution:**

```bash
# Verify region names are valid
python main.py --regions us-east-1 eu-west-1

# Not:
python main.py --regions USA-EAST-1
```

### Error: "InvalidVolume.NotFound"

**Cause:** Scanning region with no volumes

**Solution:**

This is normal - region simply has no orphaned volumes. No action needed.

### Error: "RequestLimitExceeded"

**Cause:** Too many API calls (throttling)

**Solution:**

```bash
# Reduce worker threads
python main.py --workers 3

# Add delay between requests (built-in pagination handles this)
# Paginator automatically retries with backoff
```

---

## Permission Issues

### Error: "User: arn:aws:iam::123456789:user/zombie is not authorized"

**Cause:** Missing IAM permissions

**Solution:**

Apply minimum required policy to your IAM user:

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

Steps:
1. Go to AWS IAM Console
2. Select your user
3. Add inline policy
4. Paste above JSON

---

## Diagnostic Commands

### Check AWS Configuration

```bash
# Show active credentials
aws sts get-caller-identity

# Show current region
aws configure get region

# List configured profiles
aws configure list
```

### Test EC2 API Access

```bash
# Describe regions
aws ec2 describe-regions

# Describe volumes in region
aws ec2 describe-volumes --region us-east-1

# Count available volumes
aws ec2 describe-volumes \
  --region us-east-1 \
  --filters "Name=status,Values=available" \
  --query 'length(Volumes)'
```

### Check Python Environment

```bash
# Python version
python --version

# Virtual environment active?
which python

# Installed packages
pip list | grep boto3
```

### Test Zombie Hunter

```bash
# Dry run (no write)
python main.py --help

# Single region test
python main.py --regions us-east-1 --workers 1

# With debug logging
python -u main.py 2>&1 | head -50
```

---

## Getting Help

### Collect Debug Information

```bash
# Save debug output
python main.py > debug.log 2>&1

# Check environment
echo "AWS_REGION=$AWS_REGION" >> debug.log
echo "Python: $(python --version)" >> debug.log
pip list >> debug.log
```

### Common Solutions Checklist

- [ ] AWS credentials configured (`aws sts get-caller-identity`)
- [ ] Python 3.7+ installed (`python --version`)
- [ ] Dependencies installed (`pip list | grep boto3`)
- [ ] .env file created (if using .env)
- [ ] IAM permissions granted (ec2:DescribeVolumes)
- [ ] AWS region valid (us-east-1, eu-west-1, etc.)
- [ ] Network connectivity to AWS

### Report an Issue

When reporting issues, include:

```
- Python version: python --version
- AWS region: echo $AWS_REGION
- Worker count: (from command)
- Error message: (full traceback)
- Debug log: (output from `python main.py > debug.log 2>&1`)
```

## Next Steps

- Read [INSTALLATION.md](./INSTALLATION.md) for setup help
- See [CONFIGURATION.md](./CONFIGURATION.md) for config options
- Check [USAGE.md](./USAGE.md) for usage examples
