from core.database import db_execute, db_select, db_execute_seq
from core.settings import DATABASE


ERROR_DICT: dict = {"status": "error","desc": "Something went wrong, Please contact System Administrator."}

async def get_user_details(email_id: str):
    sql: str = """SELECT Height, Weight, BMI, TargetBMI, TargetDays, Age, DATE(DietStarts) AS DietStarts, DATE(DietEnds) AS  DietEnds
                FROM UserDetails ud 
                INNER JOIN UserAccess ua 
                ON ud.UserAccess_ID = ua.UserAccess_ID  
                WHERE ua.Email_ID = '{}'""".format(email_id)

    res = await db_execute(database=DATABASE, query=sql, out='dict')
    if res:
        return res[0]
    else:
        return None