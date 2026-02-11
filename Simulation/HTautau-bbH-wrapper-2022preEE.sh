#!/bin/bash

# Wrapper script to generate BBH (bottom quark fusion) Higgs to tau tau YAML files
# for 2022preEE era (Run3Summer22NanoAODv12)
# This script extracts BBH samples from datasets.yaml and creates individual YAML files

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
DATASETS_FILE="$REPO_DIR/datasets.yaml"
OUTPUT_DIR="$REPO_DIR/2022EE/bbh_htautau"

# Check if datasets.yaml exists
if [ ! -f "$DATASETS_FILE" ]; then
    echo "Error: datasets.yaml not found at $DATASETS_FILE"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Generating BBH YAML files for 2022preEE (Run3Summer22NanoAODv12)..."
echo "Output directory: $OUTPUT_DIR"

# Extract BBH samples for 2022preEE (Summer22NanoAODv12, era: 2022EE)
# Using Python to parse YAML properly
export DATASETS_FILE
export OUTPUT_DIR

python3 << 'EOF'
import yaml
import os
import sys

datasets_file = os.environ.get('DATASETS_FILE')
output_dir = os.environ.get('OUTPUT_DIR')

# Load datasets.yaml
with open(datasets_file, 'r') as f:
    datasets = yaml.safe_load(f)

# Filter BBH samples for Summer22NanoAODv12 (era: 2022EE)
count = 0
for sample_name, sample_data in datasets.items():
    if 'BBHto2Tau' in sample_name and 'Run3Summer22NanoAODv12_private' in sample_name:
        era = sample_data.get('era')
        # era can be either a string or the directory name, check both
        if era in ['2022EE', '2022preEE'] or str(era) == '2022EE':
            # Create YAML file for this sample
            output_file = os.path.join(output_dir, f"{sample_name}.yaml")
            
            # Write the YAML file
            with open(output_file, 'w') as out:
                yaml.dump({sample_name: sample_data}, out, default_flow_style=False, sort_keys=False)
            
            count += 1
            print(f"Created: {os.path.basename(output_file)}")

print(f"\nTotal BBH samples generated for 2022preEE: {count}")
EOF

echo "Done!"
