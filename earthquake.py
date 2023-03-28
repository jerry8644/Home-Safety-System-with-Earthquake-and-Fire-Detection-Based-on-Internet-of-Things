import mysql.connector

try:
    cnx=mysql.connector.connect(user='iot1',password='iot1',host='34.81.255.169',database='test1')
    #cursor.execute("SHOW TABLES")
    # ~ result=cursor.fetchall()
    # ~ print(result)
    #cursor.execute("INSERT INTO Earthquake (detect) Values(%d)"%(333))
    while True:
        cursor=cnx.cursor()
        cursor.execute("SELECT detect FROM Earthquake")
        result=cursor.fetchone()
        result=list(map(int,result))
        if result!=[0]:
            print(result)##### pir 
        else:
            print("no earthquake",result)
        cnx.commit()
finally:
    cnx.close()
