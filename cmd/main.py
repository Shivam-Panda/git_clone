# When finished with entire script, build with 'pyinstaller {file_name}.py'
# When finished with entire script, build with 'pyinstaller main.py'

import sys

try:
    files = sys.argv[1::]
    for i in files:
        print(open(i).read())
except:
    print('No Valid Arguement Given')
