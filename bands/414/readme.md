# 414 Wild-Linx 带子

## Feature分类

1. BaseGame
2. fakePick
3. WildLinxEvaluate

## Slot

每次slot给到一个长度为5的带子片段，实际牌面长度为3，有一个固定的index来从带子中选择牌面

## 拼接

现在只有长度为5的带子片段，需要拼接原长度未知的带子

采用穷举遍历的方法，将所有可能的拼接方式都尝试一遍。每次固定一个带子，然后遍历所有的带子片段，如果能找到唯一一个有重叠的片段，就将其拼接到一起。然后将结果放回去继续遍历下一个带子片段，递归直到没有新的拼接发生。

## Code

1. extract.py: 从原始ws数据中提取长度为5的带子片段，保存为json文件
2. json2csv.py: 其中有`read_column`函数从json文件中读取需要的带子片段；`get_frequency`函数计算每个带子片段的频率返回一个字典；`save_to_csv`函数将带子和频率的字典保存为csv文件
3. reconstruct.py: 拼接函数，将所有可能的拼接方式都尝试一遍，返回拼接后的带子
4. main.py: 主函数，调用以上函数，实现从原始数据到拼接后的带子

运行代码：

```bash
python3 main.py
```
