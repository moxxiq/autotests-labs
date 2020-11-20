import re

print("""В усіх словах, що складаються з 5ти
букв 2 останні буде замінено на "xz". Введіть рядок...""")
s = input()
re_words = re.compile(r"[A-ґ']+")

s = re_words.sub(
    lambda match: match[0][:-2] + 'xz' if len(match[0]) == 5 else match[0],
    s,
)
print(s)
