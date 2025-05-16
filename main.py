from ursina import *
from ursina.shaders import lit_with_shadows_shader 

from panda3d.core import DepthTestAttrib, RenderModeAttrib
from panda3d.core import Point3

import time
import threading
from multiprocessing import Process

from gui import init_gui

app = Ursina(borderless=False)  

# --- Manual FPS limit ---
target_fps = 60
target_frame_duration = 1 / target_fps
last_time = time.time()

mesh_render_mode = 'default'

EPSILON = 1e-4  # Small offset to prevent self-collision

camera_mode = 0  # 0 = perspective, 1 = orthographic, 2 = isometric
original_position = Vec3(0, 0, -20)
original_rotation = Vec3(0, 0, 0)

window.color = color.hex('cccccc')
mainmodel = 'untitled'
modelscale = 1

controlwindow = False


# genplane = {
#     "position" : [0,0,0],
#     "rotation" : [0,0,0],
#     "scale"    : [1,1,1]
# }


genplane = Entity(model='plane', double_sided=True)
genplane.rotation= (0, 1, 0)



#shit like ['gp', the fucking thing]
def process_gui_cmd(cmd: list):
    print("cmd ", cmd)
    if cmd[0] == "gp":
        print(cmd)
        genplane.position = cmd[1][0]
        genplane.rotation = cmd[1][1]
        genplane.scale    = cmd[1][2]

        print(genplane.rotation)
        pass
    elif cmd[0] == "winclosed":
        global controlwindow
        controlwindow = False
        print("control window reset")
        pass
    pass

threading.Thread(target=init_gui, args=(process_gui_cmd,), daemon=True).start()


def create_line(start, end, base_color, opacity):
    color_with_opacity = color.rgba(base_color.r, base_color.g, base_color.b, opacity)
    return Entity(
        model=Mesh(vertices=[start, end], mode='line', thickness=2),
        color=color_with_opacity,
        double_sided=True,
        enabled=True,
        collision=False  
    )

def create_aim_lines():
    return Entity(
        parent=genplane,
        model=Mesh(vertices=[Vec3(0, 0, 0), Vec3(0, 10, 0)], mode='line'),
        color=color.red,
        scale=1
    )

def create_grid_dots(x_range=(-10, 10), z_range=(-10, 10), spacing=1):
    for x in range(x_range[0], x_range[1] + 1, spacing):
        for z in range(z_range[0], z_range[1] + 1, spacing):
            Entity(
                model='sphere',
                scale=0.05,
                color=color.white33,
                position=Vec3(x, 0, z),
                collision=None  # Ensure no interference
            )

create_grid_dots()

aimlines = [create_aim_lines() for _ in range(4)]

def update():
    global last_time
    now = time.time()
    elapsed = now - last_time

    if elapsed < target_frame_duration:
        time.sleep(target_frame_duration - elapsed)

    last_time = time.time()

    half_w = genplane.scale_x / 2
    half_h = genplane.scale_y / 2

    half_w = half_w / genplane.scale_x

    # Set local positions based on current scale
    corners = [
        Vec3(-half_w, 0, -half_h), #bottomleft
        Vec3( half_w, 0, -half_h), #bottomright
        Vec3(-half_w, 0,  half_h), #topleft
        Vec3( half_w, 0,  half_h), #topright
    ]

    for arrow, corner in zip(aimlines, corners):
        # transform = genplane.get_net_transform().get_inverse().getMat()
        # local_corner = transform.xform_point(Point3(corner))
        arrow.position = corner


    #updates
    # firstentity.rotation_y += 30 * time.dt 
    # print(mouse.hovered_entity)
    pass


def reflect_ray(origin, direction, remaining_bounces, max_bounces, base_color=color.red):
    if remaining_bounces <= 0:
        return

    hit_info = raycast(origin, direction, distance=100, ignore=(camera,), debug=False)

    opacity = remaining_bounces / max_bounces

    if hit_info.hit:
        hit_point = hit_info.point
        create_line(origin, hit_point, base_color, opacity)

        # Compute reflection vector
        normal = hit_info.normal
        reflected_dir = direction - 2 * direction.dot(normal) * normal

        # Add tiny offset in the reflection direction to avoid self-collision
        reflected_origin = hit_point + reflected_dir.normalized() * EPSILON

        reflect_ray(reflected_origin, reflected_dir.normalized(), remaining_bounces - 1, max_bounces, base_color)
    else:
        end = origin + direction * 10
        create_line(origin, end, base_color, opacity)

def toggle_camera_mode():
    global camera_mode, original_position, original_rotation

    camera_mode = (camera_mode + 1) % 3

    if camera_mode == 0:
        # Return to normal perspective
        camera.orthographic = False
        camera.fov = 90
        camera.position = original_position
        camera.rotation = original_rotation
        print("Camera: Perspective")
    elif camera_mode == 1:
        # Flat orthographic view
        camera.orthographic = True
        camera.fov = 10
        camera.position = (0, 0, -20)
        camera.rotation = (0, 0, 0)
        print("Camera: Orthographic")
    elif camera_mode == 2:
        original_position = camera.position
        original_rotation = camera.rotation

        camera.orthographic = True
        camera.fov = 10
        # Place the camera diagonally above and facing the origin
        camera.position = Vec3(20, 20, -20)
        camera.look_at(Vec3(0, 0, 0))

def input(key):
    if key == 'space':
        global mesh_render_mode
        # window.render_mode = 'wireframe'
        if mesh_render_mode == 'default':
            mesh_render_mode = 'wireframe'
            mainentity.visible = False
        else: 
            mesh_render_mode = 'default'
            mainentity.visible = True
        print('reapplied texture')
    elif key == 'r':
        origin = camera.world_position
        direction = camera.forward.normalized()
        reflect_ray(origin, direction, remaining_bounces=5, max_bounces=5, base_color=color.azure)

    elif key == 'c':
        crosshair.enabled = not crosshair.enabled
        print(f"Crosshair {'enabled' if crosshair.enabled else 'disabled'}")

    elif key == 'p':
        toggle_camera_mode()
        


# Entity(
#     model='cube',
#     collider='mesh'
# )

wireframeentity = Entity(
    model=mainmodel,   # Replace with your .obj file
    scale=modelscale,
    # texture='brick',
)

# Enable wireframe mode using Panda3D
wireframeentity.model.setRenderModeWireframe()

# Optional: hide texture if you want a plain wireframe (untextured)
wireframeentity.texture = None

# Optional: make it a solid color
wireframeentity.color = color.black


crosshair = Entity(
    parent=camera.ui,
    model='circle',
    scale=0.002,
    color=color.white,
    position=(0, 0),
    enabled=True
)

# window.render_mode = 'point'

mainentity = Entity(model=mainmodel,
# firstentity = Entity(model='icosphere',
# color = color.rgb(200, 60, 50),
texture = 'brick',
position = (0,0,0),
rotation = (0,0,0),
collider = 'mesh',
scale=modelscale,
# scale = 2,
)

# shadow_pivot = Entity(model='cube', color=color.red)
# DirectionalLight(parent=shadow_pivot, shadows=True, rotation=(45, -45, 45))


editorcam = EditorCamera()
app.run()