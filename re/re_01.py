import re

finditer = re.finditer(r'\d+', '123abc456abc789')
print(type(finditer), finditer)
for match in finditer:
    print(match, match.group())
