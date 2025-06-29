import pybullet as p
import pybullet_data
import time

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


#100: Simple opening of pybullet.
#110: Added the table --> The table is working and all. But it opens and closes immediately. Fix it maybe in an upcoming version.
#120: Added boxes and balls. --> Now that doesn't visualise. Shall we fix the closing immediately part before going forward? Will update github before all that.

