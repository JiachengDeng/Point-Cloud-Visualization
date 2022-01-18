import numpy as np
import os
import argparse
import scipy.linalg as linalg
import math

def rotate_mat(axis, radian):
    rot_matrix = linalg.expm(np.cross(np.eye(3), axis / linalg.norm(axis) * radian))
    return rot_matrix

def rotate(pcd,axis,yaw):
    # axis_x, axis_z, axis_y = [1,0,0](指着右后), [0,1,0](指着天上), [0, 0, 1](指着右前)
    yaw = math.pi/180*yaw
    rot_matrix = rotate_mat(axis, yaw)
    pcd = np.dot(pcd,rot_matrix)
    return pcd

def standardize_bbox(pcl, bbox_corners):
    # pt_indices = np.random.choice(pcl.shape[0], points_per_object, replace=False)
    # np.random.shuffle(pt_indices)
    # pcl = pcl[pt_indices]  # n by 3
    mins = np.amin(pcl, axis=0)
    maxs = np.amax(pcl, axis=0)
    center = (mins + maxs) / 2.0
    scale = np.amax(maxs - mins)
    print("Center: {}, Scale: {}".format(center, scale))
    pcl_result = ((pcl - center) / scale).astype(np.float32)  # [-0.5, 0.5]
    bbox_result = ((bbox_corners - center) / scale).astype(np.float32)  # [-0.5, 0.5]
    return pcl_result, bbox_result



def box_center_to_corner(box):
    # To return
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

xml_head = """
<scene version="0.5.0">
    <integrator type="path">
        <integer name="maxDepth" value="-1"/>
    </integrator>
    <sensor type="perspective">
        <float name="farClip" value="100"/>
        <float name="nearClip" value="0.1"/>
        <transform name="toWorld">
            <lookat origin="{},{},{}" target="0,0,0" up="0,0,1"/>
        </transform>
        <float name="fov" value="{}"/>
        
        <sampler type="ldsampler">
            <integer name="sampleCount" value="256"/>
        </sampler>
        <film type="ldrfilm">
            <integer name="width" value="{}"/>
            <integer name="height" value="{}"/>
            <rfilter type="gaussian"/>
            <boolean name="banner" value="false"/>
        </film>
    </sensor>
    
    <bsdf type="roughplastic" id="surfaceMaterial">
        <string name="distribution" value="ggx"/>
        <float name="alpha" value="0.05"/>
        <float name="intIOR" value="1.46"/>
        <rgb name="diffuseReflectance" value="1,1,1"/> <!-- default 0.5 -->
    </bsdf>
    
"""

xml_ball_segment = """
    <shape type="sphere">
        <float name="radius" value="{}"/>
        <transform name="toWorld">
            <translate x="{}" y="{}" z="{}"/>
        </transform>
        <bsdf type="diffuse">
            <rgb name="reflectance" value="{},{},{}"/>
        </bsdf>
    </shape>
"""

xml_bar_segment = """
    <shape type="cylinder">
        <float name="radius" value="{}"/>
        <point name="p0" x="{}" y="{}" z="{}"/>
        <point name="p1" x="{}" y="{}" z="{}"/>
        <bsdf type="twosided">
            <bsdf type="diffuse">
                <rgb name="reflectance" value="{},{},{}"/>
            </bsdf>
        </bsdf>
    </shape>
"""

xml_bar_segment_ex = """
    <shape type="cylinder">
        <float name="radius" value="{}"/>
        <point name="p0" x="{}" y="{}" z="{}"/>
        <point name="p1" x="{}" y="{}" z="{}"/>
        <transform name="toWorld">
            <translate x="{}" y="{}" z="{}"/>
        </transform>
        <bsdf type="twosided">
            <bsdf type="diffuse"/>
        </bsdf>
    </shape>
"""

xml_tail = """
    <shape type="rectangle">
        <ref name="bsdf" id="surfaceMaterial"/>
        <transform name="toWorld">
            <scale x="10" y="10" z="1"/>
            <translate x="0" y="0" z="{}"/>
        </transform>
    </shape>
    
    <shape type="rectangle">
        <transform name="toWorld">
            <scale x="10" y="10" z="1"/>
            <lookat origin="-4,4,20" target="0,0,0" up="0,0,1"/>
        </transform>
        <emitter type="area">
            <rgb name="radiance" value="6,6,6"/>
        </emitter>
    </shape>
</scene>
"""


def colormap(x, y, z, mode):
    if mode == "gradient":
        vec = np.array([x, y, z])
        vec = np.clip(vec, 0.001, 1.0)
        norm = np.sqrt(np.sum(vec ** 2))
        vec /= norm
        return [vec[0], vec[1], vec[2]]
    elif mode == "gray":
        return [0.5, 0.5, 0.5]
    elif mode == "red":
        return [1.0, 0.0, 0.0]
    elif mode == "blue":
        return [0.0, 0.0, 1.0]
    elif mode == "green":
        return [0.0, 1.0, 0.0]
    elif mode == "color1":
        return [0.5, 0.5, 0.5]
    elif mode == "color2":
        return [0.7, 0.4, 0.4]
    elif mode == "color3":
        return [0.85, 0.45, 0.15]
    elif mode == "color4":
        return [0.4, 0.4, 0.7]
    elif mode == "color5":
        return [0.3, 0.6, 0.6]
    elif mode == "color6":
        return [0.5, 0.5, 0.3]

def paint_pcl(in_path, out_path, args):
    w, h = [int(v) for v in args.size.split("x")] #像素w, h
    eye = [float(v) for v in args.eye.split(',')] #视角？
    xml_segments = [xml_head.format(eye[0], eye[1], eye[2], args.fov, w, h)] #.format格式化函数输入  #开头

    pcl = np.load(in_path+'_pc.npz', allow_pickle=True)['pc']  #读入场景点云数据（n, 6）
    print(pcl.shape)
    colors = pcl[:,3:]  #(40000,3)

    pcl = pcl[:,0:3] #(40000,3)
    print(pcl.shape)
    
    for i in range(len(args.axis)): #旋转
        pcl = rotate(pcl,args.axis[i],args.yum[i])
    
    #bbox related
    bbox=np.load(in_path+'_bbox.npy') #读入GT建议框数据(M, 8)[x, y, z, l, w, h, theta, semantic label]
    print(bbox.shape)
    print(bbox)
    bbox_corners = np.zeros([bbox.shape[0], 8, 3]) #cornor (M,8,3)
    for k in range(len(bbox)):
        bbox_corners[k] = box_center_to_corner(bbox[k])

    for i in range(len(args.axis)): #旋转
        for k in range(len(bbox_corners)):
            bbox_corners[k] = rotate(bbox_corners[k],args.axis[i],args.yum[i])
          

    xml_path = out_path + ".xml"

    pcl, bbox_corners = standardize_bbox(pcl, bbox_corners)
    pcl = pcl[:, [2, 0, 1]]
    pcl[:, 0] *= -1
    pcl[:, 2] += 0.0125

    bbox_corners = bbox_corners[..., [2, 0, 1]] 
    bbox_corners[..., 0] *= -1
    bbox_corners[:, 2] += 0.0125

    #draw point cloud
    for i in range(pcl.shape[0]):
        # color = colormap(pcl[i, 0] + 0.5, pcl[i, 1] + 0.5, pcl[i, 2] + 0.5 - 0.0125, mode=args.colormode) 
        color = colors[i]
        xml_segments.append(xml_ball_segment.format(args.radius, pcl[i, 0], pcl[i, 1], pcl[i, 2], *color))

    #draw bbox
    lines = [[0, 1], [1, 2], [2, 3], [0, 3],
        [4, 5], [5, 6], [6, 7], [4, 7],
        [0, 4], [1, 5], [2, 6], [3, 7]]
    
    rgb = [[1,1,0],[0,1,0],[0,0,1],[1,0,0]]
    for i in range(bbox_corners.shape[0]):
        bbox_corners_points = bbox_corners[i] #(8, 3)
        for j in range(12):
            xml_segments.append(xml_bar_segment.format(args.bar_radius, bbox_corners_points[lines[j][0], 0], bbox_corners_points[lines[j][0], 1], bbox_corners_points[lines[j][0], 2], bbox_corners_points[lines[j][1], 0], bbox_corners_points[lines[j][1], 1], bbox_corners_points[lines[j][1], 2], *args.bar_color))
    z = np.min(pcl[:, 2])
    xml_segments.append(xml_tail.format(z - args.radius)) #收尾
    xml_content = str.join("", xml_segments)
    with open(xml_path, "w") as f:
        f.write(xml_content)

    import sys

    sys.path.append("./Mitsuba_0.5.0/")

    # xml_path = os.path.abspath(xml_path)
    print(xml_path)
    assert os.path.exists(xml_path)
    os.system(f'"render\\Mitsuba_0.5.0\\mitsuba.exe" {xml_path} -j 1 -q')

    os.remove(xml_path)

def each_from(folder):
    for name in os.listdir(folder):
        subroot = os.path.join(folder, name)
        for subname in os.listdir(subroot):
            if subname.endswith("results.npy"):
                info = dict(
                    name=name,
                    pcd_path=os.path.join(subroot, subname),
                )
                yield info


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)  #根目录 lauch.json里设置
    parser.add_argument("output_folder", type=str) #根目录 lauch.json里设置
    parser.add_argument("--radius", default=0.005, type=float)  #球的半径 radius of the ball
    parser.add_argument("--size", default="1000x1000", type=str)  #渲染分辨率 rendering resolution
    parser.add_argument("--colormode", default="gradient", type=str) #颜色模式 color mode
    parser.add_argument('--eye', default='1.5,1.5,1.5', type=str)  #视角？ Perspective? (maybe)
    parser.add_argument('--fov', default=25, type=float)  #视场 Field of View
    parser.add_argument('--axis', default=[[1,0,0],[0,1,0],[0,0,1]], type=list) #旋转的轴 axis of rotation
    parser.add_argument('--yum', default=[110,30,10], type=list)  #轴向{左，上，前} 顺时针旋转度数 Rotate clockwise by degrees {left, up, front}
    parser.add_argument('--bar_radius', default=0.005, type=float) #框的粗细 the thickness of the box
    parser.add_argument("--bar_color", default=[1, 0, 0], type=list) #boundding box color [R, G, B]
    args = parser.parse_args()

    k = 5051 #the index of scenes 1~10335
    scene_num = ('00000'+str(k))[-6:]
    input_path = os.path.join(args.path, scene_num)
    paint_pcl(input_path, args.output_folder, args) # 输入路径、 输出路径、 args设置 （input path, output path, args settings）
