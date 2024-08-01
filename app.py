import os
from flask import Flask,redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from fileinput import filename
from werkzeug.utils import secure_filename
from datetime import *
from database import add_event,Event,showEvents,showEvent,verEvents,tobeverEvents,verify,remov,verAdmin,verOrg

UPLOAD_FOLDER = r"C:\Users\Sathya Sree\Desktop\Profile\project\M7\mini_project6\static"
current_dir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./event.db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


ref = {'CSE':'Computer Science and Engineering',
       'ECE':'Electrical and Communication Engineering',
       'IT':'Information Technology',
       'EEE':'Electrical and Electronics Engineering',
       'MECH': 'Mechanical Engineering',
       'CIVIL':'Civil Engineering',
       'CS':'Cyber Security'
    }


@app.route('/sec/OrganizersPage',methods=['GET','POST'])
def collectFormData():
    if request.method == 'GET':
        return render_template('eop.html')
    else:
        d = request.form
        name = str(d['ename']).strip()
        desc = str(d['desc']).strip()
        date = str(d['timings']).strip()
        oname = str(d['faculty']).strip()
        odept = str(d['branch']).strip()
        venue = str(d['venue']).strip()
        edept = 'Any' if str(d['ev']) == 'cle' else odept
        oph  = int(d['contact'])
        print(request.files)
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file :
            filename = secure_filename(str(datetime.now())+str(file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        fileloc = filename
        add_event(name,desc,date,edept,venue,fileloc,oname,odept,oph);
        return "<center>" + "<h1>" + "SUCCESS" + "</h1></center>"

@app.route('/participant/home',methods=['GET'])
def ParticipantHome():
    k = showEvents('Any')
    if k == None:
        UpcEvents,PastEvents,ref2 = [],[],[]
    else:
        UpcEvents,PastEvents,ref2 = k
    return render_template('stu_home.html',CollegeEvents=UpcEvents,PastEvents=PastEvents,dc=ref2)

@app.route('/event/<string:dept>')
def ParticipantDept(dept):
    print(dept)
    UpcEvents,PastEvents,ref2 = showEvents(dept)
    return render_template('DeptBase.html',CollegeEvents=UpcEvents,PastEvents=PastEvents,Dept = ref[str(dept).upper()])

@app.route('/organizers/home')
def OrganizerHome():
    UpcEvents,PastEvents,ref2 = showEvents('Any')
    return render_template('org_home.html',CollegeEvents=UpcEvents,PastEvents=PastEvents,dc=ref2)

@app.route('/event/<int:eid>')
def event(eid):
    d = showEvent(eid)
    return render_template('event.html',e=d)

@app.route('/admin')
def admin():
    return render_template('admin.html')



@app.route('/admin/VerifiedEvents')
def VerifiedEvents():
    return render_template('admin1.html',Heading='Verified Events',events=verEvents(),ie=0)

@app.route('/admin/EventsToBeVerified')
def ToBeVerified():
    return render_template('admin1.html',Heading='Events To Be Verified',events=tobeverEvents(),ie=1)

@app.route('/admin/<int:b>/<int:eid>')
def verification(b,eid):
    if b==1:
        verify(eid)
    else:
        remov(eid)
    return redirect('/admin/EventsToBeVerified')

@app.route('/',methods=['POST','GET'])
def index():
        return render_template('l.html')
         

@app.route('/verAd')
def verifyAdmin():
    d = request.args
    n = str(d['email']).strip()
    d = str(d['password']).strip()
    if verAdmin(n,d):
        return redirect('/admin')
    return redirect('/')

@app.route('/verOrg')
def verifyOrg():
    d = request.args
    n = str(d['email']).strip()
    d = str(d['password']).strip()
    if verOrg(n,d):
        return redirect('/organizers/home')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)