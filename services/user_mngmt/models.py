from core.database import db_execute, db_select, db_execute_seq
from core.settings import DATABASE
import os, json

ERROR_DICT: dict = {"status": "error","desc": "Something went wrong, Please contact System Administrator."}


async def create_new_user(name: str, email: str, password: str):
    res: list = await db_execute(database=DATABASE, query="call SP_CreateNewUser('{}', '{}', '{}')".format(name, email, password),
                                 out='dict')
    if res:
        return res[0]
    else:
        return ERROR_DICT


async def authenticate_user(email: str):
    res: list = await db_execute(database=DATABASE, query="call SP_CheckUserAccessByUserID('{}')".format(email),
                                 out='dict')
    if res:
        return res[0]
    else:
        return ERROR_DICT


async def create_user_session(uuid: str, user_id: int, access_jti: str, refresh_jti: str):
    sql: str = "call SP_CreateUserSession('{}', {}, '{}', '{}')".format(uuid, user_id, access_jti, refresh_jti)
    await db_execute(database=DATABASE, query=sql, out=False)


async def update_user_session(user_id: str, access_jti: str, new_access_jti: str, new_refresh_jti: str):
    sql: str = "call SP_UpdateUserSession('{}', '{}', '{}', '{}')".format(user_id, access_jti, new_access_jti, new_refresh_jti)
    await db_execute(database=DATABASE, query=sql, out=False)


async def revoke_user_session(user_id: str, access_jti: str):
    sql: str = "call SP_RevokeUserAccess('{}', '{}')".format(user_id, access_jti)
    res = await db_execute(database=DATABASE, query=sql, out='dict')
    return res


def get_revoked_tokens():
    sql: str = "call SP_GetDenyTokenList()"
    tokens: list = db_execute_seq(database=DATABASE, query=sql, out='list')
    l_token = []
    for token in tokens:
        l_token.append(token[0])
    return l_token


async def check_user_details(user_id: str):
    sql: str ="""SELECT FullName, Gender, MedicalCondition, Height, Weight, BMI, TargetBMI, TargetDays, Age, DATE(DietStarts) AS DietStarts, DATE(DietEnds) AS  DietEnds
                FROM UserDetails ud 
                INNER JOIN UserAccess ua 
                ON ud.UserAccess_ID = ua.UserAccess_ID  
                WHERE ua.Email_ID = '{}'""".format(user_id)
    res = await db_execute(database=DATABASE, query=sql, out='dict')
    if res:
        return res[0]
    else:
        return None


async def today_diet_plan(user_id: str):
    sql: str = """select DietTime, DietFood from DietPlan dp
                inner join UserAccess ua 
                on ua.UserAccess_ID = dp.UserAccess_ID 
                where dp.DietDate = DATE(DATE_ADD(NOW(), INTERVAL 1 DAy))
                and ua.Email_ID = '{}'
                ORDER BY DietOrder """.format(user_id)
    res = await db_execute(database=DATABASE, query=sql, out='dict')
    if res:
        return res
    else:
        return None


async def update_user_details(user_id: str, age: int, gender: str, height: int, weight: int, activity: list, medical: list):
    p_medical: str = ",".join(medical)
    p_activity: str = ",".join(activity)
    p_bmi = weight/((height*0.01)*(height*0.01))
    print(weight)
    print(height)
    print(p_bmi)
    sql: str = 'call SP_UpdateUserDetails("{}", {}, "{}", {}, {}, "{}", "{}", {});'.format(user_id, age, gender, height, weight, p_activity, p_medical, p_bmi)
    res = await db_execute(database=DATABASE, query=sql, out='dict')
    if res:
        return {"status": "success","location": "/users/dashboard/"}
    else:
        return ERROR_DICT