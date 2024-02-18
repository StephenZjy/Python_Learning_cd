import matplotlib.pyplot as plt

# 给定的列表
data = [-137, 28, -161, -137, 23, -158, -134, 21]

# 初始化空的折线图
plt.figure()

# 用于存储x和y坐标的列表
x_values = []
y_values = []

# 逐个遍历列表中的元素并更新折线图
for i, value in enumerate(data):
    x_values.append(i)  # x坐标使用索引
    y_values.append(value)

    # 绘制折线图
    plt.plot(x_values, y_values, marker='o')

    # 刷新画布
    plt.draw()
    plt.pause(0.5)  # 控制每次刷新之间的时间间隔，单位为秒

# 最后显示图形
plt.show()
