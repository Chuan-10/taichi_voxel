from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges = 0, exposure=1)
scene.set_floor(-0.05, (1.0, 1.0, 1.0))
scene.set_background_color((0.5, 0.5, 0.4))
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))


@ti.func
def create_cylinder(pos, radius, height, color):
    for I in ti.grouped(
            ti.ndrange((pos[0] - radius, pos[0] + radius), (pos[1], pos[1] + height),
                       (pos[2] - radius, pos[2] + radius))):
        if I[0] ** 2 + I[2] ** 2 <= radius ** 2: 
            scene.set_voxel(I, 1, color)


@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    create_cylinder(ivec3(0, 0, 0), 30, 5, vec3(0.9, 0.1, 0.1))


initialize_voxels()

scene.finish()
