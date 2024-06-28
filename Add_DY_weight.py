import ROOT as R
import argparse
import sys
import os

def Add_new_column(df,new_column, overwrite=False):
    '''
    add a new column, new_column should be a dictionary with key name of new column with value of column value (best to use float)
    new_column = {column_name: value}
    ''' 
    modified = False
    col_names = df.GetColumnNames()
    print("calling adding new column")
    for c in new_column:    
        if c not in col_names:    
            df = df.Define(c,str(new_column[c])) 
            print(f"Adding new Column {c}")
            modified = True
        elif overwrite and c in col_names:
            df = df.Redefine(c,str(new_column[c])) 
            print(f"Redefining Column {c}")
            modified = True
        else:
            continue
        #     print(f"Column already exists {c}")
    return df, modified

def add_DYScaleFactor(input_scalefactor_file, input_file):
    
    TH2F_name = "FF_mass_tt_pt_tt"
    f = input_file
    
    print("Start calculate dyjets scale factor!")
    
    cpp_code =f""" TFile* f = new TFile("{input_scalefactor_file}");"""
    R.gInterpreter.Declare(cpp_code)
    cpp_code = f"""
                    
                    TH2F* histogram = (TH2F*)f->Get("{TH2F_name}");
                    double Getscalefactor(double x, double y) {{
                        if (x > 500){{
                            x = 499.9;
                        }}
                        if (y > 500){{
                            y = 499.9;
                        }}
                        if (x < -9.9) return 1.0 ;
                        if (y < -9.9) return 1.0 ;
                        
                        return histogram->Interpolate(x,y);
                    }}
                    """
    R.gInterpreter.Declare(cpp_code)
    cpp_code = f"""
    float test_value = Getscalefactor(113.0, 18.0);
    """
    R.gInterpreter.Declare(cpp_code)
    R.gROOT.ProcessLine("std::cout << test_value << std::endl;")

    if ".root" in f:
        if "DYto2" in f:
            # continue
            print("Start process: ", f)
            df = R.RDataFrame('ntuple', f)
            df, _ = Add_new_column(df, {
                "DY_weight": "Getscalefactor(mass_tt, pt_tt)" ,
                "DY_weight__up":"Getscalefactor(mass_tt, pt_tt) **2" ,
                "DY_weight__down": "double(1.0)" })
            df.Snapshot('ntuple', f'{f}a.root')
            print(f"finished processing {f}")
            os.system(f"mv {f}a.root {f}")
        else:
            print("Start process: ", f)
            df = R.RDataFrame('ntuple', f)
            df, _ = Add_new_column(df, {"DY_weight": "1.0", "DY_weight": "1.0" , "DY_weight": "1.0"})
            df.Snapshot('ntuple',  f'{f}a.root')                    
            print(f"finished processing {f}")
            os.system(f"mv {f}a.root {f}")
    else:
        print(f"{f} is not a root file")
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='input file for post-process')
    parser.add_argument('--era', type = str, default='2022postEE')

    args = parser.parse_args()

    if args.era == "2022postEE":
        input_scalefactor_file = "/data/bond/zhiyuanl/Plotting/sample_database/DY_scalefactors/2022postEE_scalefactor.root"
    elif args.era == "2022EE":
        input_scalefactor_file = "/data/bond/zhiyuanl/Plotting/sample_database/DY_scalefactors/2022EE_scalefactor.root"
    else:
        print("wrong era provided")
        sys.exit(-1)
    add_DYScaleFactor(input_scalefactor_file, args.input_file)