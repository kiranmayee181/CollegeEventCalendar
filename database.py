from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session,Session
from sqlalchemy import select,and_,update,delete
from datetime import date


SQLALCHEMY_DATABASE_URI = "sqlite:///./event.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
ref = {'cse':0,'ece':0,'it':0,'eee':0,'mech': 0,'civil':0,'cs':0}

class Event(Base):
    __tablename__ = 'events'
    eid = Column(Integer, autoincrement=True, primary_key=True)
    ename = Column(String(512),nullable=False)
    edesc = Column(String(512),nullable=False)
    edate= Column(String(512),nullable=False)
    edept = Column(String(512),nullable=False)
    evenue = Column(String(512),nullable=False)
    eposter= Column(String(512),nullable=False)
    oname= Column(String(512),nullable=False)
    odept= Column(String(512),nullable=False)
    verified = Column(Integer,default=0)
    ophno = Column(Integer,default=9957685478)

class Organizers(Base):
    __tablename__ = "Organizers"
    ouname = Column(String(512),nullable=False,primary_key=True)
    opwd = Column(String(512),nullable=False)

def add_event(ename,edesc,edate,edept,evenue,eposter,oname,odept,oph):
    dbsession = Session(engine)
    a = Event(ename=ename,edesc=edesc,edate=edate,edept=edept,evenue=evenue,eposter=eposter,oname=oname,odept=odept,ophno=oph)
    b = date.today()
    if strToDate(a.edate) < b:
        a.verified = 1
    dbsession.add(a)
    dbsession.commit()
    dbsession.close()

def strToDate(st):
    print(st)
    x = st.split('-')
    return date(int(x[0]),int(x[1]),int(x[2]))

def showEventC():
    b = date.today()
    c = select(Event).filter(Event.edept == 'Any').filter(Event.verified == 1)
    d = select(Event).filter(strToDate(Event.edate > b))


def showEvents(dept):
    b = date.today()
    dbsession = Session(engine)
    c = select(Event).filter(Event.edept == dept).filter(Event.verified == 1)
    upC,past = [],[]
    ref2 =  getN()
    for i in dbsession.scalars(c):
        print("i",i)
        if strToDate(str(i.edate)) > b:
            upC.append(i.__dict__)
        else:
            past.append(i.__dict__)
    dbsession.close()
    # return None
    return upC,past,ref2

def showEvent(eid):
    dbsession = Session(engine)
    c = select(Event).filter(Event.eid == eid)
    d = dbsession.scalars(c)
    for i in d:
        k =  i.__dict__
    dbsession.close()
    return k
    
def getN():
    dbsession = Session(engine)
    c = select(Event).filter(Event.verified == 1)
    b = date.today()
    ref2 = {'cse':0,'ece':0,'it':0,'eee':0,'mech': 0,'civil':0,'cs':0}
    for i in dbsession.scalars(c):
        print(i.__dict__)
        if strToDate(str(i.edate)) > b:
            if(str(i.edept))!='Any':
                ref2[str(i.edept)]+=1
    dbsession.close()
    return ref2

def verify(eid):
    dbsession = Session(engine)
    v = update(Event).values({'verified':1}).where(Event.eid == eid)
    dbsession.execute(v)
    dbsession.commit()
    dbsession.close()

def remov(eid):
    dbsession = Session(engine)
    x = delete(Event).where(Event.eid == eid)
    dbsession.execute(x)
    dbsession.commit()
    dbsession.close()

def verEvents():
    dbsession = Session(engine)
    c = select(Event).filter(Event.verified == 1)
    x = []
    for i in dbsession.scalars(c):
        x.append(i.__dict__)
    dbsession.close()
    return x

def tobeverEvents():
    dbsession = Session(engine)
    b = date.today()
    c = select(Event).filter(Event.edate > b).filter(Event.verified == 0)
    x = []
    for i in dbsession.scalars(c):
        x.append(i.__dict__)
    dbsession.close()
    return x

def verAdmin(uname,pwd):
    return uname=='Admin' and pwd=='Admin'

def verOrg(uname,pwd):
    dbsession = Session(engine)
    c = select(Organizers).filter(Organizers.ouname == uname)
    t = None
    for i in dbsession.scalars(c):
        t = i.__dict__
        break
    if t == None:
        return False
    return t['opwd']==pwd