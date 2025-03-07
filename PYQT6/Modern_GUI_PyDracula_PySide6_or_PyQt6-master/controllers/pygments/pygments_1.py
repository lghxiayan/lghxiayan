from pygments.lexers import get_all_lexers

# 获取所有 lexer 的别名
all_lexers = {alias for _, _, aliases, _ in get_all_lexers() for alias in aliases}

if 'ansi' in all_lexers:
    print("Lexer with alias 'ansi' is available.")
else:
    print("Lexer with alias 'ansi' is NOT available.")
