import sys
import os
import globals as globals

def init_pf():
    try:
        # Check if pf_path is set and valid
        if not globals.pf_path or not os.path.exists(globals.pf_path):
            raise ValueError("PowerFactory path is not set or invalid. Please set the correct path in the UI.")

        # Add PowerFactory to system path
        sys.path.append(globals.pf_path)

        # Try to import PowerFactory
        import powerfactory as pf  # type: ignore

        app = pf.GetApplicationExt()
        print(app)
        projName = globals.init_project_name

        # Activate project
        app.ActivateProject(projName)
        project = app.GetActiveProject()
        print(f"{projName} activated")

        return app, project

    except ValueError as ve:
        # Handle missing or invalid PowerFactory path
        print(ve)
        return None, None

    except ModuleNotFoundError as error:
        # Handle missing PowerFactory module
        print("PowerFactory module not found. Check if PowerFactory is installed and path is correct.")
        return None, None

    except pf.ExitError as error:
        # Handle PowerFactory-specific errors
        print(f"Error in PowerFactory: {error}")
        return None, None
