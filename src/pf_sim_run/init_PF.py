import sys; 
# Path to PowerFactory
sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2023\Python\3.9")
# Import as a system import
import powerfactory as pf

def init_PF():
    try:
        app = pf.GetApplicationExt()
    except pf.ExitError as error:
        print(error)
        print('error.code = %d' % error.code)

    projName ='Project'
  
    # activate project
    project = app.ActivateProject(projName)
    print(projName + ' activated')
    
    return project


# 1 -> SYGAAENDE
# 2 -> NORDGAAENDE

# FOR EXAMPLE --------------
# 82-034.650-K-2-O1-O1
# 82 -> BTR
# 034.650 KM
# K - KØRELEDNINGER
# R - RETURN VEJ
# 2 -> SPOR
