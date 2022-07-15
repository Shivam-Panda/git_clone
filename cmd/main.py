# When finished with entire script, build with 'pyinstaller {file_name}.py'
# When finished with entire script, build with 'pyinstaller main.py'

import json
import os
import sys

c = sys.argv[0]

storage_dir = './.panda/storage.json'

def logout():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj['username'] = None
    cur_obj['password'] = None
    open(storage_dir, "w").write(json.dumps(cur_obj))

def write_folder(file_names, name):
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    body = cur_obj['body']
    body[name] = file_names
    open(storage_dir, "w").write(json.dumps(cur_obj))

def write_file(s, file_name):
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    body = cur_obj['body']
    body[file_name] = s
    open(storage_dir, "w").write(json.dumps(cur_obj))

def clear():
    open(storage_dir, "w").write('{}')

def login(username, password):
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    reqs = cur_obj['reqs']
    reqs['username'] = username
    reqs['password'] = password
    cur_obj['reqs'] = reqs
    open(storage_dir, "w").write(json.dumps(cur_obj))
    
def reset_files():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj['body'] = {}
    open(storage_dir, "w").write(json.dumps(cur_obj))

def get_login():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    return [cur_obj['reqs']['username'], cur_obj['reqs']['password']]

def initializeDirStorage(projectId):
    if os.path.exists('./.panda/'):
        print('Already Exists')
        try:
            open('./.panda/storage.json', 'a')
            
        except:
            print('File Already Created')
    else:
        os.mkdir('./.panda/')
        open('./.panda/storage.json', 'a')
        open(storage_dir, "w").write(json.dumps({
            'reqs': {
                'projectId': projectId
            },
            'body': {
                'tester': None
            }
        }))

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
            write_folder(s, i)
            open_folder(s, ns, i)

def reset():
    open(storage_dir, "w").write(json.dumps({}))

try:
    cmd = sys.argv[1]
except:
    print('Error, try again')
    exit()

if cmd == 'add':
    files = sys.argv[2::]
    if files[0] == '.':
        files_in_dir = os.listdir('./')
        files_without_panda = []
        for i in files_in_dir:
            if i == '.panda':
                pass
            else:
                files_without_panda.append(i)

        write_folder(files_without_panda, "root")
        
        for i in files_in_dir:
            if i == '.panda':
                # DO NOTHING
                pass
            elif i.__contains__('.'):
                write_file(open(i, "r").read(), i)
            else:
                f = os.listdir(i)
                open_folder(f,[i], i)
    else:
        for i in files:
            if i.startswith('./'):
                f = os.listdir(i)
                open_folder(f,[i], i)
            else:
                write_file(open(i, "r").read(), i)

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
elif cmd == 'init':
    try:
        open('./.panda/storage.json')
        print('Already Initialized')
    except:
        initializeDirStorage(int(sys.argv[2]))
        print('Initialized')
else:
    print('Invalid Input, try again')
