import numpy as np
import open3d as o3d
from pyntcloud import PyntCloud
import os

'''
The purpose of this code is to count the number of scenes without objects in the ScanNetV2 dataset
'''

Path = '' #The path of the training set 
num = 0

for scene in range(707):
    for j in range(3):
        if os.path.exists(os.path.join(Path, ('scene000'+str(scene))[:9]+'_0'+str(j)+'_bbox.npy')):
            BBox_path = os.path.join(Path, ('scene000'+str(scene))[:9]+'_0'+str(j)+'_bbox.npy')
            bbox_data = np.load(BBox_path)
            if bbox_data.shape[0]==0:
                num+=1

print(num)