import sys
import globals

# Import pf from system path
sys.path.append(globals.pf_path)
import powerfactory as pf

def init_pf():
    try:
        app = pf.GetApplicationExt()
        print(app)
        projName ='S-Banen(55)'
  
        # activate project
        app.ActivateProject(projName)
        project = app.GetActiveProject()
        print(projName + ' activated')
        
        return app, project
    
    except pf.ExitError as error:
        print(error)
        print('error.code = %d' % error.code)
