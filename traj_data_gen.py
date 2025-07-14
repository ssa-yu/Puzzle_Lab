import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random, os, json

def draw_volleyball_court(ax):
    points = np.array([
        [0, 0, 0], [9, 0, 0], [0, 6, 0], [9, 6, 0],
        [0, 9, 0], [9, 9, 0], [0, 12, 0], [9, 12, 0],
        [0, 18, 0], [9, 18, 0]
    ])
    courtedge = [2, 0, 1, 3, 2, 4, 5, 3, 5, 7, 6, 4, 6, 8, 9, 7]
    curves = points[courtedge]

    ax.plot(curves[:, 0], curves[:, 1], curves[:, 2], c='k', linewidth=1)
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='black', s=1)

def generate_parabola(start, end, angle_deg=45, num_points=50, max_height=3):
    t = np.linspace(0, 1, num_points)
    x = start[0] + (end[0] - start[0]) * t
    y = start[1] + (end[1] - start[1]) * t

    base_height = np.linalg.norm(np.array(end) - np.array(start))
    raw_height = base_height * random.uniform(0.3, 1.0) * np.sin(np.radians(angle_deg))
    height = min(raw_height, max_height)

    z = start[2] + (end[2] - start[2]) * t + height * 4 * (t - t**2)
    return np.vstack((x, y, z)).T

def generate_connected_trajectory(num_segments=5, bounds=([1,8], [1,17], [0.5,2.5])):
    segments = []
    current_point = np.array([
        random.uniform(*bounds[0]),
        random.uniform(*bounds[1]),
        random.uniform(*bounds[2])
    ])

    for _ in range(num_segments):
        next_point = np.array([
            random.uniform(*bounds[0]),
            random.uniform(*bounds[1]),
            random.uniform(*bounds[2])
        ])
        angle = random.uniform(5, 90)
        parabola = generate_parabola(current_point, next_point, angle_deg=angle)
        segments.append(parabola)
        current_point = next_point

    return segments

def draw_generated_trajectory(folder, filename):
    num_segments = random.randint(2, 5)
    segments = generate_connected_trajectory(num_segments=num_segments)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    draw_volleyball_court(ax)

    # 預先定義顏色名稱，隨機選取
    color_names = ["red", "blue", "green", "orange", "cyan"]
    random.shuffle(color_names)
    selected_colors = color_names[:num_segments]

    print("color list")
    color_list = []
    for i, (seg, color_name) in enumerate(zip(segments, selected_colors)):
        xs, ys, zs = seg[:, 0], seg[:, 1], seg[:, 2]
        print(f"{color_name} ")
        ax.plot(xs, ys, zs, color=color_name, linewidth=2)
        color_list.append(color_name)
    
    color_list_reverse = color_list[::-1]  

    json_data = {
        "image_id": filename,
        "format": "png",
        "color_list": [color_list,color_list_reverse]
    }

    ax.set_xlim(0, 9)
    ax.set_ylim(0, 18)
    ax.set_zlim(0, 5)
    ax.view_init(elev=5, azim=195)

    # 美化設定
    ax.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    
    plt.tight_layout()

    plt.savefig(os.path.join(folder ,f"{filename}.png"), dpi=300, bbox_inches='tight')

    ax.view_init(elev=95, azim=195)
    plt.savefig(os.path.join(folder ,f"{filename}_2.png"), dpi=300, bbox_inches='tight')

    plt.close(fig)   
    print("image saved!")
    return json_data

# ✅ 執行
if __name__ == "__main__":
    base_path = 'dataset'
    folder_path = 'dataset/image'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    datas = []
    for i in range(1, 101):
        data = draw_generated_trajectory(folder=folder_path, filename = i)
        datas.append(data)
    
    with open(os.path.join(base_path, 'answer.json'), 'w') as json_file:
        json.dump(datas, json_file, indent=4)
    print("json saved!")