import sys
import globals

# Import pf from system path
sys.path.append(globals.pf_path)
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
        
        # # Get the grid
        # netdat = app.GetProjectFolder('netdat')
        # grid = netdat.GetContents('*.ElmNet')[0]

        # # Create new busbar
        # new_busbar_1 = grid.CreateObject('ElmTerm','Test Busbar')
        # new_busbar_2 = grid.CreateObject('ElmTerm','Test Busbar 2')
        # cubicle_busbar_1 = new_busbar_1.CreateObject('StaCubic','Test Cubicle Busbar 1')
        # cubicle_busbar_2 = new_busbar_2.CreateObject('StaCubic','Test Cubicle Busbar 2')
        # test_line = grid.CreateObject('ElmLne','Test Line')
        # test_line = test_line.CreateObject('StaCubic','Cubicle connection test',cubicle_busbar_1)
        
        # ElmLne.CreateFeederWithRoutes(float dis, float rem, DataObject O)
        
        return app
    
    except pf.ExitError as error:
        print(error)
        print('error.code = %d' % error.code)
