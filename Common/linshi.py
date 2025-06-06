# 高级用法

from tqdm import tqdm
# tqdm库是一个可以很方便地在Python循环操作中输出进度条的库

# 可迭代对象（Iterable）
# 迭代器（Iterator)

# 列表生成式
"""
# 带 if过滤
res = [i * i for i in range(11) if i % 2 == 0]
print(res)

# 双重循环
res = [i + j for i in range(5) for j in range(6, 11)]
print(res)

# 包含函数
L = ['Hello', 'World', 'IBM', 'Apple']
res = [s.lower() for s in L]
print(res)

# 包含 if...else
res = [i if i % 2 == 0 else "奇数" for i in range(11)]
print(res)


# generator生成器
# 只要把一个列表生成式的 [] 改成 () ，就创建了一个 generator
# 列表
L = [x * x for x in range(10)]
print(L)
print(type(L))
# 生成器
L = (x * x for x in range(10))
print(L)
print(type(L))

# for打印生成器每个元素
L2 = (x * x for x in range(10))
for i in L2:
    print(i)

# next() 方法 可以获取 generator 的下一个元素
L2 = (x * x for x in range(10))
print(next(L2))
print(next(L2))
print(next(L2))


def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1

b = fib(8)
# for打印生成器每个元素
for i in b:
    print(i)
print(fib(8))


 # 执行流程
def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield 3
    print('step 3')
    yield 5

L = odd()
for i in L:
    print(i)

# 批量生成示例，占用大量内存
def test():
    for i in tqdm(range(10000000)):
        temp = ['你好'] * 2000
        yield temp

# 生成式批量生成示例，减少内存占用
def test():
    for i in tqdm(range(10000000)):
        temp = ['你好'] * 2000
        yield temp


a = test()
for ele in a:
    continue


# 可以使用 isinstance() 判断一个对象是否是 Iterator 对象
# 集合数据类型如 list、dict、str 等是 Iterable 但不是 Iterator
print(isinstance([], Iterator))
print(isinstance({}, Iterator))
print(isinstance("test", Iterator))
print(isinstance(1234, Iterator))
print(isinstance([x for x in range(2)], Iterator))
print(isinstance((x for x in range(2)), Iterator))
print(isinstance(enumerate([]), Iterator))



# 把 list、dict、str 等 Iterable 变成 Iterator 可以使用 iter() 函数
print(isinstance(iter({}), Iterator))
print(isinstance(iter("test"), Iterator))
print(isinstance(iter([x for x in range(2)]), Iterator))
"""


import pandas as pd
import qrcode


def excel_to_qrcode_cp(file_path, sheet_name, column_name):
    # 读取Excel文件
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 获取指定列的数据
    data = df[column_name].tolist()

    # 生成二维码并保存为图片
    for item in data:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(str(item))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # img.save(f"{item}.png")
        img.save(f"D:\project\create\TestDatas\cb.png")


def excel_to_qrcode_cp2(file_path, sheet_name, column_name):
    # 读取Excel文件
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 获取指定列的数据
    # data = df[column_name].tolist()

    data = "我爱你"

    # 生成二维码并保存为图片
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data.encode('utf-8'))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # img.save(f"{item}.png")
    img.save(f"D:\project\create\TestDatas\cb.png")


def excel_to_qrcode(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 将整个Excel文件转换为字符串
    data = df.to_string(index=False)


    # 生成二维码并保存为图片
    qr = qrcode.QRCode(version=10, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"D:\project\create\TestDatas\cb.png")

# 使用示例
file_path = "D:\project\create\TestDatas\md5.xlsx"  # Excel文件路径
sheet_name = "Sheet1"  # 工作表名称
column_name = "md5"  # 列名，包含要转换为二维码的数据

excel_to_qrcode_cp2(file_path, sheet_name, column_name)
# excel_to_qrcode(file_path)
