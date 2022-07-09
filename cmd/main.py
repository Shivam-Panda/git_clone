# When finished with entire script, build with 'pyinstaller {file_name}.py'
# When finished with entire script, build with 'pyinstaller main.py'

import os
import sys

c = sys.argv[0]

cmd = sys.argv[1]

storage_dir = c[0:len(c)-7] + 'storage.txt'

def write_file(s):
    text = open(storage_dir).read()
    f = open(storage_dir, "w")
    f.write(text + '\n' + s)

def clear():
    f = open(storage_dir, "w")
    f.write("")

def login(username, password):
    f = open(storage_dir, "w")
    f.write("USERNAME:" + username + ';PASSWORD:' + password)

def getter():
    ks = open(storage_dir).read().split(';')
    print(ks)
    username = ''
    password = ''
    for i in ks:
        if i.__contains__('USERNAME:'):
            username = i[i.index(':')+1::]
        if i.__contains__('PASSWORD'):
            password = i[i.index(':')+1::]
    return [username, password]

def open_folder(f, names):
    for i in f:
        if i.__contains__('.'):
            dir = './'
            for j in names:
                dir += j
                dir += '/'
            dir += i
            write_file(open(dir).read())
        else:
            dir = './'
            ns = []
            for j in names:
                ns.append(j)
                dir += j
                dir += '/'
            ns.append(i)
            dir += i
            s = os.listdir(dir)
            open_folder(s, ns)

if cmd == 'add':
    files = sys.argv[2::]
    if files[0] == '.':
        # Get All Files in current folder
        files_in_dir = os.listdir('./')
        for i in files_in_dir:
            if i.__contains__('.'):
                write_file(open(i).read())
            else:
                f = os.listdir(i)
                open_folder(f,[i])
    else:
        for i in files:
            if i.startswith('./'):
                f = os.listdir(i)
                open_folder(f,[i])
            else:
                write_file(open(i).read())
elif cmd == 'login':
    user = sys.argv[2]
    passw = sys.argv[3]
    login(user, passw)
    getter()
elif cmd == 'logout':
    clear()
elif cmd == 'get':
    getter()
else:
    print('Invalid Input, try again')
