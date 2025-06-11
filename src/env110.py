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

#100: Simple opening of pybullet.
#110: Added the table --> The table is working and all. But it opens and closes immediately. Fix it maybe in an upcoming version.
