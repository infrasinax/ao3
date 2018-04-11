#/usr/bin/env python
# encoding: utf-8

import platform
if platform.dist()[0] == "Red Hat":
    print("Red Hat use o yum ")
elif platform.dist()[0] == "CentOS":
    print("CentOS use o yum")
elif platform.dist()[0] == "Debian":
    print("Debian use o apt-get")
elif platform.dist()[0] == "Ubuntu":
    print("Ubuntu use o apt-get")
else:
    print("Não te conheço")

