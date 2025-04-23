"""
项目2: L-System分形生成与绘图模板
请补全下方函数，实现L-System字符串生成与绘图。
"""
import matplotlib.pyplot as plt
import math

def apply_rules(axiom, rules, iterations):
    """
    生成L-System字符串
    :param axiom: 初始字符串（如"F"或"0"）
    :param rules: 规则字典，如{"F": "F+F--F+F"} 或 {"1": "11", "0": "1[0]0"}
    :param iterations: 迭代次数
    :return: 经过多轮迭代后的最终字符串
    """
    current = axiom   # 初始化当前序列为公理（初始状态）
    for _ in range(iterations):     # 根据指定的迭代次数进行循环
        next_seq = []      # 初始化下一个序列为空列表
        for c in current:     # 遍历当前序列中的每个字符
            next_seq.append(rules.get(c, c))       # 根据规则替换字符，若无对应规则则保留原字符
        current = ''.join(next_seq)      # 将下一个序列转换为字符串并更新当前序列
    return current     # 返回最终生成的序列

def draw_l_system(instructions, angle, step, start_pos=(0,0), start_angle=0, tree_mode=False, savefile=None):
    """
    根据L-System指令绘图
    :param instructions: 指令字符串（如"F+F--F+F"）
    :param angle: 每次转向的角度（度）
    :param step: 每步前进的长度
    :param start_pos: 起始坐标 (x, y)
    :param start_angle: 起始角度（0表示向右，90表示向上）
    :param tree_mode: 是否以树模式绘图（影响颜色和线宽）
    :param savefile: 若指定则保存为图片文件，否则直接显示
    """
    # 初始化绘图起点和角度
    x, y = start_pos  # 使用 start_pos 参数作为初始位置
    current_angle = start_angle  # 使用 start_angle 参数作为初始角度
    stack = []      # 用于存储状态的栈（位置和角度）
    fig, ax = plt.subplots()    # 创建绘图对象
    
    # 标志位，用于判断是否是树模式（根据指令中是否包含 '[' 和 ']' 判断）
    tree_mode = '[' in instructions or ']' in instructions or tree_mode
    
    # 遍历命令序列并执行相应的绘图操作
    for cmd in instructions:   # 遍历命令序列
        # 计算下一个点的坐标（基于当前角度和步长）
        if cmd in ('F', '0', '1'):
            nx = x + step * math.cos(math.radians(current_angle))
            ny = y + step * math.sin(math.radians(current_angle))
            # 绘制线段并更新当前位置
            ax.plot([x, nx], [y, ny], color='green' if tree_mode else 'blue', linewidth=1.2 if tree_mode else 1)
            x, y = nx, ny
        elif cmd == 'f':
            # 移动到下一个位置（不绘制线段）
            x += step * math.cos(math.radians(current_angle))
            y += step * math.sin(math.radians(current_angle))
        elif cmd == '+':
            # 逆时针旋转指定角度
            current_angle += angle
        elif cmd == '-':
            # 顺时针旋转指定角度
            current_angle -= angle
        elif cmd == '[':
            # 保存当前状态到栈中
            stack.append((x, y, current_angle))
            # 树模式下调整角度
            if tree_mode:
                current_angle += angle
        elif cmd == ']':
            # 从栈中恢复之前的状态
            x, y, current_angle = stack.pop()
            # 树模式下调整角度
            if tree_mode:
                current_angle -= angle
    
    # 设置绘图比例和显示效果
    ax.set_aspect('equal')
    ax.axis('off')    # 隐藏坐标轴
    if savefile:
        plt.savefig(savefile, bbox_inches='tight', pad_inches=0.1, dpi=150)
        plt.close()  # 关闭绘图窗口
    else:
        plt.show()   # 显示绘图窗口

if __name__ == "__main__":
    """
    主程序示例：分别生成并绘制科赫曲线和分形二叉树
    学生可根据下方示例，调整参数体验不同分形效果
    """
    # 1. 生成并绘制科赫曲线
    axiom = "F"  # 公理
    rules = {"F": "F+F--F+F"}  # 规则
    iterations = 3  # 迭代次数
    angle = 60  # 每次转角
    step = 10  # 步长
    instr = apply_rules(axiom, rules, iterations)  # 生成指令字符串
    draw_l_system(instr, angle, step, savefile="l_system_koch.png")  # 绘图并保存

    # 2. 生成并绘制分形二叉树
    axiom = "0"
    rules = {"1": "11", "0": "1[0]0"}
    iterations = 5
    angle = 45
    instr = apply_rules(axiom, rules, iterations)
    draw_l_system(instr, angle, step, tree_mode=True, savefile="fractal_tree.png")
