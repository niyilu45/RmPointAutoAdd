import os
import re
import toml
from pprint import pprint
import inc.RmPointGen as RMPG

if __name__ == '__main__':
    fn = "xx.cpp"

    # ret = RMPG.Parser(fn)
    ret = RMPG.GenDefineFile(fn)
    pprint(ret)






