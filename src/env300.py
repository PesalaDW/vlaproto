import pybullet as p
import pybullet_data
import time
import random
import math

# Start GUI
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load a plane (flat ground)
plane_id = p.loadURDF("plane.urdf")

# Set gravity
p.setGravity(0, 0, -9.81)

# Load a white table (simple box for now)
table_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.05])
table_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.05], rgbaColor=[1, 1, 1, 1])
table_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=table_shape,
                             baseVisualShapeIndex=table_visual,
                             basePosition=[0, 0, 0.05])

# Load KUKA IIWA + gripper URDF from pybullet_data
robot_start_pos = [0.0, 0.0, 0.05]  # base at table center (table height ~0.1 m; robot base sits slightly above ground)
robot_start_orient = p.getQuaternionFromEuler([0, 0, 0])
kuka_id = p.loadURDF("kuka_iiwa/model.urdf", robot_start_pos, robot_start_orient, useFixedBase=True)

ROBOT_RADIUS = 0.15  # meters
ROBOT_BASE_XY = [0.0, 0.0]  # same as robot_start_pos[:2]
#Circular safe zone to prevent objects spawning inside this.

def create_object(shape, color_rgb, position):
    if shape == "cube":
        collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.03, 0.03, 0.03])
        visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.03, 0.03, 0.03], rgbaColor=color_rgb + [1])
    elif shape == "ball":
        collision = p.createCollisionShape(p.GEOM_SPHERE, radius=0.03)
        visual = p.createVisualShape(p.GEOM_SPHERE, radius=0.03, rgbaColor=color_rgb + [1])
    else:
        return None
    return p.createMultiBody(baseMass=1, baseCollisionShapeIndex=collision,
                             baseVisualShapeIndex=visual,
                             basePosition=position)

colors = {
    "red": [1, 0, 0],
    "green": [0, 1, 0],
    "blue": [0, 0, 1]
}

#positions = [[-0.2, 0.2, 0.1], [0, 0.2, 0.1], [0.2, 0.2, 0.1],   # Cubes
#             [-0.2, -0.2, 0.1], [0, -0.2, 0.1], [0.2, -0.2, 0.1]]  # Balls
def random_position_on_table():
    x = random.uniform(-0.45, 0.45)
    y = random.uniform(-0.45, 0.45)
    z = 0.12  # Slightly above the table
    return [x, y, z]

#positions = [random_position_on_table() for _ in range(6)]
#def is_far_enough(pos, other_positions, min_dist=0.07):
 #   for other in other_positions:
  #      dx = pos[0] - other[0]
   #     dy = pos[1] - other[1]
    #    if math.sqrt(dx * dx + dy * dy) < min_dist:
     #       return False
    #return True

def is_far_enough(pos, other_positions, min_dist=0.07, avoid_center=True):
    for other in other_positions:
        dx = pos[0] - other[0]
        dy = pos[1] - other[1]
        if math.sqrt(dx * dx + dy * dy) < min_dist:
            return False
    # Avoid the robot center
    if avoid_center:
        dx = pos[0] - ROBOT_BASE_XY[0]
        dy = pos[1] - ROBOT_BASE_XY[1]
        if math.sqrt(dx * dx + dy * dy) < ROBOT_RADIUS:
            return False
    return True


def generate_non_overlapping_positions(n=6, max_tries=1000):
    positions = []
    tries = 0
    while len(positions) < n and tries < max_tries:
        candidate = random_position_on_table()
        if is_far_enough(candidate, positions):
            positions.append(candidate)
        tries += 1
    if len(positions) < n:
        raise RuntimeError("Could not place all objects without overlap.")
    return positions

positions = generate_non_overlapping_positions()

shapes = ["cube", "cube", "cube", "ball", "ball", "ball"]

for shape, color, pos in zip(shapes, list(colors.keys()) * 2, positions):
    create_object(shape, colors[color], pos)

# Set camera to top-down view
p.resetDebugVisualizerCamera(cameraDistance=1.0,
                             cameraYaw=0,
                             cameraPitch=-89.99,  # Slightly off -90 to avoid gimbal issues
                             cameraTargetPosition=[0, 0, 0.05])  # Center on table


# Keep simulation running
while True:
    p.stepSimulation()
    time.sleep(1/240)



"""
100: Simple opening of pybullet.
110: Added the table --> The table is working and all. But it opens and closes immediately. Fix it maybe in an upcoming version.
120: Added boxes and balls. --> Now that doesn't visualise. Shall we fix the closing immediately part before going forward? Will update github before all that.
130: Maybe the issue was that the objects weren't spawned.
140: Added the final line. I think it fixes the issue noted in 120. --> Some issues
    1) Closes soon.
    2) Don't see the balls or cubes spawned.
    3) Some errors/warnings like things noted on the command line. 
141: Changed line 46 to list(color...) to try fix error 3, which Chat caught without me telling about that. --> This fixed it!!
    Some more fixes:
        1) On the white table randomize all the objects every time the code is run.
142: Initial position of the objects are randomized. --> Need to stop overlapping.
143: Added a big new functionality to stop overlapping. --> All good now.

200: Adding a robot arm. --> Need to stop the arm colliding with the objects and pushing them away.
201: Fixing issue noted in 200. --> Error in line 96 when passing avoid_center=true to this. 
202: Removed that passing of avoid... --> Fixed the issue.
300: Camera setup done. All g also. But wayyyy too zoomed. Fix that.
"""
