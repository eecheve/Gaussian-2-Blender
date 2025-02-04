import bpy
import os
import urllib.request
import zipfile
import tempfile
import shutil
    
def install_io_scene_obj():
    """In some Blender installations, it appears the module to export as .obj is not
    installed by default. This function installs it."""
    # URL for the io_scene_obj add-on from Blender's GitHub
    addon_url = "https://github.com/blender/blender/archive/master.zip"

    try:
        # Try to fetch the URL to check internet connectivity
        print(f"Checking internet connection by attempting to access {addon_url}...")
        urllib.request.urlopen(addon_url)
    except urllib.error.URLError as e:
        # If an error occurs, print the message and return
        print(f"Error: Unable to connect to the internet. Please check your network connection. {e}")
        return
    
    # Create a temporary directory to store the downloaded file
    temp_dir = tempfile.mkdtemp()

    try:
        # Download the add-on ZIP file
        zip_path = os.path.join(temp_dir, "blender_master.zip")
        print(f"Downloading io_scene_obj add-on from {addon_url}...")
        urllib.request.urlretrieve(addon_url, zip_path)

        # Extract the ZIP file
        print(f"Extracting ZIP file to {temp_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find the io_scene_obj add-on folder within the extracted files
        addon_folder = os.path.join(temp_dir, "blender-master", "release", "scripts", "addons", "io_scene_obj")
        
        if os.path.exists(addon_folder):
            # Install the add-on by copying it to Blender's script directory
            addon_install_path = bpy.utils.user_resource('SCRIPTS', path='addons')
            print(f"Installing io_scene_obj to {addon_install_path}...")

            # Copy the add-on folder to the Blender add-ons folder
            if not os.path.exists(addon_install_path):
                os.makedirs(addon_install_path)

            # Copy the add-on to Blender's directory
            shutil.copytree(addon_folder, os.path.join(addon_install_path, "io_scene_obj"))
            
            # Enable the add-on after installation
            bpy.ops.wm.addon_enable(module="io_scene_obj")
            print("io_scene_obj add-on installed and enabled.")
        else:
            print(f"Error: io_scene_obj folder not found in the extracted files.")
    except Exception as e:
        # Handle any errors that occur during the download or extraction process
        print(f"An error occurred during the installation process: {e}")

def addon_is_installed(addon_name):
    # Get the list of all installed add-ons
    installed_addons = addon_utils.modules()

    # Iterate over the installed add-ons to check their location
    for addon in installed_addons:
        # Try to access the 'module' attribute safely
        #print(f"currently seeing {addon.__name__}")
        try:
            if addon.__name__ == addon_name:
                print(f"Found {addon_name}")
                return True
        except AttributeError:
            # If an add-on doesn't have the 'module' attribute, we ignore it
            continue
    print(f"{addon_name} not found in the current Blender installation.")
    return False

def ExportSceneAs_old(folder_path, file_name, file_type):
    file_path = folder_path + "\\" + file_name + file_type
    
    export_functions = {
        ".fbx": lambda: bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True, bake_anim=True, embed_textures=True),
        ".dae": lambda: bpy.ops.wm.collada_export(filepath=file_path, filter_collada=True, apply_modifiers=True, 
                                                   selected=True, use_blender_profile=True, use_texture_copies=True),
        ".obj": lambda: bpy.ops.export_scene.obj(filepath=file_path, use_selection=True, use_materials=True),
        ".x3d": lambda: bpy.ops.export_scene.x3d(filepath=file_path, use_selection=True),
        ".stl": lambda: bpy.ops.export_mesh.stl(filepath=file_path, use_selection=True)
    }
    
    if file_type in export_functions:
        bpy.ops.object.select_all(action='SELECT')
        export_functions[file_type]()
        bpy.ops.object.select_all(action='DESELECT')
    else:
        print("Invalid file type")
        
def export_obj(folder_path, file_name, file_type):
        """Exports OBJ and ensures its MTL file retains transparency."""
        if not addon_is_installed("io_scene_obj"):
            install_io_scene_obj()
        
        bpy.ops.preferences.addon_enable(module="io_scene_obj") #enable obj export
        file_path = folder_path + "\\" + file_name + file_type
        bpy.ops.export_mesh.obj(filepath=file_path, use_selection=True, 
                            use_materials=True, path_mode='COPY', 
                            keep_vertex_order=True, use_triangles=False, 
                            use_edges=False)
        EnsureObjMtlTransparency(folder_path, file_name)  # Fix transparency in .mtl

def ExportSceneAs(folder_path, file_name, file_type):  
    """
    Exports the scene as the specified file type while ensuring transparency is enabled.

    Parameters:
    folder_path (str): The directory where the file will be saved.
    file_name (str): The name of the exported file (without extension).
    file_type (str): The format of the exported file (e.g., ".fbx", ".dae", ".obj", ".x3d", ".stl").
    """
 
    bpy.context.scene.render.film_transparent = True # Enable film transparency for proper alpha handling

    file_path = folder_path + "\\" + file_name + file_type

    export_functions = {
        ".fbx": lambda: bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True, 
                                                  bake_anim=True, embed_textures=True, 
                                                  path_mode='COPY', use_active_collection=False),
        ".dae": lambda: bpy.ops.wm.collada_export(filepath=file_path, filter_collada=True, 
                                                  apply_modifiers=True, selected=True, 
                                                  use_blender_profile=True, use_texture_copies=True),
        #".obj": lambda: bpy.ops.export_scene.obj(filepath=file_path, use_selection=True, 
        #                                         use_materials=True), #<-- old version
        ".obj": lambda: export_obj(folder_path, file_name, file_type),
        ".x3d": lambda: bpy.ops.export_scene.x3d(filepath=file_path, use_selection=True),
        ".stl": lambda: bpy.ops.export_mesh.stl(filepath=file_path, use_selection=True)
    }
    if file_type in export_functions:
        bpy.ops.object.select_all(action='SELECT')
        export_functions[file_type]()
        bpy.ops.object.select_all(action='DESELECT')
    else:
        print("Invalid file type")
        
def EnsureObjMtlTransparency(folder_path, file_name):
    """
    Modifies the generated .mtl file to ensure that transparency (alpha) values are retained.

    Parameters:
    folder_path (str): The directory where the .mtl file is stored.
    file_name (str): The base name of the .obj file (without extension).
    """

    mtl_path = folder_path + "\\" + file_name + ".mtl"

    try:
        with open(mtl_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.startswith("Kd"):  # Ensure the diffuse color is set
                new_lines.append("d 1.0\n")  # Ensure the transparency is explicitly written
                new_lines.append("Tr 0.0\n")  # Alternative transparency notation

        with open(mtl_path, "w") as file:
            file.writelines(new_lines)

        print(f"Transparency settings added to {mtl_path}")

    except FileNotFoundError:
        print(f"Warning: .mtl file not found at {mtl_path}. The .obj may not retain transparency.")
    
#TO DEBUG
file_path = "C:\\Documents\\Gaussian-2-Blender\\output"
file_name = "methyl_xanthate_highlighted2"
file_type = ".obj"

addon_is_installed("io_scene_obj")
#print("**********")

#ExportSceneAs(folder_path=file_path, file_name=file_name, file_type=file_type)
    