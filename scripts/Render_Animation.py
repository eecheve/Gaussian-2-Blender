import bpy

def Render_Animation():
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(1.60443, 0.014596, 2.55805))
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 5)) #setting camera and lights for rendering
    cam = bpy.data.objects["Camera"]
    scene = bpy.context.scene
    mesh_objs = [o for o in scene.objects if o.type =='MESH']
    for ob in mesh_objs:
        ob.select_set(True)
    bpy.ops.view3d.camera_to_view_selected()
    
bpy.context.scene.render.film_transparent = True
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
