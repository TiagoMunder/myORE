#!/usr/bin/python

import MySQLdb


def connection():
    # Open database connection
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()

    return data


def TABLE():
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    # Drop table if it already exist using execute() method.



    cursor.execute("DROP TABLE IF EXISTS ORESERVER")

    # Create table as per requirement
    sql = """CREATE TABLE ORESERVER (                              
               ID INT NOT NULL AUTO_INCREMENT,
               ID_M INT NOT NULL,
               KEY_R TEXT NOT NULL,
               NONCE VARCHAR(300) NOT NULL,
               ind INT,
               PRIMARY KEY (ID),
               CONSTRAINT KEY_MASTER FOREIGN KEY (ID_M) REFERENCES MASTER(ID) 
               ON UPDATE CASCADE ON DELETE CASCADE
               )"""
    cursor.execute(sql)


def MASTERTABLE():
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    # Drop table if it already exist using execute() method.
    cursor.execute("ALTER TABLE ORESERVER DROP FOREIGN KEY KEY_MASTER")
    cursor.execute("DROP TABLE IF EXISTS MASTER")
    # Create table as per requirement
    sql = """CREATE TABLE MASTER (                              
               ID INT NOT NULL AUTO_INCREMENT,                 
               AGE INT NOT NULL,
               PRIMARY KEY (ID)
               )"""
    cursor.execute(sql)
    cursor.execute("""ALTER TABLE ORESERVER ADD  CONSTRAINT KEY_MASTER FOREIGN KEY (ID_M) REFERENCES MASTER(ID) 
                   ON UPDATE CASCADE ON DELETE CASCADE""")


def InsertMaster(age):
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sql = """INSERT INTO MASTER(
            AGE
            )
            VALUES ('%d')""" % age

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()

    except(MySQLdb.Error, MySQLdb.Warning) as e:
        # Rollback in case there is any error
        print(e)
        db.rollback()


def Insert(list, nonce, index1, key):
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sql = """INSERT INTO ORESERVER(
            ID_M,
            KEY_R,
            NONCE,
            ind    
            )
            VALUES ('%d','%s','%s','%d')""" % \
          (key, list, nonce, index1)

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        # Rollback in case there is any error
        print(e)
        db.rollback()


def delete(id):
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    # Prepare SQL query to DELETE required records
    sql = "DELETE FROM ORE WHERE ID = '%d'" % id
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()


def deleteX(id_m):
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    # Prepare SQL query to DELETE required records
    sql = "DELETE FROM MASTER WHERE ID = '%d'" % id_m
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()


def CTR():
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    sql = "SELECT * FROM ORESERVER"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        return results
    except:
        print("Error: unable to fecth data")


def CTRORDER():
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    sql = "SELECT * FROM ORESERVER ORDER BY ind"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        return results
    except:
        print("Error: unable to fecth data")


def Update(id, indnew):
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sql = "UPDATE ORESERVER SET ind = '%d' WHERE ID = '%d'" % \
          (indnew, id)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        print('error updating')
        db.rollback()


def CTRORDERMORE(indnew):
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    sql = "SELECT * FROM ORESERVER WHERE ind >= '%d' ORDER BY ind" % indnew
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        return results
    except:
        print("Error: unable to fecth data")


def getRangeID(lower, upper):
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    sql = "SELECT ID_M FROM ORESERVER WHERE ind >= '%d' AND ind <= '%d' ORDER BY ind" % \
          (lower, upper)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        return results
    except:
        print("Error: unable to fecth data")


def getIDByPOS(pos):
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="oreserver")
    cursor = db.cursor()
    sql = "SELECT ID FROM MASTER WHERE AGE = '%d'" % pos
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        return results
    except:
        print("Error: unable to fecth data")

