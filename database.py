import pymysql as pm


def loginCheck(user, passw):
    con = pm.connect(host='localhost', user='root', password='admin', database='healthcare')

    cursor = con.cursor()

    query = "select * from userinfo where user = '%s' and password = '%s'" % (user, passw)

    cursor.execute(query)

    if cursor.rowcount == 1:
        status = True
    else:
        status = False
    con.close()
    return status




def signupCheck(user, passw):
    con = pm.connect(host='localhost', user='root', password='admin', database='healthcare')

    cursor = con.cursor()

    query = "insert into userinfo values('%s', '%s')" % (user, passw)

    cursor.execute(query)

    try:
        con.commit()
        status = True
    except:
        con.rollback()
        status = False
    return status

    con.close()
