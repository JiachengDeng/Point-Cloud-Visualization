# Point-Cloud-Visualization
This repository is build for point cloud visualization and 3D point cloud object detection related visualization.
Our open source of 3D point cloud visualization is based on Open3D and Mitsuba0.5.0.
## Open3D-based Method
Reference: <a href="https://github.com/isl-org/Open3D" title="Open3D">Open3D</a>

### Inroduction
We develop this visualization method based on `Open3D`.

### 🔥Pros&Cons
✔️ **Real-time**

✔️ **Free Viewing Angle and Distance**

❌ **Rough Rendering**

❌ **Too Thin Lines of Bounding Boxes** (**TODO**: This can be optimized by `/Open3D-based Method/ScanNetV2 dataset/better_visualization.py`)

### 👇Some demos

<div align=center>
<img src="https://github.com/JiachengDeng/Point-Cloud-Visualization/raw/main/resources/Open3D_ScanNetV2.jpg" width = "600" height = "600" alt="A demo of a scene in the ScanNetV2 dataset with Open3D" />

<img src="https://github.com/JiachengDeng/Point-Cloud-Visualization/raw/main/resources/Open3D_SUNRGBD.jpg" width = "600" height = "600" alt="A demo of a scene in the SUN RGB-D dataset with Open3D" />

![demo image](https://github.com/JiachengDeng/Point-Cloud-Visualization/raw/main/resources/ScanNetV2.gif)

![demo image](https://github.com/JiachengDeng/Point-Cloud-Visualization/raw/main/resources/SUNRGBD.gif)
  
</div>

## Mitsuba0.5.0-based Method
Reference: <a href="https://www.mitsuba-renderer.org/devblog/2014/02/mitsuba-0-5-0-released/" title="Mitsuba-renderer0.5.0">Mitsuba-renderer0.5.0</a>

### Inroduction
We develop this visualization method based on `Mitsuba` and the software can be downloaded from the link below.

Download: <a href="http://www.mitsuba-renderer.org/releases/current/windows/" title="Mitsuba0.5.0-releases">Mitsuba0.5.0-releases</a> 

### 🔥Pros&Cons
✔️**High Quality Rendering**

✔️ **You can set the viewing angle, resolution, etc.**

❌ **Rendering takes a long time**

### 👇Some demos

![Aaron Swartz](https://github.com/JiachengDeng/Point-Cloud-Visualization/raw/main/resources/Mitasuba_ScanNetV2.png)
![Aaron Swartz](https://github.com/JiachengDeng/Point-Cloud-Visualization/raw/main/resources/Mitasuba_SUNRGBD.png)

# Dataset preparation

We follow the VoteNet codebase for preprocessing our data.
The instructions for preprocessing SUN RGB-D are [here](https://github.com/facebookresearch/votenet/tree/main/sunrgbd) and ScanNet are [here](https://github.com/facebookresearch/votenet/tree/main/scannet).🎉

If you think processing data is too cumbersome for you but want to try our visualization software, we have prepared mini data in the `mini-data` folder for you!✨

# 👇Attention Plz!!!
Please pay attention to this issue:
https://github.com/facebookresearch/3detr/issues/3
