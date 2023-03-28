import mysql.connector
# ~ cnx=mysql.connector.connect(user='iot1',password='iot1',host='34.81.255.169',database='test1')
cnx=mysql.connector.connect(user='root',password='iot1',host='35.194.170.131',database='iot')
try:
    cursor=cnx.cursor()
    cursor.execute("SHOW TABLES")
    result=cursor.fetchall()
    print(result)
    
finally:
    cnx.close()
