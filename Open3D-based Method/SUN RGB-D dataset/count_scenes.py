import numpy as np
import open3d as o3d
from pyntcloud import PyntCloud
import os

'''
The purpose of this code is to count the number of scenes without objects in the SUN RGB-D dataset
'''

Train_Path = '' #The path of the training set 
Val_Path = '' #The path of the val set 

train_num = 0
for scene in range(5051,10336):
    scene_index = ('00'+str(scene))[-6:]
    BBox_path = os.path.join(Train_Path, scene_index+'_bbox.npy')
    bbox_data = np.load(BBox_path)
    if bbox_data.shape[0]==0:
        train_num+=1
print(f"The number of scenes without objects in the SUN RGB-D training dataset is {train_num}.")

test_num = 0
for scene in range(1,5051):
    scene_index = ('00000'+str(scene))[-6:]
    BBox_path = os.path.join(Val_Path, scene_index+'_bbox.npy')
    bbox_data = np.load(BBox_path)
    if bbox_data.shape[0]==0:
        test_num+=1
print(f"The number of scenes without objects in the SUN RGB-D test dataset is {test_num}.")