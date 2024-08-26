# 414 Wild-Linx 带子

## Feature分类

1. BaseGame
2. FreeSpin
   1. FreeLinXFeature
   2. FreeStacksFeature
3. WildLinXFeature

## Slot

每次slot给到一个长度为5的带子片段，实际牌面长度为3。从带子片段中取牌面的时候偏移到index=1的位置开始，取3个icon。

图标有种类变化，X图标和arrow图标在赋值的时候会被替换成其他图标。

Free spin有两条额外带子。

## Icon

```python
transDict = {"0": "1101", "11": "1201", "10": "1202","1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005", "6": "1006", "7": "1007", "8": "1008"}

offset = 1

def convert_rule(lst):

    # 将不同倍率的箭头替换为11
    res = list(map(lambda x: '11' if int(x) in [
               18, 19, 20, 21, 22, 23, 24] else x, lst))

    # 替换不同倍率x图标为0
    res = list(map(lambda x: '0' if int(x) in [
               13, 14, 32, 15, 27, 28, 17, 29, 30, 36] else x, res))
    return res
```

## Code

运行代码：

```bash
python3 main.py
```
