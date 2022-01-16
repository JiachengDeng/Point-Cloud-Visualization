import numpy as np
import open3d as o3d
from pyntcloud import PyntCloud
import os

k=1 # The number of scene in the training set and The value range is 0~706.
Path = '' # The path of the training set 
scene_num = ('000'+str(k)+'_00')[-7:]  #input
use_lineset = True # Whether to visualize the bounding boxes in a scene.

BBox_path = os.path.join(Path, 'scene'+scene_num+'_bbox.npy')
pc_path = os.path.join(Path, 'scene'+scene_num+'_vert.npy')
sem_path = os.path.join(Path, 'scene'+scene_num+'_sem_label.npy') 
ins_path = os.path.join(Path, 'scene'+scene_num+'_ins_label.npy') 

pc_data = np.load(pc_path) 
pc = pc_data

pc[...,[0, 1, 2]] = pc[...,[0, 2, 1]]
pc[...,[3, 4, 5]] = pc[...,[3, 4, 5]]
pc[..., 1] *= -1

bbox_data = np.load(BBox_path)
bbox = bbox_data

sem_data = np.load(sem_path)
sem = sem_data

ins_data = np.load(ins_path)
ins = ins_data

MEAN_COLOR_RGB = np.array([109.8, 97.2, 83.8])

point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(pc[:,0:3])
point_cloud.colors = o3d.utility.Vector3dVector(pc[:,3:]/256.0)

# Use the same color for all lines by defaults and users can customize colors here.
colors = [[0, 1, 0] for _ in range(12)]
lines = [[0, 1], [1, 2], [2, 3], [0, 3],
        [4, 5], [5, 6], [6, 7], [4, 7],
        [0, 4], [1, 5], [2, 6], [3, 7]]

output_sets = [point_cloud]

if use_lineset == True:
    # Our lines span from points 0 to 1, 1 to 2, 2 to 3, etc...
    for i in range(bbox.shape[0]):
        line = o3d.geometry.LineSet()
        line.points = o3d.utility.Vector3dVector(box_center_to_corner(bbox[i,:6]))
        line.lines = o3d.utility.Vector2iVector(lines)
        line.colors = o3d.utility.Vector3dVector(colors)
        
        output_sets.append(line)
print(f"This is the {K}th scene.")
print(f'The size of Bounding Boxes = {bbox_data.shape}')
print(f'The size of the labels of the semantic segmentation = {sem_data.shape}')
print(set(sem))
print(f'The size of the labels of the instance segmentation = {ins_data.shape}')
print(set(ins))
o3d.visualization.draw_geometries(output_sets)

def flip_axis_to_camera_tensor(pc):
    """Flip X-right,Y-forward,Z-up to X-right,Y-down,Z-forward
    Input and output are both (N,3) array
    """
    pc2 = pc.copy()

    return pc2

def box_center_to_corner(box):
    """box_size is array(l,w,h), heading_angle is radius clockwise from pos x axis, center is xyz of box center
    output (8,3) array for 3D box cornders
    Similar to utils/compute_orientation_3d
    """
    center = box[0:3]
    center[...,[0, 1, 2]] = center[..., [0, 2, 1]]  # cam X,Y,Z = depth X,-Z,Y
    center[..., 1] *= -1

    l, w, h = box[3], box[4], box[5]

    rotation = 0 #The yaw angle is 0 for all scenes in the ScanNet V2 dataset.

    R = np.array([
    [np.cos(rotation), 0.0, np.sin(rotation)],
    [0.0, 1.0, 0.0],
    [-np.sin(rotation), 0.0, np.cos(rotation)]])

    x_corners = [l / 2, l/ 2, -l / 2, -l / 2, l / 2, l / 2, -l / 2, -l / 2]
    y_corners = [h / 2, h / 2, h / 2, h / 2, -h / 2, -h / 2, -h / 2, -h / 2]
    z_corners = [w / 2, -w / 2, -w / 2, w / 2, w / 2, -w / 2, -w / 2, w / 2]
    corners_3d = np.dot(R, np.vstack([x_corners, y_corners, z_corners]))
    corners_3d[0, :] = corners_3d[0, :] + center[0]
    corners_3d[1, :] = corners_3d[1, :] + center[1]
    corners_3d[2, :] = corners_3d[2, :] + center[2]
    corners_3d = np.transpose(corners_3d)
    return corners_3d