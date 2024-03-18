from flask import Flask, render_template, request, session
import db, sys
from datetime import datetime


#todo: see all journal entries (page)
#todo: move to sqlite with slqalchemy and put online!  add logins.
#todo: enter multiple activities (working through modal)
#todo: multiple users (needs account setup, email, pw reset)
#todo: beta testing.
#todo: budget this and allocate hours towards it.
#todo: write some logic to check activities for all groups, check journal entries for completion, encourage, etc.
#todo: set up goal setting / editing in account creation, suggested goals, etc. (meditation once a day, etc)
#todo: table for activity intentions by user / cat.
# day and date in journal entry links, only show last few, but have full list. 

app = Flask(__name__)
app.secret_key = 'YXD$$)$%%DFGXXYJ22'

#todo: create filter / search links
# todo: put on python anywhere and test on phone.
# todo: (future) - make a phone app with an individual database (how to handle privacy) - just use global db.

@app.route('/session_test')
def session_test():
    session['data'] = "test"
    return render_template('index.html', session=session)


# todo: get all common content for header and sidebars in one shot
# todo: turn journal entry page (or sidebar) into ajax links to put in each one individually.
# toto: enable date field
@app.route('/')
def index():
    session.pop('data', default=None)
    entries = db.get_entry_days()
    journals = db.get_all_entries()
    date = datetime.today().strftime('%m-%d-%Y')
    messages = db.get_messages()
    return render_template('index.html', days=entries, date=date, messages=messages, journals=journals)

@app.route('/journal_ajax', methods=['POST'])
def journal_modal():
    form = request.form
    print(form)
    type = form['type']
    notes = form['notes']
    date = datetime.today().strftime('%Y-%m-%d')
    db.check_and_run_journal_insert(notes, date, type)
    return "entry made!"


#todo: ok this is good! just clean it up and put in sucess in div.
#todo: make drop down smaller.
# todo: move activities to modal / footer include / sidebar links
# todo: rename this to activity_ajax or something
@app.route('/ajax', methods=['POST'])
def ajax_endpoint():

    try:
        form = request.form
        print(form)
        activity = form['activity']
        date = form['date']
        time = form['time']
        date_time = date + " " + time
        duration = form['duration']
        notes = form['notes']
        print("{}, {}, {}, {}".format(activity, date_time, duration, notes))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ERROR on line {}: ".format(exc_tb.tb_lineno) + str(e))

    sql = "Insert into activities(`datetime`, `activity`, `notes`, `duration`) Values('{}', '{}', '{}', '{}')".format(
        date_time, activity, notes, duration)
    db.insert_sql(sql)

    return "record inserted! :)"

@app.route('/all_entries')


# todo: show date of entry at top of form
# todo: edit
# todo: finish ajax modal for all entry types.
# todo: update journal page with new entry upon insert
@app.route('/get_entries', methods=['GET'])
def get_entries():
    journals = db.get_all_entries()
    days = db.get_entry_days()
    date = request.args.get('date', 0)
    if date == 0:
        date = datetime.today().strftime('%Y-%m-%d')
    entries = db.assemble_entry_dict(db.get_entries(date))
    return render_template('entries.html', entries=entries, days=days, date=date, journals=journals)

#todo: right now this is set up to enter one at a time - should handle multiple
# todo: make a page to pull this stuff out so i can look at it.
@app.route('/activity', methods=['POST'])
def enter_activity(): 
    db.enter_activity(request.form)
    acted = db.get_activities()
    msg = db.get_messages()
    days = db.get_entry_days()
    #activity = request.form['type']
    #date = request.form['date']
    #duration = request.form['duration']
    #notes = request.form['notes']
    #content = [activity, date, duration, notes]
    #content = request.form
    return render_template('activity_log.html', acts=acted, messages=msg, days=days)

# todo: order by date desc
# todo: cleanup table
# todo: show time
# todo: put in goals for activities per week and show if / how far to goal being attained.
@app.route('/activity_log')
def get_activities():
    acted = db.get_activities()
    msg = db.get_messages()
    days = db.get_entry_days()
    return render_template('activity_log.html', acts=acted, messages=msg, days=days)


#todo: add - did you meditate today? did you work out today? did you plant seeds today? (how much, which kind, etc.)
#todo: add ability to process a previous date from form (or edit entries)
#todo: show a different scren or go right to today (get entries)
# todo: pack all info related to an entry into one clean dict
# todo: show today's entry
# todo: use activity log template for full right side usage
# todo: add ability to add a previous entry (play with this)
# todo: add ability to edit / add to today or previous entry (play with it)
@app.route('/process_form', methods=['POST'])
def process_form():
    gratitude = request.form['Gratitude']
    vision = request.form['Vision']
    journal = request.form['Journal']
    intentions = request.form['Intentions']
    ach = request.form['Achievements']
    date = datetime.today().strftime('%Y-%m-%d')
    days = db.get_entry_days()
    page_content = {"Gratitude":gratitude, "Vision":vision, "Journal":journal, "Intentions":intentions, "Achievements":ach}
    for key in page_content:
        db.check_and_run_journal_insert(page_content[key], date, key)
    return render_template('index.html', days=days)


#todo: show and edit entries
