import mysql.connector
import datetime

import db

# todo: add dict cursor and convert endpoints

mydb = mysql.connector.connect(
  host="localhost",
  user="python",
  password="***",
  database="wellness_db"
)

""" this connects to the db that does messaging. i think i put this in like this to be global to the main dashboard"""
dash_db = mysql.connector.connect(
  host="localhost",
  user="python",
  password="***",
  database="dashboard"
)


mycursor = mydb.cursor()
dictCursor = mydb.cursor(dictionary=True)
db_cursor = dash_db.cursor()

def fetchAssoc(sql):
    dictCursor.execute(sql)
    return dictCursor.fetchall()

def run_query(sql):
    mycursor.execute(sql)
    return mycursor.fetchall()

def get_messages():
    sql = "select * from notifications"
    db_cursor.execute(sql)
    return db_cursor.fetchall()

def insert_sql(sql):
    mycursor.execute(sql)
    mydb.commit()

def enter_activity(form):
  activity = form['type']
  date = form['date']
  time = form['time']
  date_time = date + " " + time
  duration = form['duration']
  notes = form['notes']
  sql = "Insert into activities(`datetime`, `activity`, `notes`, `duration`) Values('{}', '{}', '{}', '{}')".format(date_time, activity, notes, duration)
  mycursor.execute(sql)
  mydb.commit()
  return sql

#todo: also format time of day
def get_activities():
    acts = run_query("select * from activities where datetime like '%2024%' order by datetime DESC")
    acts_output = []
    for act in acts:
        act_item = []
        for act_index in act:
            act_item.append(act_index)
        date_str = act[1]
        date_parts = date_str.split(" ")
        print(date_parts)
        date = date_parts[0]
        if len(date_parts) > 1:
            time = date_parts[1]
        else:
            time = "?"
        #print(date)
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        date_formatted = date_obj.strftime('%a %b %d')
        #print(date_formatted)
        act_item[1] = date_formatted
        act_item.append(time)
        acts_output.append(act_item)

    return acts_output

def get_entry_days():
  sql = "select entered from journal_entries group by entered order by entered desc limit 6"
  res = db.run_query(sql)
  dates = {}
  for date in res:
    date_link = date[0].strftime('%Y-%m-%d')
    date_formatted = date[0].strftime('%a %b %d')
    #print(date_formatted)
    #weekday = datetime.datetime.date.weekday()
    #print(weekday)
    dates[date_link] = date_formatted
  return dates

#get_entry_days()


def get_all_entries():
    sql = "select entered from journal_entries"
    res = db.run_query(sql)
    dates = {}
    for date in res:
        date_link = date[0].strftime('%Y-%m-%d')
        date_formatted = date[0].strftime('%a %b %d')
        # print(date_formatted)
        # weekday = datetime.datetime.date.weekday()
        # print(weekday)
        dates[date_link] = date_formatted
    return dates


def get_entries(date):
    sql = "select * from journal_entries where entered = '{}'".format(date)
    #print(sql)
    return db.run_query(sql)


def assemble_entry_dict(entries):
  entry_dict = {"Journal":[],"Gratitude":[],"Achievements":[],"Intentions":[],"Vision":[]}
  for entry in entries:
    entry_type = entry[1]
    contents = entry[2]
    entry_dict[entry_type].append(contents)
  return entry_dict


def check_and_run_journal_insert(field, date, type):
    insert_sql = "INSERT INTO `journal_entries` (`type`, `entry`, `entered`, `last_updated`) VALUES " \
             "('{}', '{}', " \
             "'{}', '0000-00-00 00:00:00.000000');"
    if len(field) > 0:
        entry = field.replace("'", "''")
        sql = insert_sql.format(type, entry, date)
        run_query(sql)
        mydb.commit()




