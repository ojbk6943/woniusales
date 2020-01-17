

import re

msgs = '1350000000'

result = re.match('^1[3456789]\d{9}$', msgs)
print(result)
if result:
    print(result.group())
else:
    print("buzhi")