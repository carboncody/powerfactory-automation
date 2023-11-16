import pandas as pd
from pf_sim_run.init_pf import init_pf
from pf_sim_run.get_project_state import get_project_state
from pf_sim_run.get_existing_busbars import get_existing_busbars
from pf_sim_run.create_busbar import create_busbar

def pf_sim_run(): # busbar_pos_df
    app = init_pf()
    
    # Get the grid
    netdat = app.GetProjectFolder('netdat')
    grid = netdat.GetContents('*.ElmNet')[0]

    # Create new busbar
    new_busbar_1 = grid.CreateObject('ElmTerm','Test Busbar')
    new_busbar_2 = grid.CreateObject('ElmTerm','Test Busbar 2')
    cubicle_busbar_1 = grid.CreateObject('StaCubic','Test Cubicle Busbar 1')
    
    
    [project_busbar_names, existing_line_names] = get_project_state(app, cubicle_busbar_1, new_busbar_1)
    # matched_busbar_df = get_existing_busbars(project_busbar_names, busbar_pos_df)
    
    example_busbar_pos = "85-018.622-K-2"
    # create_busbar(app, example_busbar_pos)
    
    return app