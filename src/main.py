import os
from process_input.process_input import process_input
from pf_sim_run.pf_sim_run import pf_sim_run

def main():
    os.system('cls')
    print("-----------------------------------------------------")

    [timely_grouped_json, busbar_pos_df] = process_input()  
    [app, project] = pf_sim_run()
    
    del app
    
if __name__ == "__main__":
    main()
    