import boto3
import os
import logging
import csv
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple
from datetime import datetime
import json
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s'
)
logger = logging.getLogger(__name__)


class AWSZombieHunter:
    def __init__(self, regions: List[str] = None, max_workers: int = 10):
        """
        Initialize AWS Zombie Hunter with multi-region support.
        
        Args:
            regions: List of AWS regions to scan. If None, scans all available regions.
            max_workers: Number of parallel threads for scanning (default: 5)
        """
        load_dotenv()
        
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.specified_region = os.getenv("AWS_REGION")
        self.max_workers = max_workers
        self.regions = regions or []
        
        # Initialize EC2 client for region discovery
        try:
            self.ec2_base = boto3.client(
                'ec2',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.specified_region or 'us-east-1'
            )
            logger.info("AWS connection established successfully.")
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise

    def get_available_regions(self) -> List[str]:
        """
        Fetch all available AWS regions.
        """
        try:
            logger.info("Fetching available AWS regions...")
            response = self.ec2_base.describe_regions()
            regions = [region['RegionName'] for region in response['Regions']]
            logger.info(f"Found {len(regions)} available regions: {', '.join(regions)}")
            return regions
        except Exception as e:
            logger.error(f"Failed to fetch regions: {e}")
            return [self.specified_region] if self.specified_region else ['us-east-1']

    def scan_region(self, region: str) -> Tuple[str, List[Dict]]:
        """
        Scan a single region for zombie (unattached) EBS volumes using Paginator.
        
        Args:
            region: AWS region name
            
        Returns:
            Tuple of (region_name, list_of_volumes)
        """
        try:
            logger.info(f"Scanning region: {region}")
            
            ec2_client = boto3.client(
                'ec2',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=region
            )
            
            # Use paginator for efficient handling of large volume lists
            paginator = ec2_client.get_paginator('describe_volumes')
            
            # Configure paginator with filter
            page_iterator = paginator.paginate(
                Filters=[
                    {
                        'Name': 'status',
                        'Values': ['available']
                    }
                ],
                PaginationConfig={
                    'MaxItems': 10000,        # Maximum items to return
                    'PageSize': 500            # Items per API call (max 500)
                }
            )
            
            # Collect volumes from all pages
            volumes = []
            page_count = 0
            
            for page in page_iterator:
                page_count += 1
                page_volumes = page.get('Volumes', [])
                volumes.extend(page_volumes)
                logger.debug(f"Region {region}: Page {page_count} - Retrieved {len(page_volumes)} volumes (Total: {len(volumes)})")
            
            logger.info(f"Region {region}: Found {len(volumes)} unattached volumes across {page_count} page(s)")
            
            # Add region info to each volume
            for volume in volumes:
                volume['Region'] = region
            
            return region, volumes
            
        except Exception as e:
            logger.error(f"Failed to scan region {region}: {e}")
            return region, []

    def scan_all_regions_parallel(self) -> Dict[str, List[Dict]]:
        """
        Scan all regions in parallel using ThreadPoolExecutor.
        
        Returns:
            Dictionary with region names as keys and volume lists as values
        """
        # Determine which regions to scan
        if self.regions:
            regions_to_scan = self.regions
            logger.info(f"Scanning specified regions: {', '.join(regions_to_scan)}")
        else:
            regions_to_scan = self.get_available_regions()
        
        results = {}
        
        logger.info(f"Starting parallel scan of {len(regions_to_scan)} regions with {self.max_workers} workers...")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all scan tasks
            future_to_region = {
                executor.submit(self.scan_region, region): region 
                for region in regions_to_scan
            }
            
            # Collect results with progress bar
            with tqdm(total=len(regions_to_scan), desc="Scanning regions", unit="region") as pbar:
                for future in as_completed(future_to_region):
                    region, volumes = future.result()
                    results[region] = volumes
                    pbar.update(1)
        
        return results

    def consolidate_results(self, region_results: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Consolidate results from all regions into a single flat list.
        """
        all_volumes = []
        total_volumes = 0
        
        logger.info("Consolidating results from all regions...")
        
        for region, volumes in region_results.items():
            all_volumes.extend(volumes)
            total_volumes += len(volumes)
        
        logger.info(f"Total zombie volumes found across all regions: {total_volumes}")
        return all_volumes

    def save_to_csv(self, volumes: List[Dict], filename: str = 'zombie_volumes.csv') -> None:
        """
        Save discovered volumes to a CSV file with regional information.
        """
        if not volumes:
            logger.info("No volumes to save.")
            return
        
        headers = ['Region', 'VolumeId', 'Size (GB)', 'CreateTime', 'AvailabilityZone', 'IOPS', 'Throughput']
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for vol in volumes:
                    row = {
                        'Region': vol.get('Region', 'N/A'),
                        'VolumeId': vol['VolumeId'],
                        'Size (GB)': vol['Size'],
                        'CreateTime': vol['CreateTime'].isoformat() if hasattr(vol['CreateTime'], 'isoformat') else str(vol['CreateTime']),
                        'AvailabilityZone': vol['AvailabilityZone'],
                        'IOPS': vol.get('Iops', 'N/A'),
                        'Throughput': vol.get('Throughput', 'N/A')
                    }
                    writer.writerow(row)
            
            logger.info(f"Report successfully saved: {filename}")
            print(f"\n✅ Report generated: {os.path.join(os.getcwd(), filename)}")
            print(f"📊 Total zombie volumes: {len(volumes)}")
            
        except Exception as e:
            logger.error(f"CSV write error: {e}")

    def save_to_json(self, region_results: Dict[str, List[Dict]], filename: str = 'zombie_volumes.json') -> None:
        """
        Save detailed results to JSON format (organized by region).
        """
        try:
            # Convert datetime objects to strings for JSON serialization
            json_data = {}
            for region, volumes in region_results.items():
                json_data[region] = []
                for vol in volumes:
                    json_data[region].append({
                        'VolumeId': vol['VolumeId'],
                        'Size': vol['Size'],
                        'CreateTime': vol['CreateTime'].isoformat() if hasattr(vol['CreateTime'], 'isoformat') else str(vol['CreateTime']),
                        'AvailabilityZone': vol['AvailabilityZone'],
                        'Iops': vol.get('Iops', 'N/A'),
                        'Throughput': vol.get('Throughput', 'N/A'),
                        'State': vol.get('State', 'available'),
                        'Encrypted': vol.get('Encrypted', False)
                    })
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(json_data, jsonfile, indent=2)
            
            logger.info(f"JSON report saved: {filename}")
            print(f"📋 Detailed report: {os.path.join(os.getcwd(), filename)}")
            
        except Exception as e:
            logger.error(f"JSON write error: {e}")

    def print_summary(self, region_results: Dict[str, List[Dict]]) -> None:
        """
        Print a summary of findings by region.
        """
        print("\n" + "="*70)
        print("🔍 AWS ZOMBIE HUNTER - SCAN SUMMARY")
        print("="*70)
        
        total_volumes = 0
        total_size_gb = 0
        
        for region, volumes in sorted(region_results.items()):
            if volumes:
                region_size = sum(vol['Size'] for vol in volumes)
                print(f"\n  📍 Region: {region}")
                print(f"     - Zombie Volumes: {len(volumes)}")
                print(f"     - Total Size: {region_size} GB")
                total_volumes += len(volumes)
                total_size_gb += region_size
        
        print("\n" + "-"*70)
        print(f"  📊 TOTAL ACROSS ALL REGIONS:")
        print(f"     - Zombie Volumes: {total_volumes}")
        print(f"     - Total Wasted Storage: {total_size_gb} GB")
        print(f"     - Estimated Monthly Cost: ${total_size_gb * 0.1:.2f} USD (avg)")
        print("="*70 + "\n")


def main():
    """
    Main entry point for AWS Zombie Hunter.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AWS Zombie Hunter - Detect unused EBS volumes across regions'
    )
    parser.add_argument(
        '--regions',
        nargs='+',
        help='Specific regions to scan (e.g., us-east-1 eu-west-1). If not specified, all regions are scanned.'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=5,
        help='Number of parallel scanning threads (default: 5)'
    )
    parser.add_argument(
        '--json-output',
        action='store_true',
        help='Generate additional JSON output with detailed regional breakdown'
    )
    
    args = parser.parse_args()
    
    logger.info("="*70)
    logger.info("AWS Zombie Hunter - Starting scan")
    logger.info("="*70)
    
    try:
        # Initialize hunter
        hunter = AWSZombieHunter(
            regions=args.regions,
            max_workers=args.workers
        )
        
        # Scan all regions in parallel
        region_results = hunter.scan_all_regions_parallel()
        
        # Print summary
        hunter.print_summary(region_results)
        
        # Consolidate and save results
        all_volumes = hunter.consolidate_results(region_results)
        
        if all_volumes:
            hunter.save_to_csv(all_volumes)
            
            if args.json_output:
                hunter.save_to_json(region_results)
        else:
            print("\n✨ System is clean! No zombie volumes found.")
        
        logger.info("Scan completed successfully")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
