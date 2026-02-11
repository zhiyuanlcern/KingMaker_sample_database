#!/usr/bin/env python3
"""
Script to create missing sample directories and YAML files from datasets.yaml
"""

import yaml
import os
from pathlib import Path

def create_sample_files(datasets_file='datasets.yaml'):
    """Extract rem_hbb and wg samples from datasets.yaml and create directory structure"""
    
    # Load the datasets file
    with open(datasets_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Sample types to process
    sample_types = ['rem_hbb', 'wg']
    
    stats = {st: {'created': 0, 'skipped': 0} for st in sample_types}
    
    for sample_name, sample_data in data.items():
        if not isinstance(sample_data, dict):
            continue
            
        sample_type = sample_data.get('sample_type')
        if sample_type not in sample_types:
            continue
            
        era = sample_data.get('era')
        if not era:
            print(f"Warning: No era found for {sample_name}, skipping")
            continue
        
        # Create directory structure
        dir_path = Path(era) / sample_type
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create YAML file
        yaml_file = dir_path / f"{sample_name}.yaml"
        
        if yaml_file.exists():
            print(f"Skipping {yaml_file} (already exists)")
            stats[sample_type]['skipped'] += 1
            continue
        
        # Write the sample data to individual YAML file
        with open(yaml_file, 'w') as f:
            yaml.dump(sample_data, f, default_flow_style=False, sort_keys=False)
        
        print(f"Created {yaml_file}")
        stats[sample_type]['created'] += 1
    
    # Print summary
    print("\n=== Summary ===")
    for sample_type in sample_types:
        print(f"{sample_type}: {stats[sample_type]['created']} created, {stats[sample_type]['skipped']} skipped")

if __name__ == '__main__':
    create_sample_files()
