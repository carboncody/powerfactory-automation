import sys; 
# Path to PowerFactory
sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2023\Python\3.9")
# Import as a system import
import powerfactory as pf

def init_pf():
    try:
        app = pf.GetApplicationExt()
        print(app)
        projName ='S-Banen(52)'
  
        # activate project
        app.ActivateProject(projName)
        project = app.GetActiveProject()
        # print(projName + ' activated')
        
        return [app, project]
    except pf.ExitError as error:
        print(error)
        print('error.code = %d' % error.code)
