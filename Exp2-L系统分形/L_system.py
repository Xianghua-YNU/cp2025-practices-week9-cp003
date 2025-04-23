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
    # TODO: 实现L-System字符串生成逻辑
    current = axiom
    for _ in range(iterations):
        next_seq = []
        for c in current:
            next_seq.append(rules.get(c, c))
        current = ''.join(next_seq)
    return current

def draw_l_system(instructions, angle, step, start_pos=(0,0), start_angle=0, savefile=None):
    """
    根据L-System指令绘图
    :param instructions: 指令字符串（如"F+F--F+F"）
    :param angle: 每次转向的角度（度）
    :param step: 每步前进的长度
    :param start_pos: 起始坐标 (x, y)
    :param start_angle: 起始角度（0表示向右，90表示向上）
    :param savefile: 若指定则保存为图片文件，否则直接显示
    """
    # TODO: 实现L-System绘图逻辑
    # 初始化绘图起点和角度
    x, y = initial_pos
    current_angle = initial_angle
    stack = []
    fig, ax = plt.subplots()
    for cmd in commands:
        if cmd in ('F', '0', '1'):
            nx = x + step * math.cos(math.radians(current_angle))
            ny = y + step * math.sin(math.radians(current_angle))
            ax.plot([x, nx], [y, ny], color='green' if tree_mode else 'blue', linewidth=1.2 if tree_mode else 1)
            x, y = nx, ny
        elif cmd == 'f':
            x += step * math.cos(math.radians(current_angle))
            y += step * math.sin(math.radians(current_angle))
        elif cmd == '+':
            current_angle += angle_deg
        elif cmd == '-':
            current_angle -= angle_deg
        elif cmd == '[':
            stack.append((x, y, current_angle))
            if tree_mode:
                current_angle += angle_deg
        elif cmd == ']':
            x, y, current_angle = stack.pop()
            if tree_mode:
                current_angle -= angle_deg
    ax.set_aspect('equal')
    ax.axis('off')
    if savefile:
        plt.savefig(savefile, bbox_inches='tight', pad_inches=0.1, dpi=150)
        plt.close()
    else:
        plt.show()
    
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
    draw_l_system(instr, angle, step, savefile="fractal_tree.png")
