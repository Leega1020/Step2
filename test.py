from collections import Counter

# 创建一个 Counter 对象来统计字符串中字符的出现次数
text = [55,66,44,33,22,66,44,55,55]
char_count = Counter(text)
r=char_count.most_common(6)
# for i in r:
#     a1,a2=i
#     print(f"{a1}:{a2}")
aa=[f"{a1}:{a2}" for a1,a2 in r]

# 统计每个字符的出现次数
print(aa)

# 输出结果
# Counter({'l': 3, 'o': 2, 'h': 1, ',': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})
