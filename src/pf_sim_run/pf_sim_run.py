import pandas as pd
from pf_sim_run.init_pf import init_pf
from pf_sim_run.get_project_state import get_project_state
from pf_sim_run.get_existing_busbars import get_existing_busbars

def pf_sim_run(busbar_pos_df):
    app = init_pf()
    [project_busbar_names, existing_line_names] = get_project_state(app)
    matched_busbar_df = get_existing_busbars(project_busbar_names, busbar_pos_df)
    
    return app