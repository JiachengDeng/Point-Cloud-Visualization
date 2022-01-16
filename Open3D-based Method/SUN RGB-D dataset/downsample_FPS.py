import numpy as np
import open3d as o3d
from pyntcloud import PyntCloud
import os

def farthest_point_sample(point, npoint):
    N, D = point.shape
    xyz = point[:,:3]
    centroids = np.zeros((npoint,))
    distance = np.ones((N,)) * 1e10
    farthest = np.random.randint(0, N)
    for i in range(npoint):
        centroids[i] = farthest
        centroid = xyz[farthest, :]
        dist = np.sum((xyz - centroid) ** 2, -1)
        mask = dist < distance
        distance[mask] = dist[mask]
        farthest = np.argmax(distance, -1)
    point = point[centroids.astype(np.int32)]
    return point
# pcd = o3d.io.read_point_cloud("piano_0015 - Cloud.pcd")     #更改为你想要读取点云的路径
point = '' #input point cloud with data shape [N,6]
point_size = point.shape[0]
sample_point = 2048   #输入想要采样的点的个数
pcd_point = farthest_point_sample(point, sample_point)  # FPS采样
pcd_finl = o3d.geometry.PointCloud()
pcd_finl.points = o3d.utility.Vector3dVector(np.asarray(pcd_point[:,0:3]))
pcd_finl.colors = o3d.utility.Vector3dVector(pcd_point[:,3:])
finl_point_size = np.asarray(pcd_finl.points).shape[0]
print("原始点云点的个数为：", point_size)
print("下采样后点的个数为：", finl_point_size)
o3d.visualization.draw_geometries([pcd_finl],
                                  mesh_show_back_face=False)