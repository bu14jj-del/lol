import sys
sys.path.insert(0, 'C:/Python312/Lib/site-packages')

import buildozer

class MyBuildozer(buildozer.Buildozer):
    def check_root(self):
        pass

b = MyBuildozer()
b.run_command(['android', 'debug'])