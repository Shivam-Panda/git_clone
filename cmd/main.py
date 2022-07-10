# When finished with entire script, build with 'pyinstaller {file_name}.py'
# When finished with entire script, build with 'pyinstaller main.py'

import json
import os
import sys

c = sys.argv[0]

cmd = sys.argv[1]

storage_dir = c[0:len(c)-7] + 'storage.json'

def logout():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj['username'] = None
    cur_obj['password'] = None
    open(storage_dir, "w").write(json.dumps(cur_obj))
    r_storage = open(storage_dir, "r").read()
    obj = json.loads(r_storage)

def write_file(s, file_name):
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj[file_name] = s
    open(storage_dir, "w").write(json.dumps(cur_obj))
    r_storage = open(storage_dir, "r").read()
    obj = json.loads(r_storage)

def clear():
    open(storage_dir, "w").write('{}')

def login(username, password):
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj['username'] = username
    cur_obj['password'] = password
    open(storage_dir, "w").write(json.dumps(cur_obj))
    r_storage = open(storage_dir, "r").read()
    obj = json.loads(r_storage)
    
def reset_files():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    obj = {
        'username': cur_obj['username'],
        'password': cur_obj['password']
    }
    open(storage_dir, "w").write(json.dumps(obj))

def get_login():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    return [cur_obj['username'], cur_obj['password']]

def open_folder(f, names):
    for i in f:
        if i.__contains__('.'):
            dir = './'
            for j in names:
                dir += j
                dir += '/'
            dir += i
            write_file(open(dir).read(), i)
        else:
            dir = './'
            ns = []
            for j in names:
                ns.append(j)
                dir += j
                dir += '/'
            ns.append(i)
            write_file("Folder", i)
            dir += i
            s = os.listdir(dir)
            open_folder(s, ns)

def reset():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    obj = {}
    open(storage_dir, "w").write(json.dumps(obj))

if cmd == 'add':
    files = sys.argv[2::]
    if files[0] == '.':
        # Get All Files in current folder
        files_in_dir = os.listdir('./')
        for i in files_in_dir:
            if i.__contains__('.'):
                write_file(open(i).read(), i)
            else:
                f = os.listdir(i)
                write_file("Folder", i)
                open_folder(f,[i])
    else:
        for i in files:
            if i.startswith('./'):
                f = os.listdir(i)
                open_folder(f,[i])
            else:
                write_file(open(i).read(), i)
elif cmd == 'login':
    user = sys.argv[2]
    passw = sys.argv[3]
    login(user, passw)
elif cmd == 'get_login':
    get = get_login()
    print('Username: ' + get[0])
    print('Password: ' + get[1])
elif cmd == 'logout':
    logout()
elif cmd == 'reverse':
    reset_files()
elif cmd == 'hard_reset':
    reset()
else:
    print('Invalid Input, try again')
