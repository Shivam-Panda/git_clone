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

def write_folder(file_names, name):
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj[name] = file_names
    open(storage_dir, "w").write(json.dumps(cur_obj))

def write_file(s, file_name):
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj[file_name] = s
    open(storage_dir, "w").write(json.dumps(cur_obj))

def clear():
    open(storage_dir, "w").write('{}')

def login(username, password):
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj['username'] = username
    cur_obj['password'] = password
    open(storage_dir, "w").write(json.dumps(cur_obj))
    
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

def open_folder(f, names, name):
    write_folder(f, name)
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
            dir += i
            s = os.listdir(dir)
            open_folder(s, ns, i)

def reset():
    obj = {}
    open(storage_dir, "w").write(json.dumps(obj))

if cmd == 'add':
    files = sys.argv[2::]
    if files[0] == '.':
        files_in_dir = os.listdir('./')
        write_folder(files_in_dir, "root")
        for i in files_in_dir:
            if i.__contains__('.'):
                write_file(open(i).read(), i)
            else:
                f = os.listdir(i)
                open_folder(f,[i], i)
    else:
        for i in files:
            if i.startswith('./'):
                f = os.listdir(i)
                open_folder(f,[i], i)
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
