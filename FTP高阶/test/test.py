# -*- coding: UTF-8 -*-

import hashlib
a = '123123'

m = hashlib.md5()
m.update(b'a')
print(m.hexdigest())
