#!/usr/bin/python

import MySQLdb



def connection():
   # Open database connection
   db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="ore")

   # prepare a cursor object using cursor() method
   cursor = db.cursor()

   # execute SQL query using execute() method.
   cursor.execute("SELECT VERSION()")

   # Fetch a single row using fetchone() method.
   data = cursor.fetchone()

   return data

def TABLE():
      db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="ore")
      cursor = db.cursor()
      # Drop table if it already exist using execute() method.
      cursor.execute("DROP TABLE IF EXISTS ORE")
      # Create table as per requirement
      sql = """CREATE TABLE ORE (                              
               POS INT NOT NULL,                 
               KEY_L VARCHAR(100) NOT NULL )"""
      cursor.execute(sql)

def Insert(POS,KEY_L):
   db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="ore")
   cursor = db.cursor()
   # Prepare SQL query to INSERT a record into the database.
   sql = """INSERT INTO ORE(POS,
            KEY_L)
            VALUES ('%d', '%s')""" % \
            (POS,KEY_L)
   try:
      # Execute the SQL command
      cursor.execute(sql)
      # Commit your changes in the database
      db.commit()
   except:
      # Rollback in case there is any error
      print("error")
      db.rollback()

def delete(POS):
   db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123123", db="ore")
   cursor = db.cursor()
   # Prepare SQL query to DELETE required records
   sql = "DELETE FROM ORE WHERE POS = '%d'" % POS
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


