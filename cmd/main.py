# When finished with entire script, build with 'pyinstaller {file_name}.py'
# When finished with entire script, build with 'pyinstaller main.py'
import json
import os
import sys

c = sys.argv[0]

storage_dir = './.panda/storage.json'
body_dir = './.panda/body.json'

panda_ignore = []

try:
    panda_ignore = open('.pandaignore', "r").read().split('\n')
except:
    # No .pandaignore file
    pass

from python_graphql_client import GraphqlClient

client = GraphqlClient("https://safe-crag-17237.herokuapp.com/graphql")

def loginHttp(username, password):
    query = """
        query ($username: String!, $password: String!) {
            login(input: {
                username: $username,
                password: $password
            })
        } 
    """
    try:
        data = client.execute(query=query, variables={
            "username": username,
            "password": password
        })['data']
    except:
        print("Error Fetching")
        exit()
    return data['login']

def logout():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    reqs = cur_obj['reqs']
    reqs['username'] = None
    reqs['password'] = None
    reqs['key'] = None
    reqs['projectId'] = None
    cur_obj['reqs'] = reqs
    open(storage_dir, "w").write(json.dumps(cur_obj))


def getProjectId():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    reqs = cur_obj['reqs']
    return reqs['projectId']


def write_folder(file_names, name):
    r_storage = open(body_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj[name] = file_names
    open(body_dir, "w").write(json.dumps(cur_obj))


def write_file(s, file_name):
    r_storage = open(body_dir, "r").read()
    cur_obj = json.loads(r_storage)
    cur_obj[file_name] = s
    open(body_dir, "w").write(json.dumps(cur_obj))


def commit(projectId, s, name):
    query = '''
        mutation ($s: String!, $projectId: Float!, $name: String!) {
            commit(
                input: $s,
                projectId: $projectId,
                name: $name
            )
        }
    '''

    try:
        d = client.execute(query=query, variables={
            "projectId": projectId,
            "s": s,
            "name": name
        })
    except:
        print("Error Fetching")
        exit()
    return d['data']['commit']


def login(username, password):
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    reqs = cur_obj['reqs']
    try:
        key = loginHttp(username, password)
        if key == None:
            print("Error. Signup on the website (Insert Link when Done) or Login Error")
            exit()
        reqs['username'] = username
        reqs['password'] = password
        reqs['key'] = key
        cur_obj['reqs'] = reqs
        open(storage_dir, "w").write(json.dumps(cur_obj))
    except:
        pass


def checkLogin():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    if cur_obj['reqs']['key']:
        return True
    else:
        return False


def reset_files():
    cur_obj = {
        'need': ['root']
    }
    open(body_dir, "w").write(json.dumps(cur_obj))


def get_login():
    r_storage = open(storage_dir, "r").read()
    cur_obj = json.loads(r_storage)
    return [cur_obj['reqs']['username'], cur_obj['reqs']['password']]


def stringify():
    return rf'{open(body_dir, "r").read()}'


def initializeDirStorage(projectId):
    if os.path.exists('./.panda/'):
        print('Already Exists')
        try:
            open('./.panda/storage.json', 'a')

        except:
            print('File Already Created')
    else:
        os.mkdir('./.panda/')
        open(storage_dir, 'a')
        open(body_dir, 'a')
        open(storage_dir, "w").write(json.dumps({
            'reqs': {
                'projectId': projectId
            }
        }))
        open(body_dir, "w").write(json.dumps({
            "need": ['root']
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
            try:
                if dir in panda_ignore:
                    pass
                else:
                    write_file(open(dir).read(), i)
            except:
                print("Error")
                exit()
        else:
            dir = './'
            ns = []
            for j in names:
                ns.append(j)
                dir += j
                dir += '/'
            ns.append(i)
            dir += i
            try:
                if dir in panda_ignore:
                    pass
                else:
                    s = os.listdir(dir)
                    write_folder(s, i)
                    open_folder(s, ns, i)
            except:
                print("Error")
                exit()


def pullRequestWriteFolder(full_vals, dir, folder_name):
    files = full_vals[folder_name]
    cur_dir = dir + folder_name + '/'

    if os.path.isdir(cur_dir):
        pass
    else:
        os.mkdir(cur_dir)

    for i in files:
        if i.__contains__('.'):
            try:
                open(cur_dir + i, "a")
            except:
                print("File Already Exists")
            open(cur_dir + i, "w").write(full_vals[i])
        else:
            pullRequestWriteFolder(full_vals, cur_dir, i)


# To Git Clone just pull request it
def handlePullRequest():
    query = """
        query ($projectId: Float!, $name: String!) {
            pullRequest(
                projectId: $projectId,
                name: $name
            )
        }
    """

    print("To Get the Root Commit, click enter")
    name = input('Commit Name: ')

    iid = getProjectId()

    try:
        d = client.execute(query=query, variables={
            'projectId': iid,
            "name": name
        })
    except:
        print("Errors Fetching")
        exit()

    data = d['data']

    try:
        if d['errors'] is not None:
            print("Errors Occured")
            print(d['errors'])
            exit()
    except:
        pass

    j = json.loads(data['pullRequest'])
    # Get the Root
    root = j['root']
    for i in root:
        if i.__contains__('.'):
            try:
                open(i, "a")
            except:
                print('File Already Exists')
            open(i, 'w').write(j[i])
        else:
            pullRequestWriteFolder(full_vals=j, dir='./', folder_name=i)

def checkValidProjectId(projectId):
    query = '''
        query ($id: Int!) {
            findProject(input: {
                id: $id
            }) {
                id
            }
        }
    '''

    try:
        d = client.execute(query=query, variables={
            'id': int(projectId)
        })
    except:
        print("Error Fetching")
        exit()

    try:
        if d['errors'] is not None:
            print('Errors')
            exit()
    except:
        print("No Errors")

    if d['data']['findProject'] is None:
        return False
    else:
        return True

try:
    cmd = sys.argv[1]
except:
    print('Must Have An Argument After Command')
    exit()

if cmd == 'add':
    files = sys.argv[2::]
    if files[0] == '.':
        files_in_dir = os.listdir('./')
        files_without_panda = []
        for i in files_in_dir:
            if i == '.panda' or i in panda_ignore:
                pass
            else:
                files_without_panda.append(i)

        write_folder(files_without_panda, "root")

        for i in files_without_panda:
            if i == '.panda':
                # DO NOTHING
                pass
            elif i.__contains__('.'):
                try:
                    write_file(open(i, "r").read(), i)
                except:
                    pass
            else:
                f = os.listdir(i)
                try:
                    open_folder(f, [i], i)
                except:
                    pass
    else:
        write_folder(file_names=files, name='root')
        for i in files:
            if i.startswith('./'):
                f = os.listdir(i)
                open_folder(f, [i], i)
            else:
                f = os.listdir(i)
                open_folder(f, [i], i)
elif cmd == 'login':
    user = sys.argv[2]
    passw = sys.argv[3]
    login(user, passw)
elif cmd == 'commit':
    com_name = input('Commit Name: ')
    print("Make Sure You Are Logged In and have Added")
    if checkLogin():
        s = stringify()
        if commit(getProjectId(), s, com_name):
            reset_files()
            print("Commit Succeeded")
        else:
            print("Commit Failed, Please Try Again")
    else:
        print('Guess You weren\'t Logged In')
        exit()
elif cmd == 'pull':
    handlePullRequest()
elif cmd == 'get_login':
    get = get_login()
    print('Username: ' + get[0])
    print('Password: ' + get[1])
elif cmd == 'logout':
    logout()
elif cmd == 'reverse':
    reset_files()
elif cmd == 'init':
    try:
        id = sys.argv[2]
    except:
        print('Must Input ProjectID')
        exit()

    if checkValidProjectId(id):
        # Do Nothing
        pass
    else:
        print('Project ID not Valid')
        exit()

    if os.path.isdir('./.panda'):

        if os.path.isfile('./.panda/storage.json'):
            print('Storage.json Created')
        else:
            open('./.panda/storage.json', "a")

            s = json.dumps({
                'reqs': {
                    'projectId': id
                }
            })

            open('./.panda/storage.json', "w").write(s)

            print('Now Initialized')

        if os.path.isfile('./.panda/body.json'):
            print('body.json Created')
        else:
            open('./.panda/body.json', "a")

            s = json.dumps({
                'need': ['root']
            })

            open('./.panda/body.json', "w").write(s)

            print('Now Initialized')
    else:
        initializeDirStorage(int(id))
else:
    print('Valid Command not found')
    print('''
    - add
    - login
    - commit
    - pull
    - clone
    - get_login
    - logout
    - reverse
    - init 
    ''')
