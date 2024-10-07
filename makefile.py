import os
import subprocess
import sys

def process_input_string(input_string, show = False, sample_type="data"):
    # Run dasgoclient command to get list of files
    command = f'dasgoclient -query="file dataset={input_string}" | sort'
    files = subprocess.check_output(command, shell=True, universal_newlines=True).strip().split('\n')

    # Extract the relevant information from the input string
    if "22EENanoAOD" in input_string:
        era = "2022postEE"
    elif "22NanoAOD" in input_string:
        era = "2022EE"
    elif "23NanoAOD" in input_string:
        era = "2023"
    elif "23BPixNanoAOD" in input_string:
        era = "2023BPix"
    
    dataset = input_string.split("/")[1]
    sample_type = sample_type
    nick = input_string.split("/")[1] +  input_string.split("/")[2].split("-")[0]
    # xsec = 1.0

    # Define the output file path based on the nick variable
    output_path = f"{nick}.yaml"

    # Create the output file
    if show:
        print("{}: ".format(nick))
        print("  dbs: {}".format(input_string))
        print("  era: {}".format(era))
        print("  nick: {}".format(nick))
        print("  sample_type: {}".format(sample_type))
    else:
        os.makedirs(f"{era}", exist_ok=True)
        os.makedirs(f"{era}/{sample_type}", exist_ok=True)
        with open(f"{era}/{sample_type}/{output_path}", "w") as f:
            f.write("dbs: {}\n".format(input_string))
            f.write("era: {}\n".format(era))
            f.write("filelist:\n")
            for file in files:
                f.write("- root://xrootd-cms.infn.it//{}\n".format(file))
            # f.write("generator_weight: 1.0\n")
            # f.write("nevents: {}\n".format(len(files)))
            f.write("nfiles: {}\n".format(len(files)))
            f.write("nick: {}\n".format(nick))
            f.write("sample_type: {}\n".format(sample_type))
            # f.write("xsec: {}\n".format(xsec))

    # Print the output file contents
    # if not show:
    #     with open(output_path, "r") as f:
    #         print(f.read())

if __name__ == '__main__':
    # Check if the program is run with a text file argument
    if len(sys.argv) > 1:
        txt_file = sys.argv[1]
        show = int(sys.argv[2])
        
        sample_type_lst = ["dyjets", "wjets", "ttbar", "data", "rem_hbb", "diboson", "wg", "singletop", "dyjets", "ggh_htautau", "vbf_htautau"]
        for s in sample_type_lst:
            if s in txt_file:
                sample_type = s
                break
        # Read the text file line by line
        
        with open(txt_file, 'r') as f:
            lines = f.readlines()

        # Process each line
        for line in lines:
            line = line.strip()
            if line:
                # print(line)
                process_input_string(line, show, sample_type)
