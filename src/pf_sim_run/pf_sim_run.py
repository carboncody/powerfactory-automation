from pf_sim_run.init_pf import init_pf
from pf_sim_run.get_project_state import get_project_state

def pf_sim_run():
    app = init_pf()
    get_project_state(app)
    return [app]