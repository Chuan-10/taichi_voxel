from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges = 0, exposure=1.5)
scene.set_floor(-1.0, (1.0, 1.0, 1.0))
scene.set_background_color((135/255.0, 216/255.0, 235/255.0))
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))

@ti.func
def create_block(pos, size, color, color_noise, prob):
    for I in ti.grouped(
            ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]),
                       (pos[2], pos[2] + size[2]))):
        if ti.random() < prob:
            scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.func
def create_cone(pos, radius, height, color):
    for I in ti.grouped(
            ti.ndrange((pos[0] - radius, pos[0] + radius), (pos[1], pos[1] + height),
                       (pos[2] - radius, pos[2] + radius))):
        if (I[0]-pos[0]) ** 2 + (I[2]-pos[2]) ** 2 <= ((height + pos[1] - I[1]) * radius / height) ** 2: 
            scene.set_voxel(I, 1, color)

@ti.func
def create_cloud(pos, radius, color, prob):
    for I in ti.grouped(
            ti.ndrange((pos[0] - radius[0], pos[0] + radius[0]), (pos[1] - radius[1], pos[1] + radius[1]),
                       (pos[2] - radius[2], pos[2] + radius[2]))):
        if (I[0]-pos[0])**2/radius[0]**2 + (I[1]-pos[1])**2/radius[1]**2 + (I[2]-pos[2])**2/radius[2]**2 <= 1 and ti.random() <= prob:
            scene.set_voxel(I, 1, color)

@ti.func
def create_tree(pos, height, radius, color):
    create_block(pos, ivec3(2, height * 0.5, 2), vec3(0.7), vec3(0.3), 1.0)
    create_cone(pos + ivec3(1, height * 0.5, 1), radius, height * 0.5, color)

@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    for i in range(4):
        create_block(ivec3(-60, -(i + 1)**2 - 40, -60),
                     ivec3(120, 2 * i + 1, 120),
                     vec3(0.5 - i * 0.1) * vec3(1.0, 0.8, 0.6),
                     vec3(0.05 * (3 - i)), 1.0)
    create_block(ivec3(-60, -40, -60), ivec3(120, 1, 120), vec3(1.2) * vec3(34/255.0, 139/255.0, 34/255.0), vec3(0.05), 1.0)
    create_cloud(ivec3(20, 30, 40), ivec3(16, 5, 12), vec3(1.0), 0.1)
    create_cloud(ivec3(-52, 25, 30), ivec3(10, 8, 12), vec3(1.0), 0.1)
    create_cloud(ivec3(-40, 36, -10), ivec3(12, 6, 18), vec3(1.0), 0.15)
    create_cloud(ivec3(40, 40, -30), ivec3(12, 6, 8), vec3(1.0), 0.15)
    create_tree(ivec3(-30, -41, -20), 30, 15, vec3(34/255.0, 139/255.0, 34/255.0))
    create_tree(ivec3(30, -41, -45), 15, 7, vec3(34/255.0, 139/255.0, 34/255.0))
    create_tree(ivec3(46, -41, 32), 46, 16, vec3(34/255.0, 139/255.0, 34/255.0))
    create_tree(ivec3(24, -41, -12), 22, 18, vec3(34/255.0, 139/255.0, 34/255.0))

initialize_voxels()

scene.finish()
