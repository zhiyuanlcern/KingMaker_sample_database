#!/bin/bash

# Directory containing the txt files
directory="data/jobs/"

# Loop through each txt file in the directory
# for file in "$directory"/tmp*/stdall*.txt; do
find "$directory" -name 'stdall*.txt' -type f -mtime -5 -print0 | while IFS= read -r -d $'\0' file; do

# for file in data/jobs//tmp8qxc3a6p/stdall_88To89.txt; do
    # echo "Checking file: $file"
    # Use awk to process each file and check for matching numbers
    # Use awk to process each file and check for matching numbers and capture output file
    awk '
    BEGIN {
        output_file = ""  # Initialize the output file variable at the start of each file
    }

    # Function to extract number after a specific pattern
    function extract_number(line, pattern,       a, start) {
        start = index(line, pattern);
        if (start > 0) {
            subline = substr(line, start + length(pattern));
            if (match(subline, /[0-9]+/)) {
                return substr(subline, RSTART, RLENGTH);
            }
        }
        return ""
    }

    # Check for lines containing "outputfile"
    /outputfile/ {
        if (match($0, /[^\s]*\.root/)) {
            output_file = substr($0, RSTART, RLENGTH);
        }
    }

    # Check for lines containing "Starting Setup of Dataframe"
    /\[.*\]\s+Starting Setup of Dataframe with/ { 
        num_setup = extract_number($0, "Starting Setup of Dataframe with ")  # Extract number from the line mentioning setup
    }

    # Check for lines containing "Flag_goodVertices: pass="
    /Flag_goodVertices: pass=/ { 
        num_flag = extract_number($0, "Flag_goodVertices: pass=")  # Extract number from the line mentioning flag
        
        # Only report if there is a mismatch
        if (num_setup != "" && num_setup != num_flag) {
            if (output_file == "") {
                print "Mismatch found in " FILENAME ": Setup=" num_setup ", Flag=" num_flag ". Output file not found."
            } else {
                print "Mismatch found in " FILENAME ": Setup=" num_setup ", Flag=" num_flag ", Output file: " output_file
            }
        }
        
        # Reset num_setup after check to avoid false comparisons
        num_setup = ""
    }
    ' "$file"
done