# 导入必要的库
import numpy as np  # 用于数值计算
import matplotlib.pyplot as plt  # 用于绘图

def get_fern_params():
    """返回巴恩斯利蕨的IFS参数
    
    每个变换包含6个参数(a,b,c,d,e,f)和概率p
    这些参数定义了仿射变换的矩阵和平移向量
    """
    return [
        [0.00, 0.00, 0.00, 0.16, 0.00, 0.00, 0.01],   # 茎干 - 产生蕨类的主要茎干部分
        [0.85, 0.04, -0.04, 0.85, 0.00, 1.60, 0.85],   # 小叶片 - 产生蕨类的小叶片部分
        [0.20, -0.26, 0.23, 0.22, 0.00, 1.60, 0.07],   # 左侧大叶片 - 产生蕨类左侧的大叶片
        [-0.15, 0.28, 0.26, 0.24, 0.00, 0.44, 0.07]    # 右侧大叶片 - 产生蕨类右侧的大叶片
    ]

def get_tree_params():
    """返回概率树的IFS参数
    
    每个变换包含6个参数(a,b,c,d,e,f)和概率p
    这些参数定义了树的生成规则
    """
    return [
        [0.00, 0.00, 0.00, 0.50, 0.00, 0.00, 0.10],    # 树干 - 产生树的主干部分
        [0.42, -0.42, 0.42, 0.42, 0.00, 0.20, 0.45],   # 左分支 - 产生向左生长的分支
        [0.42, 0.42, -0.42, 0.42, 0.00, 0.20, 0.45]    # 右分支 - 产生向右生长的分支
    ]

def apply_transform(point, params):
    """应用单个变换到点
    
    :param point: 二维点坐标(x,y)
    :param params: 变换参数列表[a,b,c,d,e,f,p]
    :return: 变换后的新点坐标
    """
    x, y = point  # 解包当前点坐标
    a, b, c, d, e, f, _ = params  # 解包变换参数(忽略概率p)
    # 应用仿射变换: x' = a*x + b*y + e
    #               y' = c*x + d*y + f
    return a*x + b*y + e, c*x + d*y + f

def run_ifs(ifs_params, num_points=100000, num_skip=100):
    """
    运行IFS迭代生成点集
    
    :param ifs_params: IFS参数列表，每个元素是一个变换的参数列表
    :param num_points: 要生成的总点数，默认为100000
    :param num_skip: 跳过前n个点(避免初始不稳定)，默认为100
    :return: 生成的点坐标数组，形状为(num_points, 2)
    """
    # 提取每个变换的概率用于随机选择
    probs = [p[-1] for p in ifs_params]
    indices = np.arange(len(ifs_params))  # 变换的索引数组
    
    # 初始化点集
    point = (0.5, 0)  # 初始点坐标
    points = np.zeros((num_points, 2))  # 预分配结果数组
    
    # 迭代生成点
    for i in range(num_points + num_skip):
        # 根据概率随机选择一个变换
        idx = np.random.choice(indices, p=probs)
        # 应用选定的变换到当前点
        point = apply_transform(point, ifs_params[idx])
        
        # 跳过初始不稳定点(让系统达到稳定状态)
        if i >= num_skip:
            points[i - num_skip] = point  # 存储生成的点
            
    return points

def plot_ifs(points, title="IFS Fractal", save_path=None):
    """绘制IFS分形并保存为PNG
    
    :param points: 要绘制的点集数组
    :param title: 图像标题，默认为"IFS Fractal"
    :param save_path: 图像保存路径，如果为None则不保存
    """
    plt.figure(figsize=(8, 8))  # 创建8x8英寸的图形
    # 绘制散点图，点大小为1，颜色为绿色，透明度0.75
    plt.scatter(points[:,0], points[:,1], s=1, c='green', alpha=0.75)
    plt.title(title)  # 设置标题
    plt.axis('equal')  # 设置坐标轴比例相等
    plt.axis('off')  # 关闭坐标轴显示
    
    if save_path:
        # 保存图像，设置紧密边框和高DPI(300)
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()  # 显示图像

if __name__ == "__main__":
    # 生成并绘制巴恩斯利蕨
    fern_params = get_fern_params()  # 获取蕨类参数
    fern_points = run_ifs(fern_params)  # 运行IFS生成点集
    plot_ifs(fern_points, "Barnsley Fern", "barnsley_fern.png")  # 绘制并保存
    
    # 生成并绘制概率树
    tree_params = get_tree_params()  # 获取树参数
    tree_points = run_ifs(tree_params)  # 运行IFS生成点集
    plot_ifs(tree_points, "Probability Tree", "probability_tree.png")  # 绘制并保存
