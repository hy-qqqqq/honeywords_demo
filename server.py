import generator as gen
import honeychecker as hc
import logging
import json
import hashlib

logger = logging.getLogger(__name__)
shadow = {}

def chpwd(uname: str, i: int):
    """change password or set a new password

    :param uname: username.
    :param i: user index.
    :returns: none.
    """

    method = input('Select an UI, (1) legacy-UI (2) modified-UI (3) quit : ')
    # select method
    match method:
        case '1':
            sweetwords, salt, j = gen.legacy_UI(chaff='tail', hybrid=True)
        case '2':
            sweetwords, salt, j = gen.modified_UI()
        case '3':
            return
        case _:
            logger.warning('Please input 1, 2 or 3')
            chpwd(uname, i)
    # store values to shadow file
    shadow[uname] = {'uid': i, 'salt': salt, 'sweetwords': sweetwords}
    # store values to honeychecker with command: set
    hc.table_set(i, j)

def uname_exist(uname: str):
    """check existence of username

    :param uname: username.
    :returns: -1 if not existed, index i if existed.
    """

    # load data
    load_shadow()

    if uname not in shadow.keys():
        return -1
    else:
        return shadow[uname]['uid']

def match_pwd(uname: str, pwd: str):
    """determine the correctness of input password

    :param uname: username.
    :param pwd: password.
    :returns: -1 if not existed, index j if existed.
    """

    # load data
    load_shadow()
    # matching
    line = str(pwd + shadow[uname]['salt']).encode('utf-8')
    result = hashlib.sha256(line).hexdigest()
    for idx, sweetword in enumerate(shadow[uname]['sweetwords']):
        if result == sweetword:
            return idx
    return -1

def login():
    """login server"""

    # input username
    uname = input('Enter your username: ')
    # check uname existence (index i >= 1)
    i = uname_exist(uname)
    if i < 0:
        logger.warning('Username does not exist.')
        return
    # input password
    passwd = input('Enter your password: ')
    # determine the index j
    j = match_pwd(uname, passwd)
    # check values from honeychecker with command: check
    result = hc.table_check(i, j)
    match result:
        case 'honey':
            print('Wrong password.')
            logger.error('Honeywords detected.')
            return
        case 'sugar':
            logger.info('Login successfully.')
            return
        case _:
            logger.warning('Wrong password.')

    return

def register():
    """register new account, only be used by legitimate users"""

    # input username
    uname = input('Enter a username: ')
    i = uname_exist(uname)
    # check uname existence
    if i >= 0:
        logger.warning('Username has already existed.')
        return
    # gen password
    i = len(shadow)
    chpwd(uname, i)
    # update file
    dump_shadow()

def quit():
    """quit"""
    logger.info('Quit.')

    # dump the data
    dump_shadow()
    hc.dump_table()
    # exit
    exit(0)

def main():
    """main"""
    while True:
        action = input('Select an action, (1) login (2) register (3) quit : ')
        match action:
            case '1':
                login()
            case '2':
                register()
            case '3':
                quit()
            case _:
                logger.warning('Please input 1 or 2 or 3.')

def load_shadow():
    global shadow
    try:
        with open('shadow.json', 'r', encoding='utf-8') as f:
            shadow = json.load(f)
    except ValueError:
        shadow = {}

    logger.info('Server load the stored shadow.')

def dump_shadow():
    with open('shadow.json', 'w', encoding='utf-8') as f:
        json.dump(shadow, f, ensure_ascii=False, indent=4)

    logger.info('Server dump shadow.')

if __name__ == '__main__':
    # set up logger (modify 'level' argument to stop verbosing)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    logger.info("Verbose output.")

    # load data
    load_shadow()
    hc.load_table()
    gen.load_rockyou()
    # main
    main()