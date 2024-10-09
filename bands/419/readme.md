# 419 Zodiac 带子

## Feature分类

1. baseReels
2. baseInfinityReels
3. wheelFeature
4. freeReels
5. freeInfinityReels

## Slot

单次spin为一个request，初始为baseReels，每次spin后返回icon及index。新加的reel叫infinityReels，每次spin后返回icon及index。wheelFeature中直接记录了每次spin wheel的结果。

## Icon

```python
transDict = {"Z": "1101", "S": "1201",
             "B": "1001", "C": "1002", "D": "1003", "E": "1004", "A": "1005", "K": "1006", "Q": "1007", "J": "1008", "T": "1009", "N": "1010"}

```

## Code

运行代码：

```bash
python3 main.py
```
