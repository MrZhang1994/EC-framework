import os
a = os.popen('cat /etc/services').read()

print(a)