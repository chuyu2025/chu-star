
# MPh 库完整使用教程

> **MPh** 是一个 Python 库，用于通过脚本化方式控制 COMSOL Multiphysics 仿真软件。本教程将详细介绍 MPh 的核心功能和使用方法。

---

## 🔗 参考资源

- **官方文档**: [https://mph.readthedocs.io](https://mph.readthedocs.io)
- **GitHub 仓库**: [https://github.com/MPh-py/MPh](https://github.com/MPh-py/MPh)
- **也可以参考up主的github仓库**: [https://github.com/chuyu2025](https://github.com/chuyu2025)

---

---

## 📋 目录

1. [快速入门](#快速入门)
2. [客户端管理](#客户端管理)
3. [模型管理](#模型管理)
4. [模型检查](#模型检查)
5. [参数修改](#参数修改)
6. [几何操作](#几何操作)
7. [仿真运行](#仿真运行)
8. [结果评估](#结果评估)
9. [结果导出](#结果导出)
10. [模型保存](#模型保存)
11. [高级技巧](#高级技巧)

---

## 🚀 快速入门

### 安装

```bash
pip install mph
```

### 示例

```python
import mph

# 启动 COMSOL 客户端
client = mph.start()

# 加载模型
model = client.load('your_model.mph')

# 求解模型
model.solve()

# 评估结果
result = model.evaluate('expression', 'unit')
```

---

## 🖥️ 客户端管理

### 启动客户端

```python
import mph

# 默认启动（使用所有可用核心）
client = mph.start()

# 限制处理器核心数
client = mph.start(cores=1)
```

> **⏱️ 提示**: 客户端启动大约需要 10 秒钟。

> **⚠️ 注意**: 在同一个 Python 会话中，只能运行一个 COMSOL 客户端实例。

### 客户端信息查询

```python
# 查看所有加载的模型名称
client.names()
# 输出: ['model1', 'model2']

# 获取所有模型对象
client.models()
# 输出: [Model('model1'), Model('model2')]
```

### 清理模型

```python
# 移除特定模型
client.remove(model)

# 清除所有模型（释放内存）
client.clear()
```

---

## 📂 模型管理

### 加载模型

```python
# 从文件加载模型
model = client.load('capacitor.mph')

# 加载多个模型
model1 = client.load('model1.mph')
model2 = client.load('model2.mph')
```

### 模型树结构

```python
# 打印模型树结构
mph.tree(model)
```

---

## 🔍 模型检查

### 查看参数

```python
# 获取所有参数（字典形式）
params = model.parameters()
# 输出: {'U': '1[V]', 'd': '2[mm]', 'l': '10[mm]', 'w': '2[mm]'}

# 获取特定参数值
value = model.parameter('d')
# 输出: '2[mm]'

# 带描述的参数列表
for (name, value) in model.parameters().items():
    description = model.description(name)
    print(f'{description:20} {name} = {value}')
```

**输出示例**:
```
applied voltage      U = 1[V]
electrode spacing    d = 2[mm]
plate length         l = 10[mm]
plate width          w = 2[mm]
```

### 查看材料

```python
# 获取所有材料
materials = model.materials()
# 输出: ['medium 1', 'medium 2']
```

### 查看物理场

```python
# 获取所有物理接口
physics = model.physics()
# 输出: ['electrostatic', 'electric currents']
```

### 查看研究

```python
# 获取所有研究
studies = model.studies()
# 输出: ['static', 'relaxation', 'sweep']
```

### 查看几何

```python
# 获取所有几何序列
geometries = model.geometries()
# 输出: ['geometry']
```

### 查看数据集

```python
# 获取所有数据集
datasets = model.datasets()
# 输出: ['electrostatic', 'time-dependent', 'parametric sweep']
```

---

## ⚙️ 参数修改

### 修改全局参数

```python
# 方法1: 使用 parameter() 方法
model.parameter('d', '1[mm]')

# 方法2: 直接修改（同上）
model.parameter('a', f"{num_lattice}[mm]")

# 验证修改
print(model.parameter('d'))
# 输出: '1[mm]'
```

---

## 📐 修改几何结构

### 方法一：使用 MPh 接口修改几何 在三维结构中模型树可能只显示到工作平面那一级，所以三维结构的几何修改建议使用第二种方法

```python
# 首先查看模型树
mph.tree(model)

模型树示例：
├─ geometries
│  └─ Geometry
│     ├─ cell
│     ├─ scatterer
│     ├─ 差集 1
│     └─ 形成联合体
# 将路径导入到要修改的几何体
geometries = model / 'geometries'
geometry = geometries / 'Geometry'
scatterer = geometry / 'scatterer'

# 读取几何表格数据
value = scatterer.property("table")

# 如果待导入的几何数据coor_scatter是np格式要转换为list格式，但列表里的元素应该是字符串类型
coor_list = coor_scatter.astype(str).tolist()

# 修改几何表格数据
scatterer.property("table", coor_list)

# 构建几何
model.build(geometry)
```

### 方法二：使用 Java 接口修改几何 

```python
# 获取 Java 模型对象
java_model = model.java

# 访问几何对象
geom = java_model.geom('geom1')

# 访问工作平面（如果有）
wp = geom.feature('wp1')
geom2d = wp.geom()

# 访问多边形特征
pol = geom2d.feature('pol1')

# 读取原来的几何数据
table_matrix = pol.getDoubleMatrix('table')
rows = len(table_matrix)
cols = len(table_matrix[0])

# 打印原来的几何数据化
import numpy as np
np_array = np.array([[table_matrix[i][j] for j in range(cols)] for i in range(rows)])
print(f"NumPy 数组:\n{np_array}")

# 如果待导入的几何数据coor_scatter是np格式要转换为list表格式，但列表里的元素应该是字符串类型
coor_list = coor_scatter.astype(str).tolist()
pol.set('table', coor_list)

# 构建几何
model.build(geometry)
```

> **💡 技巧**: Java 接口提供了更底层的控制，适合复杂的几何操作。

---

## 🔬 仿真运行

### 网格划分

```python
# 生成网格
model.mesh()
```

### 求解研究

```python
# 求解特定研究，name和你的comsol中的标签名对应
model.solve('name')

# 求解所有研究
model.solve()
```

### 完整仿真流程

```python
# 1. 修改参数
model.parameter('d', '1[mm]')

# 2. 构建几何
model.build(geometry)

# 3. 生成网格
model.mesh()

# 4. 求解
model.solve('name')
```

---

## 📊 结果评估

### 全局评估

```python
# 基本评估（使用默认单位）
result = model.evaluate('2*es.intWe/U^2')
# 返回: array(1.31948342)

# 指定单位
result = model.evaluate('2*es.intWe/U^2', 'pF')
# 返回: array(1.31948342)

# 转换为 float
capacitance = float(model.evaluate('2*es.intWe/U^2', 'pF'))
```

### 局部评估（场分布）

```python
# 评估多个表达式
(x, y, E) = model.evaluate(['x', 'y', 'es.normE'])

# 查找最大值及其位置
max_field = E.max()
imax = E.argmax()
x_max, y_max = x[imax], y[imax]

print(f"最大电场强度: {max_field} V/m")
print(f"位置: ({x_max}, {y_max})")
```

### 指定数据集评估

```python
# 语法: evaluate(expression, unit, dataset, inner_index, outer_index)

# 使用默认数据集
result = model.evaluate('freq')

# 指定数据集
result = model.evaluate('freq', unit=None, dataset='研究 1//参数化解 1')

# 指定时间步（内部索引）
result = model.evaluate(C, 'pF', 'time-dependent', 'first')
result = model.evaluate(C, 'pF', 'time-dependent', 'last')

# 指定参数扫描索引（外部索引）
result = model.evaluate(C, 'pF', 'parametric sweep', 'first', 1)
result = model.evaluate(C, 'pF', 'parametric sweep', 'first', 2)
```

### 查询时间步和参数值

```python
# 查询内部解（如时间步）
(indices, values) = model.inner('time-dependent')
print(f"第一个时间步: {values[0]}")
print(f"最后一个时间步: {values[-1]}")

# 查询外部解（如参数扫描）
(indices, values) = model.outer('parametric sweep')
print(f"扫描索引: {indices}")
print(f"参数值: {values}")
```

### 实际应用示例

```python
# 提取频带数据
model.datasets()
model.evaluate('freq', "k", '研究 1//参数化解 1', 'first', 1)
band = model.evaluate('freq', "k", '研究 1//参数化解 1')

# 处理复数结果
bandgap = band.tolist()
real_band = [element.real for element in bandgap][:2]
real_band_float = [round(int(x), 0) for x in real_band]
print(f"拓扑带隙: {real_band_float}")
```

---

## 💾 结果导出

### 查看可用导出

```python
# 列出所有导出节点
exports = model.exports()
# 输出: ['data', 'image', 'first-band-image']
```

### 执行导出

```python
# 导出所有定义的输出
model.exports()

# 导出特定项（使用默认文件名）
model.export('image')

# 导出到自定义路径
model.export('image', 'static_field.png')
model.export('first-band-image', 'Save_TI/first-band-image.png')
model.export('second-band-image', 'Save_TI/second-band-image')
model.export('band-gap-figure', 'Save_TI/band-gap-figure')
```

> **📌 注意**: 如果不指定路径，文件会保存在模型文件所在目录。

---

## 💿 模型保存

### 基本保存

```python
# 覆盖原文件
model.save()

# 另存为新文件
model.save('new_model.mph')
model.save('Save_TI/comsol_result.mph')
```

> **💡 提示**: `.mph` 扩展名会自动添加（如果未包含）。

### 压缩保存（减小文件大小）

```python
# 清除解和网格数据
model.clear()

# 重置建模历史
model.reset()

# 保存压缩后的模型
model.save('capacitor_compacted')
```

---

## 🎓 高级技巧

### 1. 使用名称而非标签

✅ **推荐**:
```python
model.solve('static')  # 使用研究名称
```

❌ **不推荐**:
```python
model.solve('std1')  # 使用标签（容易改变）
```

> **原因**: MPh 库设计理念是使用名称（labels）而非标签（tags），提高代码可维护性。

### 2. 资源管理

```python
# 限制核心数（多任务场景）
client = mph.start(cores=2)

# 及时清理不用的模型
client.remove(model)

# 会话结束前清空
client.clear()
```

### 3. 错误处理

```python
try:
    model = client.load('model.mph')
    model.solve('study1')
except Exception as e:
    print(f"仿真出错: {e}")
finally:
    client.remove(model)
```

### 4. 批量参数扫描

```python
import numpy as np

results = []
for d_value in np.linspace(1, 3, 10):
    model.parameter('d', f'{d_value}[mm]')
    model.solve('static')
    result = float(model.evaluate('2*es.intWe/U^2', 'pF'))
    results.append(result)
```

### 5. 混合使用 Python 和 Java API

```python
# Python 接口（高层抽象）
model.parameter('d', '2[mm]')

# Java 接口（底层控制）
java_model = model.java
geom = java_model.geom('geom1')
pol = geom.feature('pol1')
pol.set('table', data_list)
```

---


## 📚 核心概念总结

| 概念 | 说明 |
|------|------|
| **Client** | COMSOL 客户端，管理所有模型 |
| **Model** | 单个 COMSOL 模型对象 |
| **Parameters** | 全局参数（如几何尺寸） |
| **Geometry** | 几何结构定义 |
| **Study** | 研究/求解器配置 |
| **Dataset** | 求解结果数据集 |
| **Export** | 结果导出配置 |

---

## ⚡ 快速查询表

### 常用方法

```python
# 客户端
mph.start()                    # 启动客户端
client.load('file.mph')        # 加载模型
client.names()                 # 列出模型
client.clear()                 # 清除所有模型

# 模型信息
model.parameters()             # 参数列表
model.parameter('name')        # 获取参数
model.studies()                # 研究列表
model.geometries()             # 几何列表
model.datasets()               # 数据集列表

# 模型操作
model.parameter('name', 'val') # 设置参数
model.build(geometry)          # 构建几何
model.mesh()                   # 生成网格
model.solve('study')           # 求解

# 结果处理
model.evaluate('expr', 'unit') # 评估表达式
model.inner('dataset')         # 时间步信息
model.outer('dataset')         # 参数扫描信息
model.export('name', 'path')   # 导出结果
model.save('file.mph')         # 保存模型
```

---

**文档版本**: 1.0  
**最后更新**: 2025年

Happy Simulating! 🚀
