import json
import subprocess
import ROOT
import time


def read_filelist_from_das(dbs):
    filedict = {}
    das_query = "file dataset={}".format(dbs)
    das_query += " instance=prod/global"
    cmd = [
        "/cvmfs/cms.cern.ch/common/dasgoclient --query '{}' --json".format(das_query)
    ]
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    jsonS = output.communicate()[0]
    filelist = json.loads(jsonS)
    for file in filelist:
        filedict[file["file"][0]["name"]] = file["file"][0]["nevents"]
    return [
        "{prefix}/{path}".format(prefix="root://xrootd-cms.infn.it/", path=file)
        for file in filedict.keys()
    ]


# # main function with RDF
def calculate_genweight(dataset):
    ROOT.EnableImplicitMT(12)
    start = time.time()
    filelist = read_filelist_from_das(dataset["dbs"])
    # add the treename to each element in the filelist
    try:
        d = ROOT.RDataFrame("Events", filelist)
        cuts = {"negative": "(genWeight<0)*1", "positive": "(genWeight>=0)*1"}
        negative_d = d.Filter(cuts["negative"]).Count()
        positive_d = d.Filter(cuts["positive"]).Count()
        negative = negative_d.GetValue()
        positive = positive_d.GetValue()
        negfrac = negative / (negative + positive)
        genweight = 1 - 2 * negfrac
        print(f"Final genweight: {genweight}")
        end = time.time()
        print(f"Time: {end - start}")
        return genweight
    except:
        print("Error when reading input files")
        return 1.0
