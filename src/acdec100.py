import torch
import torch.nn as nn
import torch.nn.functional as F
import pybullet as p
import pybullet_data
import time

# === Load Multimodal Embeddings ===
image_embeddings = torch.load("image_embeddings.pt")
text_embeddings = torch.load("text_embeddings.pt")

# Normalize
image_embeddings = F.normalize(image_embeddings, dim=-1)
text_embeddings = F.normalize(text_embeddings, dim=-1)

# Concatenate
combined = torch.cat([image_embeddings, text_embeddings], dim=-1)  # [1, 1024]

# === Multimodal Fusion MLP ===
fusion_mlp = nn.Sequential(
    nn.Linear(1024, 512),
    nn.ReLU(),
    nn.Linear(512, 128)
)
fused_vector = fusion_mlp(combined)  # [1, 128]

# === Action Decoder MLP ===
action_decoder = nn.Sequential(
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 3)  # 3D position: x, y, z
)
predicted_position = action_decoder(fused_vector)  # [1, 3]
target_xyz = predicted_position.squeeze().tolist()

# === PyBullet Setup ===
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

plane_id = p.loadURDF("plane.urdf")
robot_id = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

# Let PyBullet load
for _ in range(100):
    p.stepSimulation()
    time.sleep(0.01)

# Define robot end effector index (KUKA)
end_effector_link_index = 6

# Use IK to calculate joint angles
joint_angles = p.calculateInverseKinematics(robot_id, end_effector_link_index, target_xyz)

# Apply joint angles
for joint_idx in range(p.getNumJoints(robot_id)):
    p.setJointMotorControl2(
        bodyIndex=robot_id,
        jointIndex=joint_idx,
        controlMode=p.POSITION_CONTROL,
        targetPosition=joint_angles[joint_idx]
    )

# Simulate for a few seconds
for _ in range(500):
    p.stepSimulation()
    time.sleep(0.01)

p.disconnect()
