import json
import logging

logger = logging.getLogger(__name__)
table_c = {}

def table_set(i: int, j: int):
    """set table_c"""
    logger.info('Honeychecker receives command "set".')

    load_table()
    table_c[str(i)] = j
    dump_table()

    return

def table_check(i: int, j: int):
    """check table_c"""
    logger.info('Honeychecker receives command "check".')

    load_table()
    if j == -1:
        return 'wrong'
    if table_c[str(i)] != j:
        return 'honey'
    else:
        return 'sugar'

def load_table():
    global table_c
    try:
        with open('table_c.json', 'r', encoding='utf-8') as f:
            table_c = json.load(f)
    except ValueError:
        table_c = {}
    
    logger.info('Honeychecker load the stored table_c.')

def dump_table():
    with open('table_c.json', 'w', encoding='utf-8') as f:
        json.dump(table_c, f, ensure_ascii=False, indent=4)

    logger.info('Honeychecker dump table_c.')
