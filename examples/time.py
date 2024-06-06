import timeit

import pacdb

def test():
    pacdb._split_depends(["blah-blah>=2.3.4a: Goof"])

if __name__ == "__main__":
    print(timeit.repeat("test()", "from __main__ import test", number=100000))
 
