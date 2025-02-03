import bpy

def InstantiateParticleSystem(atom1, atom2):
    # Try to get the two objects from the scene
    obj1 = bpy.data.objects.get(atom1)
    obj2 = bpy.data.objects.get(atom2)
    
    # Raise an error if one of the objects is not found
    if obj1 is None:
        raise ValueError(f"Object '{atom1}' not found in the scene.")
    if obj2 is None:
        raise ValueError(f"Object '{atom2}' not found in the scene.")
    
    # Store the location vectors for the two objects
    loc1 = obj1.location
    loc2 = obj2.location
    
    # Compute direction vector from obj1 to obj2
    direction = (loc2 - loc1).normalized()
    
    # Create a new particle system
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj1
    obj1.select_set(True)
    bpy.ops.object.particle_system_add()
    
    # Configure the particle system
    psys = obj1.particle_systems[-1]
    psys.name = "ParticleSystem"
    psys.settings.count = 10
    psys.settings.frame_start = 1
    psys.settings.frame_end = 10
    psys.settings.lifetime = 50
    psys.settings.emit_from = 'VOLUME'
    
    # Set the velocity of the particles in the direction of obj2
    speed_factor = 2  # Adjust this to control the speed of particles
    psys.settings.normal_factor = 0  # Disable normal-based emission
    psys.settings.object_align_factor = (direction.x, direction.y, direction.z)
    psys.settings.velocity_factor_random = 0  # Make sure there's no randomness
    
    # Disable gravity so particles move in a straight line
    psys.settings.effector_weights.gravity = 0

# Example usage
InstantiateParticleSystem("C01", "C05")
