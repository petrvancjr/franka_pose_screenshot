import roboticstoolbox as rtb
import matplotlib.pyplot as plt
import cv2
from copy import deepcopy
import numpy as np

def get_panda_at_config(q):
    assert rtb is not None, "pip install roboticstoolbox-python"
    robot = rtb.models.Panda()
    
    robot.plot(q, backend='pyplot')
    # workaround to retrieve img
    path = "/tmp/tmp.png"
    plt.axis('off')
    plt.grid(b=None)
    plt.savefig(path)
    plt.close()
    return cv2.imread(path)


def plot_camera_images_along_robot_configurations(camera_images, robot_states, name="", images=5, single_image_size = 512):

    assert len(camera_images) == len(robot_states)
    
    idxs = np.array(np.linspace(0, len(camera_images)-1, images), dtype=int)
    camera_images = deepcopy(camera_images.astype(np.uint8).squeeze())

    concatenated_image = np.array([], dtype=np.uint8).reshape(2*single_image_size,0,3)
    for idx in idxs:
        camera_image = camera_images[idx]
        camera_image = cv2.cvtColor(camera_image, cv2.COLOR_GRAY2BGR)
        camera_image = cv2.resize(camera_image, (single_image_size,single_image_size), interpolation=cv2.INTER_AREA)

        panda_config = robot_states[idx]
        pandaimg = get_panda_at_config(q=panda_config)
        # pandaimg = cv2.cvtColor(pandaimg, cv2.COLOR_BGR2GRAY)
        margin = int(single_image_size/4)
        pandaimg = pandaimg[margin:-margin,margin:-margin,:]
        pandaimg = cv2.resize(pandaimg, (single_image_size, single_image_size), interpolation=cv2.INTER_AREA)

        robot_with_image_vertical = np.vstack((pandaimg, camera_image))
        concatenated_image = np.hstack((concatenated_image, robot_with_image_vertical))

    cv2.namedWindow(f'{name} Images', cv2.WINDOW_NORMAL)
    cv2.resizeWindow(f'{name} Images', single_image_size*images, single_image_size*2) 
    cv2.imshow(f'{name} Images', concatenated_image)
    cv2.waitKey(0)  


import argparse
from video_embedding.utils import load

from franka_easy_ik import FrankaEasyIK

def main(args):
    data = load(args.video)
    # TODO: Add joint configurations data to demonstration 
    ik = FrankaEasyIK()
    qs = []

    for pos,ori in zip(data['traj'].T, data['ori'].T):
        qs.append(ik(p=pos, q=[ori[1], ori[2], ori[3], ori[0]]))

    plot_camera_images_along_robot_configurations(data['img'], qs, name=args.video)    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Play video",
        description="",
        epilog="",
    )
    parser.add_argument(
        "--video",
        default="peg_door",
    )
    main(parser.parse_args())



