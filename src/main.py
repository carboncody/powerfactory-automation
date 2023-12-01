import os
from process_input.process_input import process_input
from pf_sim_run.pf_sim_run import pf_sim_run

def main():
    os.system('cls')
    print("-----------------------------------------------------")

    # [timely_grouped_json, busbar_pos_df] = process_input()     # MOMENTARILY COMMENTED OUT FOR TESTING PURPOSES
    busbar_pos_df = process_input()     # MOMENTARILY COMMENTED OUT FOR TESTING PURPOSES
    # app = pf_sim_run()  # busbar_pos_df
    app = pf_sim_run(busbar_pos_df)  # busbar_pos_df
    
    del app
    
if __name__ == "__main__":
    main()
