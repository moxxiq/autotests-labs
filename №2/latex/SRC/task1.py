import re

print("� ��� ������, �� ����������� � 5�� ���� 2 ������ ���� ������� �� \"xz\". ������ �����...")
s = input()
re_words = re.compile(r"([^A-�']|^)([A-�]+'?[A-�]*)([\.\,\!\?]?)")

s = re_words.sub(
    lambda match:
    match[1] + re.sub(r"(.*)([A-�]{1})('?)([A-�]{1})('|$)", r"\1x\3z\5", match[2]) + match[3]
    if
        len(match[2]) - match[2].count("'") == 5
    else
        match[0],
    s,
)
print(s)
