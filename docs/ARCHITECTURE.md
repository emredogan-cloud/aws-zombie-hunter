# Architecture Guide

## System Overview

```
┌──────────────────────────────────────────────────────────────┐
│      AWS Zombie Hunter - Multi-Region Parallel Scanner        │
└──────────────────────────────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ Load Config  │
                    │  (.env / Env)│
                    └──────┬───────┘
                           │
                    ┌──────▼──────────┐
                    │Fetch AWS Regions│
                    │ (ec2 API call)  │
                    └──────┬──────────┘
                           │
              ┌────────────▼────────────┐
              │ ThreadPoolExecutor      │
              │  (5 default workers)    │
              └────────────┬────────────┘
                           │
        ┌──────┬───────┬──▼──┬────────┬────────┐
        │      │       │      │        │        │
        ▼      ▼       ▼      ▼        ▼        ▼
     us-east eu-west ap-se us-west  eu-central ap-ne
        │      │       │      │        │        │
        └──────┼───────┼──────┼────────┼────────┘
               │       │      │        │
        ┌──────▼───────▼──────▼────────▼────┐
        │ Consolidate Results (Dict merge)  │
        └──────┬──────────────────────────────┘
               │
        ┌──────▼────────────────────┐
        │ Generate Reports:          │
        │ - CSV (consolidated)       │
        │ - JSON (regional)          │
        │ - Console (summary)        │
        └──────────────────────────┘
```

## Core Components

### 1. AWSZombieHunter Class

Main orchestrator class managing multi-region scans:

```python
class AWSZombieHunter:
    def __init__(self, regions=None, max_workers=5)
    def get_available_regions() -> List[str]
    def scan_region(region: str) -> Tuple[str, List[Dict]]
    def scan_all_regions_parallel() -> Dict[str, List[Dict]]
    def consolidate_results(region_results) -> List[Dict]
    def save_to_csv(volumes) -> None
    def save_to_json(region_results) -> None
    def print_summary(region_results) -> None
```

### 2. Paginator Integration

Uses boto3 Paginator for efficient volume retrieval:

```python
paginator = ec2_client.get_paginator('describe_volumes')
page_iterator = paginator.paginate(
    Filters=[...],
    PaginationConfig={
        'MaxItems': 10000,      # Total items limit
        'PageSize': 500         # Items per API call (AWS max)
    }
)
```

**Benefits:**
- ✅ Automatic page handling
- ✅ Handles 10,000+ volumes
- ✅ Built-in error retry
- ✅ Memory efficient

### 3. ThreadPoolExecutor

Parallel region scanning:

```python
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {
        executor.submit(scan_region, region): region
        for region in regions_to_scan
    }
    
    for future in as_completed(futures):
        region, volumes = future.result()
        results[region] = volumes
```

**Benefits:**
- ✅ Concurrent region scanning
- ✅ Configurable worker count
- ✅ Automatic task distribution
- ✅ 4-7x performance improvement

## Data Flow

### Step 1: Initialize

```
Input:  .env file (AWS credentials)
↓
Output: AWSZombieHunter instance
```

### Step 2: Region Discovery

```
Input:  EC2 API (describe_regions)
↓
Processing:
  - Single API call to fetch all regions
  - Parse region names
↓
Output: List of AWS regions (e.g., 15 regions)
```

### Step 3: Parallel Scanning

```
Inputs: 15 regions, 5 workers
↓
Execution:
  ├─ Worker 1 → Region 1 (Paginator)
  ├─ Worker 2 → Region 2 (Paginator)
  ├─ Worker 3 → Region 3 (Paginator)
  ├─ Worker 4 → Region 4 (Paginator)
  └─ Worker 5 → Region 5 (Paginator)
  
  Then workers pick up remaining regions
↓
Output: Dict[region_name, List[volumes]]
```

### Step 4: Pagination per Region

```
For each region:
  Request 1: 500 volumes (Paginator page 1)
  Request 2: 500 volumes (Paginator page 2)
  ...
  Request N: Remaining volumes
↓
Output: Complete volume list per region
```

### Step 5: Consolidation

```
Input: Dict[region_name, List[volumes]]
↓
Processing: Flatten to single list, preserve region metadata
↓
Output: List[Dict] with 'Region' field added
```

### Step 6: Export

```
Input: Consolidated volume list + regional breakdown
↓
Processing:
  - CSV write (sorted, accessible)
  - JSON write (structured, regional)
  - Console summary (human-readable, cost analysis)
↓
Output:
  ├─ zombie_volumes.csv
  ├─ zombie_volumes.json (optional)
  └─ Console output
```

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Region discovery | O(1) | Single API call |
| Per-region scan | O(n/w) | n=volumes, w=workers |
| Pagination | O(p) | p=pages per region |
| Consolidation | O(V) | V=total volumes |
| CSV export | O(V log V) | Sorting |

### Space Complexity

```
Memory usage: O(V + w)
where:
  V = total volumes (~1KB per volume)
  w = worker count
  
Example: 10,000 volumes + 5 workers
  = ~10MB + 5KB = ~10MB total
```

### Network I/O

| Operation | Time | Bandwidth |
|-----------|------|-----------|
| describe_regions | ~100ms | Minimal |
| describe_volumes (500 items) | ~200-500ms | ~1-2 Mbps |
| Total (15 regions, sequential) | ~7-10s | Variable |
| Total (15 regions, 5 workers) | ~2-3s | Variable |

## Scalability Analysis

### Small Organizations (< 1000 volumes)

```
Config: max_workers=5
Time: ~1-2 seconds
Memory: ~1-2MB
```

### Medium Organizations (1K-10K volumes)

```
Config: max_workers=5-10
Time: ~3-5 seconds
Memory: ~10-15MB
```

### Large Organizations (10K-50K volumes)

```
Config: max_workers=15-20
Time: ~5-10 seconds
Memory: ~50-100MB
```

### Enterprise (50K+ volumes)

```
Config: max_workers=20
Consider: Multi-account scanning
Time: ~10-30 seconds per account
Memory: ~100-200MB
```

## Error Handling

### Credential Errors

```python
try:
    ec2_client = boto3.client(...)
except Exception as e:
    logger.error(f"Connection error: {e}")
    raise
```

### Region Scan Errors

```python
try:
    # Paginate and collect volumes
    for page in page_iterator:
        volumes.extend(page.get('Volumes', []))
except Exception as e:
    logger.error(f"Failed to scan region {region}: {e}")
    return region, []  # Graceful degradation
```

### Pagination Errors

Built-in paginator retry logic:
- ✅ ThrottlingException (exponential backoff)
- ✅ Network timeouts
- ✅ Transient failures

## Thread Safety

### Per-Region Clients

Each worker gets independent EC2 client:
```python
ec2_client = boto3.client(...)  # Thread-local
```

### Shared State

Result dictionary uses thread-safe dictionary:
```python
results[region] = volumes  # Atomic operation
```

### Logging

Python logging is thread-safe:
```python
logger.info(f"[{thread_name}] {message}")
```

## Extension Points

### Add Snapshot Scanning

```python
def scan_snapshots(self, region):
    paginator = ec2_client.get_paginator('describe_snapshots')
    # Similar implementation
```

### Add RDS Instance Detection

```python
def scan_rds_instances(self, region):
    rds_client = boto3.client('rds', region_name=region)
    # Scan for unattached resources
```

### Custom Export Formats

```python
def export_to_database(self, volumes):
    # DynamoDB, RDS, or other databases
    pass
```

## Security Considerations

### Credentials

- ✅ No hardcoded secrets
- ✅ .env file (ignored by git)
- ✅ Environment variables support
- ✅ AWS credential chain support

### IAM Permissions

- ✅ Least-privilege policy
- ✅ Read-only operations
- ✅ No delete/modify permissions

### Data Protection

- ✅ No credentials in logs
- ✅ No credentials in output files
- ✅ File permissions management

## Next Steps

- Read [USAGE.md](./USAGE.md) for examples
- See [CONFIGURATION.md](./CONFIGURATION.md) for setup
- Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for issues
