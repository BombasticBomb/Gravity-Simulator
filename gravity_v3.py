from ursina import *
import math
import os
import sys

app = Ursina(size=(640, 480))
window.color = color.black

# —————————————————————————————
# Simulation parameters
GM = 3000.5  # G·M term
start_radius = Vec3(-60, 40, 5)  # initial distance from sun
initial_speed = 5.5  # launch speed
time_scale = 2  # simulation speed

# —————————————————————————————
# Individual UI Texts (all parented to camera.ui)
state_txt = Text('', parent=camera.ui, position=(-0.52, 0.5), origin=(0, 1), scale=1.1, color=color.cyan)

gm_txt = Text(f'GM = {GM}', parent=camera.ui, position=(-0.57, 0.45), origin=(0, 1), scale=1.1, color=color.cyan)

rad_txt = Text(f'rad = {start_radius}', parent=camera.ui, position=(-0.52, 0.40), origin=(0, 1), scale=1.1, color=color.cyan)

spd_txt = Text(f'init_speed = {initial_speed}', parent=camera.ui, position=(-0.55, 0.35), origin=(0, 1), scale=1.1, color=color.cyan)

sim_txt = Text(f'sim_speed = {time_scale}', parent=camera.ui, position=(-0.55, 0.30), origin=(0, 1), scale=1.1, color=color.cyan)

# —————————————————————————————
# Sun and planet setup
sun = Entity(model='sphere', scale=20, position=Vec3(0, 0, 0), texture='sun.png')
planet = Entity(model='sphere', scale=5, position=start_radius, texture='earth.jpg')
planet.velocity = Vec3(0, 0, initial_speed)

def update():
    global GM, start_radius, initial_speed, time_scale
    # rotate for visual effect
    sun.rotation_y += time.dt * 5
    planet.rotation_y += time.dt * 15

    # compute gravity force
    r_vec = planet.position - sun.position
    r = max(r_vec.length(), 1e-3)
    accel = r_vec.normalized() * (-GM / r**2)

    # integrate
    dt = time.dt * time_scale
    planet.velocity += accel * dt
    planet.position += planet.velocity * dt

    # energy & state
    KE = 0.5 * planet.velocity.length_squared()
    PE = -GM / r
    state = 'Orbiting' if (KE + PE < 0) else 'Escaping'

    # update each text
    state_txt.text = state + f' (E={(KE+PE):.2f})'
    gm_txt.text = f'GM = {GM}'
    rad_txt.text = f'rad = {start_radius}'
    spd_txt.text = f'init_speed = {initial_speed}'
    sim_txt.text = f'sim_speed = {time_scale}'
    
    # GM Control
    if held_keys['g'] and held_keys['up arrow']:
        GM += 10
    elif held_keys['g'] and held_keys['down arrow']:
        GM -= 10
        
    #Sim_Speed Control
    if held_keys['s'] and held_keys['up arrow']:
        time_scale += 0.1
    elif held_keys['s'] and held_keys['down arrow']:
        time_scale -= 0.1

    # Initial Speed Control
    if held_keys['i'] and held_keys['up arrow']:
        planet.velocity = planet.velocity.normalized() * (planet.velocity.length() + 0.1)
    if held_keys['i'] and held_keys['down arrow']:
        planet.velocity = planet.velocity.normalized() * max(0, planet.velocity.length() - 0.1)

    # Restart
    if held_keys['escape']:
        os.execv(sys.executable, ['python'] + sys.argv)

# free camera
EditorCamera()
app.run()
