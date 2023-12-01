from pf_sim_run.init_pf import init_pf
from pf_sim_run.get_project_state import get_project_state
# from pf_sim_run.remove_existing_busbars import remove_existing_busbars
from pf_sim_run.create_busbars import create_busbars

def pf_sim_run(): # busbar_pos_df
    app = init_pf()
    
    # Get the grid
    netdat = app.GetProjectFolder('netdat')
    grid = netdat.GetContents('*.ElmNet')[0]

    [existing_busbar_names, existing_lines, existing_line_names, existing_lines_fullname] = get_project_state(app)
    # busbar_pos_tocreate = remove_existing_busbars(existing_busbar_names, busbar_pos_df)
    
    create_busbars(app, existing_lines, existing_line_names, existing_lines_fullname)
    
    return app