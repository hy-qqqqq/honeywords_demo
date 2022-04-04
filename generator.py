import random
import string
import logging
import hashlib

logger = logging.getLogger(__name__)
rockyou = []

def sweetwords_print(pwd_list):
    """print the generated passwords"""

    print('Generated passwords:')
    for idx, pwd in enumerate(pwd_list):
        print('{}\t{}'.format(idx, pwd))

def sha256_all(pwd_list):
    """apply sha256

    :param pwd_list: passwords to hash.
    :returns: sweetwords, salt
    """

    sweetwords = []
    # generate salt for the user
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    for pwd in pwd_list:
        line = str(pwd + salt).encode('utf-8')
        result = hashlib.sha256(line).hexdigest()
        sweetwords.append(result)
    return sweetwords, salt

def chaff_pwd_model(pwd: str, k=20):
    """chaffing with password model gen

    :param pwd: real password. (does not involved in the generation)
    :param k: generate amount, default is 20.
    :returns: pwd_list, index j
    """
    pwd_list = [pwd]
    while len(pwd_list) < k:
        word = random.choice(rockyou)
        length = len(word)
        # tough nut probability
        if random.random() < 0.08:
            new_word = ''.join(random.choices(string.ascii_letters + string.punctuation, k=random.randint(20, 25)))
        else:
            new_word = word[0]
            for c in range(1, length):
                method = random.choices([1, 2, 3], weights=[0.1, 0.4, 0.5])[0]
                match method:
                    case 1:
                        word = random.choice(rockyou)
                        while len(word) != length:
                            word = random.choice(rockyou)
                        new_word += word[c]
                    case 2:
                        word = random.choice(rockyou)
                        while (len(word) != length) or (word[c-1] != new_word[c-1]):
                            word = random.choice(rockyou)
                        new_word += word[c]
                    case 3:
                        new_word += word[c]
                    
        pwd_list.append(new_word)

    # shuffle
    random.shuffle(pwd_list)
    j = pwd_list.index(pwd)

    return pwd_list, j

def chaff_tweak_tail(pwd: str, k=20, t=3):
    """chaffing with tail tweaking gen

    :param pwd: real password.
    :param k: tweak amount, default is 20.
    :param t: tweak position, default is 3.
    :returns: pwd_list, index j
    """

    head = pwd[:-t]
    tail_list = [pwd[-t:]]
    
    # digits are replaced by digits, letters by letters, and special characters by special characters.
    form = ''
    for c in pwd[-t:]:
        if c in string.ascii_letters: form += 'l'
        elif c in string.digits: form += 'd'
        else: form += 's'
    # generate random tail
    while len(tail_list) < k:
        tail = ''
        for c in form:
            if c == 'l': tail += random.choice(string.ascii_letters)
            elif c == 'd': tail += random.choice(string.digits)
            else: tail += random.choice(string.punctuation)

        if tail in tail_list:
            continue
        tail_list.append(tail)
    
    # prepend head
    chaff_list = [head + tail for tail in tail_list]
    # shuffle
    random.shuffle(chaff_list)
    j = chaff_list.index(pwd)

    return chaff_list, j

def chaff_tweak_digit(pwd: str, k=20, t=3):
    """chaffing with tweaking digit gen

    :param pwd: real password.
    :param k: tweak amount, default is 20.
    :param t: tweak position, default is 3.
    :returns: pwd_list, index j
    """

    head = pwd[:-t]
    tail_list = [pwd[-t:]]
    
    # generate random tail
    while len(tail_list) < k:
        tail = ''.join(random.choices(string.digits, k=t))
        if tail in tail_list:
            continue
        tail_list.append(tail)
    
    # prepend head
    chaff_list = [head + tail for tail in tail_list]
    # shuffle
    random.shuffle(chaff_list)
    j = chaff_list.index(pwd)

    return chaff_list, j

def hybrid_gen(pwd: str, a=10, b=10, t=3, tweak='tail'):
    """hybrid gen

    :param pwd: real password.
    :param a: password model generate amount, default is 10.
    :param b: tweak amount, default is 10.
    :param t: tweak position, default is 3.
    :param tweak: tweaking method, 'digit' or 'tail'.
    :returns: pwd_list, index j
    """

    # apply password model first
    pwd_list, j = chaff_pwd_model(pwd, k=a)
    # apply tweaking method
    chaff_list = []
    if tweak == 'digit':
        for p in pwd_list:
            chaffs, tmp = chaff_tweak_digit(p, k=b, t=t)
            chaff_list.extend(chaffs)
    elif tweak == 'tail':
        for p in pwd_list:
            chaffs, tmp = chaff_tweak_tail(p, k=b, t=t)
            chaff_list.extend(chaffs)
    else:
        logger.warning('Parameter "tweak", wrong value.')
        exit(1)
    
    # shuffle
    random.shuffle(chaff_list)
    j = chaff_list.index(pwd) 
  
    return chaff_list, j

def legacy_UI(pwd='', t=3, chaff='digit', hybrid=False):
    """legacy-UI method

    :param pwd: password, need to specify when using modified-UI.
    :param t: tweak position, default is 3.
    :param chaff: chaffing method, 'digit', 'tail', or 'model'.
    :param hybrid: do hybrid generation if set True.
    :returns: sweetwords, salt, index j.
    """
    if pwd == '':
        pwd = input('Enter a password: ')
        if len(pwd) < 8:
            logger.warn('Password length should at least larger than 8.')
            exit(1)
    
    # hybrid generation if set
    if hybrid:
        pwd_list, j = hybrid_gen(pwd, tweak=chaff)
    # basic chaffing, choose a chaffing method
    else:
        if chaff == 'digit':
            pwd_list, j = chaff_tweak_digit(pwd, t=t)
        elif chaff == 'tail':
            pwd_list, j = chaff_tweak_tail(pwd, t=t)
        elif chaff == 'model':
            pwd_list, j = chaff_pwd_model(pwd)
        else:
            logger.warning('Parameter "chaff", wrong value.')
            exit(1)

    # comment this line to stop stdout the generated passwords
    sweetwords_print(pwd_list)
    # hash
    sweetwords, salt = sha256_all(pwd_list)
    return sweetwords, salt, j

def modified_UI(t=3, chaff='digit', hybrid=False):
    """modified-UI method

    :param t: tweak position, default is 3.
    :param chaff: chaffing method, 'digit', 'tail', or 'model'.
    :param hybrid: do hybrid generation if set True.
    :returns: sweetwords, salt, index j.
    """
    pwd = input('Propose a password: ')
    if len(pwd) < 8:
        logger.warn('Password length should at least larger than 8.')
        exit(1)

    # generate a salt to append to the pwd
    salt = ''.join(random.choices(string.digits, k=t))
    print('Append "{}" to make your new password.'.format(salt))
    newpwd = input('Enter your new password: ')

    if newpwd != (pwd + salt):
        logger.warning('Wrong password + salt in modified-UI.')
        exit(1)
    
    # continue the legacy-UI method
    return legacy_UI(pwd=newpwd, t=t, chaff=chaff, hybrid=hybrid)

def load_rockyou():
    """load rockyou file"""

    logger.warning('Loading rockyou file... This may take a while.')
    global rockyou
    with open('rockyou2000000.txt', 'r', encoding='utf-8', errors='ignore') as f:
        rockyou = f.read().splitlines()
