import numpy as np
import open3d as o3d
from pyntcloud import PyntCloud
import os

scene=1 # The number of scene in the training set and The value range is 1~10335.
use_lineset = True # Whether to visualize the bounding boxes in a scene.
Train_Path = '' #The path of the training set 
Val_Path = '' #The path of the val set 

scene_index = ('00000'+str(scene))[-6:]

if int(scene_index)<5051:
    BBox_path = os.path.join(Val_Path, scene_index+'_bbox.npy')
    pc_path = os.path.join(Val_Path, scene_index+'_pc.npz')
    votes_path = os.path.join(Val_Path, scene_index+'_votes.npz') 
else:
    BBox_path = os.path.join(Train_Path, scene_index+'_bbox.npy')
    pc_path = os.path.join(Train_Path, scene_index+'_pc.npz')
    votes_path = os.path.join(Train_Path, scene_index+'_votes.npz')

pc_data = np.load(pc_path) 
pc = pc_data['pc']
print(f'The data shape of point cloud is {pc.shape}')

bbox_data = np.load(BBox_path)
bbox = bbox_data[:,:7]
print(f'The data shape of GT bounding boxes is {bbox_data.shape}.')

votes_data = np.load(votes_path)
print(votes_data.files)
print(votes_data['point_votes'].shape)
votes = votes_data['point_votes']

point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(pc[:,:3])
point_cloud.colors = o3d.utility.Vector3dVector(pc[:,3:])

# Our lines span from points 0 to 1, 1 to 2, 2 to 3, etc...
lines = [[0, 1], [1, 2], [2, 3], [0, 3],
         [4, 5], [5, 6], [6, 7], [4, 7],
         [0, 4], [1, 5], [2, 6], [3, 7]]

# Use the same color for all lines
colors = [[1, 0, 0] for _ in range(len(lines))]

output_sets = [point_cloud]
if use_lineset == True:
    for i in range(bbox.shape[0]):
        line = o3d.geometry.LineSet()
        line.points = o3d.utility.Vector3dVector(box_center_to_corner(bbox[i]))
        line.lines = o3d.utility.Vector2iVector(lines)
        line.colors = o3d.utility.Vector3dVector(colors)
        output_sets.append(line)

o3d.visualization.draw_geometries(output_sets)

def box_center_to_corner(box):
    # To return
    corner_boxes = np.zeros((8, 3))

    translation = box[0:3]
    h, w, l = box[3]*2, box[4]*2, box[5]*2
    rotation = -box[6] #/np.pi*180

    # Create a bounding box outline
    bounding_box = np.array([
        [-l/2, -l/2, l/2, l/2, -l/2, -l/2, l/2, l/2],
        [w/2, -w/2, -w/2, w/2, w/2, -w/2, -w/2, w/2],
        [-h/2, -h/2, -h/2, -h/2, h/2, h/2, h/2, h/2]])

    # Standard 3x3 rotation matrix around the Z axis
    rotation_matrix = np.array([
        [np.cos(rotation), -np.sin(rotation), 0.0],
        [np.sin(rotation), np.cos(rotation), 0.0],
        [0.0, 0.0, 1.0]])

    # Repeat the [x, y, z] eight times
    eight_points = np.tile(translation, (8, 1))

    # Translate the rotated bounding box by the
    # original center position to obtain the final box
    corner_box = np.dot(
        rotation_matrix, bounding_box) + eight_points.transpose()
    # corner_box = bounding_box + eight_points.transpose()

    return corner_box.transpose()