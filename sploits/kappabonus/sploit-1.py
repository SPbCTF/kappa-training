import pymysql.cursors

#DB = "mysql://anonymous:@cloud.spbctf.com:3306/test1"
DB = "kappabonus.spbctf.com"

cnx = pymysql.connect(user='test1', password='vyvokaljrkmhtfrwxdbd',
                              host=DB,
                              database='test1')
cursor = cnx.cursor()
query = "SELECT * FROM lcbc"
cursor.execute(query)
for row in cursor:
    print(row)
cursor.close()
cnx.close()
# mysql.connector.connect