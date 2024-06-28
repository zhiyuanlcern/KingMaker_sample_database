#!/bin/bash

# Directory containing the txt files
directory="./"

# Find and loop through each txt file in the directory modified in the last 5 days
find "$directory" -name 'stdall*.txt' -type f  -print0 | while IFS= read -r -d $'\0' file; do
    awk '
    BEGIN {
        output_file = ""  # Initialize the output file variable at the start of each file
        num_all = ""      # Initialize the num_all variable
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

    # Check for lines containing "GoldenJSONFilter: pass="
    /GoldenJSONFilter: pass=/ {
        num_all = extract_number($0, "all=")  # Extract number after "all="
    }

    # Check for lines containing "Flag_goodVertices: pass=" only if num_all is not already set
    /Flag_goodVertices: pass=/ {
        if (num_all == "") {
            num_all = extract_number($0, "all=")  # Extract number after "all="
        }
    }

    # At the end of the file, compare num_setup and num_all if both are set
    END {
        if (num_setup != "" && num_all != "" && (num_all < num_setup - 1 || num_all > num_setup + 1)) {
            if (output_file == "") {
                print "Mismatch found in " FILENAME ": Setup=" num_setup ", all=" num_all ". Output file not found."
            } else {
                print "Mismatch found in " FILENAME ": Setup=" num_setup ", all=" num_all ", Output file: " output_file
            }
        }
    }
    ' "$file"
done
