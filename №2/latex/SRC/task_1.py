import re

print("В усіх словах, що складаються з 5ти букв 2 останні буде замінено на \"xz\". Введіть рядок...")
s = input()
re_words = re.compile(r"([^A-ґ']|^)([A-ґ]+'?[A-ґ]*)([\.\,\!\?]?)")

s = re_words.sub(
    lambda match:
    match[1] + re.sub(r"(.*)([A-ґ]{1})('?)([A-ґ]{1})('|$)", r"\1x\3z\5", match[2]) + match[3]
    if
        len(match[2]) - match[2].count("'") == 5
    else
        match[0],
    s,
)
print(s)
