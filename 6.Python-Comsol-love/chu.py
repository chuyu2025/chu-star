import json
import os
import mph
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import json
import numpy as np
import pandas as pd
import os
import matplotlib

# 读取 JSON 文件
json_path = os.path.join('TI_data', 'filter_float_data_com.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)


def comsol_solve(coor_scatter, num_lattice):
    """
    将结构数据导入到comsol中并返回仿真结果

    参数:
    coor_scatter (numpy.ndarray): 结构数据
    num_lattice (int): 晶格常数
    """
    # 1. 启动Comsol客户端并加载模型
    print("正在启动Comsol客户端...")
    client = mph.start()
    print("正在加载模型 com.mph...")
    model = client.load('com.mph')
    print("模型加载成功！\n")

    ##########################
    # 检查模型
    # 获取所有参数（字典形式）
    params = model.parameters()
    print(params)
    # 带描述的参数列表
    for (name, value) in model.parameters().items():
        description = model.description(name)
        print(f'{description:20} {name} = {value}')

    # 获取所有材料
    materials = model.materials()
    print(materials)

    # 获取所有物理场
    physics = model.physics()
    print(physics)

    # 获取所有研究
    studies = model.studies()
    print(studies)

    # 获取所有几何
    geometries = model.geometries()
    print(geometries)

    ##########################
    # 修改参数
    model.parameter('a', f"{num_lattice}[mm]")

    ##########################
    # 修改几何
    #首先查看一下模型树
    mph.tree(model)
    # 第一种改变几何节点参数的方法
    # 获取几何节点
    # geometries = model / 'geometries'
    # geometry = geometries / 'Geometry'
    # scatterer = geometry / 'scatterer'
    # value = scatterer.property("table")
    # print(value)
    # coor_list = coor_scatter.astype(str).tolist()
    # print(coor_list)
    # scatterer.property("table", coor_list)
    # value = scatterer.property("table")
    # print(value)
    # model.build(geometry)

    #尝试第二种改变几何节点参数的方法
    java_model = model.java
    geom = java_model.geom("geom1")
    #wp = geom.feature('wp1')
    #geom2d = wp.geom()
    pol = geom.feature('pol2')
    table_matrix = pol.getDoubleMatrix('table')
    print(table_matrix)
    rows = len(table_matrix)
    cols = len(table_matrix[0])
    np_array = np.array([[table_matrix[i][j] for j in range(cols)] for i in range(rows)])
    print(f"  NumPy 数组:\n{np_array}")
    coor_list = coor_scatter.astype(str).tolist()
    print(coor_list)
    pol.set('table', coor_list)

    # 运行研究
    print("正在运行研究 研究 1...")
    model.mesh()
    model.solve('研究 1')
    print("研究 1 运行完成")

    # 导出仿真结果
    model.exports()
    model.export('first-band-image', 'Save_TI/first-band-image.png')
    model.export('second-band-image', 'Save_TI/second-band-image')
    model.export('band-gap-figure', 'Save_TI/band-gap-figure')
    print("仿真结果导出完成")

    # 将mph文件另存为comsol_result.mph
    model.save('Save_TI/comsol_result.mph')
    print("mph文件另存为comsol_result.mph完成")

    # 获得仿真结果的拓扑带隙
    model.datasets()
    model.evaluate('freq', "k", '研究 1//参数化解 1', 'first', 1)
    band = model.evaluate('freq', "k", '研究 1//参数化解 1')
    bandgap = band.tolist()
    real_band = [element.real for element in bandgap][:2]
    real_band_float = [round(int(x), 0) for x in real_band]
    print(f"设计结果拓扑带隙: {real_band_float}")

    return real_band_float


# 提取 coordinate 和 lattice 的值
# 注意：JSON 中的键是 "Coordinate" 和 "Lattice"（首字母大写）
# 遍历所有顶层键（如 "data_1130"）
for key in data:
    item = data[key]
    # 提取 Coordinate（尝试不同大小写）
    coordinate = item.get('Coordinate') or item.get('coordinate')
    # 提取 Lattice（尝试不同大小写）
    lattice = item.get('Lattice') or item.get('lattice')
    
    if coordinate is not None and lattice is not None:
        print(f"从 {key} 中提取的数据：")
        print(f"Coordinate: {coordinate}")
        print(f"Lattice: {lattice}")
        
        # 保存到变量中供后续使用
        coordinate_data = coordinate
        lattice_data = lattice
        coordinate_data = np.array(coordinate_data)
        comsol_solve(coordinate_data, lattice_data)

        break  # 如果只需要第一个匹配项，可以添加 break

