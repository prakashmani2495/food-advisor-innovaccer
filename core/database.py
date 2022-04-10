from sqlalchemy import create_engine
from sqlalchemy.sql import text
from core.settings import DATABASE_URL, DB_HOST, DB_USER, DB_PSWD


def dict_to_str(dictionary: dict, seperator: str):
    lists = list()
    for k, v in dictionary.items():
        if str(v).isdigit():
            lists.append(" {} = {} ".format(k, int(v)))
        else:
            lists.append(" {} = '{}' ".format(k, str(v).replace("'", "\\'")))
    if seperator:
        return " %s " % seperator.join(lists)
    else:
        return " ".join(lists)


async def db_execute(database: str, query: str, out: str = None):
    """ MySql database connection arguments with autocommit transaction """
    try:
        db = create_engine(DATABASE_URL + database)
        conn = db.connect()
        res = conn.execute(text(query).execution_options(autocommit=True))
        conn.invalidate()
        db.dispose()
        if out == 'list':
            try:
                return [x for x in res]
            except Exception:
                return None
        elif out == 'dict':
            try:
                return res.mappings().all()
            except Exception:
                return None
        elif out == 'false':
            return True
        else:
            try:
                return [x for x in res]
            except Exception:
                return None
    except Exception as e:
        print(e)
        return None

async def db_select(database: str, table: str, column: str = '*', 
                        condition: dict = None, operator: str = None, order: str = None, out: str = None):
    """ Select the records from database with flexible conditions """
    sql = list()
    sql.append("SELECT %s " % column)
    sql.append("FROM %s " % table)
    if operator is not None and condition is not None:
        sql.append("WHERE")
        sql.append(dict_to_str(condition, operator))
        if order is not None:
            sql.append("ORDER BY %s" % order)
        sql.append(" ;")
    elif condition is not None and operator is None:
        sql.append("WHERE")
        sql.append(dict_to_str(condition, operator))
        if order is not None:
            sql.append("ORDER BY %s" % order)
        sql.append(" ;")
    else:
        if order is not None:
            sql.append("ORDER BY %s" % order)
        sql.append(" ;")
    query = "".join(sql)
    return await db_execute(database, query, out)


async def db_insert(database: str, table: str, values: dict, out: str = None):
    """ Insert rows into objects table given the key-value pairs in kwargs """
    key = ["%s" % k for k in values]
    value = ["'%s'" % v for v in values.values()]
    sql = list()
    sql.append("INSERT INTO %s (" % table)
    sql.append(", ".join(key))
    sql.append(") VALUES (")
    sql.append(", ".join(value))
    sql.append(");")
    query = "".join(sql)
    return await db_execute(database, query, out)


async def db_update(database: str, table: str, values: dict, condition: dict = None, operator: str = None, out: str = None):
    """ Update rows into objects table given the key-value pairs in kwargs """
    sql = list()
    sql.append("UPDATE %s SET " % table)
    sql.append(dict_to_str(values, ','))
    if condition is not None and operator is not None:
        sql.append(" WHERE")
        sql.append(dict_to_str(condition, operator))
        sql.append(";")
    elif condition is not None and operator is None:
        sql.append(" WHERE")
        sql.append(dict_to_str(condition, operator))
        sql.append(";")
    else:
        sql.append(";")
    query = "".join(sql)
    return await db_execute(database, query, out)


def db_execute_seq(database: str, query: str, out: str = None):
    """ MySql database connection arguments with autocommit transaction """
    try:
        conn: object = create_engine(DATABASE_URL + database).connect()
        res: object = conn.execute(text(query).execution_options(autocommit=True))
        conn.close()
        if out == 'list':
            try:
                return [x for x in res]
            except Exception:
                return None
        elif out == 'dict':
            try:
                return res.mappings().all()
            except Exception:
                return None
        elif out == 'false':
            return True
        else:
            try:
                return [x for x in res]
            except Exception:
                return None
    except Exception as e:
        print(e)
        return None