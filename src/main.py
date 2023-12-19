import os
from process_input.process_input import process_input
from pf_sim_run.pf_sim_run import pf_sim_run

def main():
    os.system('cls')
    print("-----------------------------------------------------")

    # process_input()     # THIS SAVES A JSON FILE WHICH HAS ALL THE TIMESERIES DATA IN utils/timeseries.json
    app = pf_sim_run()
    
    del app
    
if __name__ == "__main__":
    main()
