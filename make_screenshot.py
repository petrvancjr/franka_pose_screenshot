from PIL import Image
import roboticstoolbox as rtb
from spatialmath import SE3
import time
import swift
import numpy as np

panda = rtb.models.Panda()
sim = swift.Swift()
sim.launch()

# Set camera view angle and position
sim.set_camera_pose([0.6, 0.4, 0.4], [0.4, 0, 0.25])
sim.add(panda)

# Define the first end-effector pose
pos = [0.3, 0.0, 0.25] 
rpy = [0, np.pi-0.2, 0] # Pointing down (rotation about y-axis)
T_target = SE3(pos) * SE3.RPY(rpy)
q_target = panda.ikine_LM(T_target).q
panda.q = q_target
sim.step()
time.sleep(1)

# Save first screenshot
start_image_path = f"panda_start_{np.random.randint(1000000)}.png"
sim.screenshot(start_image_path)

# Define the second end-effector pose
pos = [0.5, 0.0, 0.25]
rpy = [0, np.pi+0.2, 0] # Pointing down (rotation about y-axis)
T_target = SE3(pos) * SE3.RPY(rpy)
q_target = panda.ikine_LM(T_target).q
panda.q = q_target
sim.step()
time.sleep(1)

# Save second screenshot
end_image_path = f"panda_end_{np.random.randint(1000000)}.png"
sim.screenshot(end_image_path)

# Blend images
start_img = Image.open(start_image_path).convert("RGBA")
end_img = Image.open(end_image_path).convert("RGBA")

# Blend images (alpha=0.5 for equal contribution)
blended_img = Image.blend(start_img, end_img, alpha=0.5)
blended_image_path = "panda_blended.png"
blended_img.save(blended_image_path)

print(f"Blended image saved as {blended_image_path}")

# Close the simulator
sim.hold()

