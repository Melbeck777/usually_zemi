import datetime
from api.__init__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Userのテーブル
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    firstName = db.Column(db.String(50), nullable=False)
    secondName = db.Column(db.String(50), nullable=False)
    firstKana = db.Column(db.String(50), nullable=False)
    secondKana = db.Column(db.String(50), nullable=False)
    emailAddress = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    studentNumber = db.Column(db.Integer, nullable=False,unique=True)
    labId = db.Column(db.Integer)
    TeamId = db.Column(db.Integer)
    gradeId = db.Column(db.Integer)
    authorityId = db.Column(db.Integer)
    createdAt = db.Column(db.DATETIME,default=datetime.datetime.now())

    def getUserList():
        user_list = db.session.query(User).all()
        if user_list == None:
            return []
        else:
            return user_list

    def recordUser(user):
        record = User(
            firstName=user['firstName'],
            secondName=user['secondName'],
            firstKana=user['firstKana'],
            secondKana=user['secondKana'],
            emailAddress=user['emailAddress'],
            password=user['password'],
            studentNumber=user['studentNumber'],
            labId=user['labId'],
            teamId=user['teamId'],
            gradeId=user['gradeId'],
            authorityId = user['authorityId'],
            createdAt=user['createdAt']
        )
        db.session.add(record)
        db.session.commit()
        return user

# 学年のテーブル
class Grade(db.Model):
    __tablename__ = "Grade"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(50),nullable=False)

    def getAllGrade():
        grade_list = db.session.query(Grade).all()
        if grade_list == None:
            return []
        else:
            return grade_list

# 研究室のテーブル
class Lab(db.Model):
    __tablename__ = "Lab"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)

    def getAllLab():
        grade_list = db.session.query(Grade).all()
        if grade_list == None:
            return []
        else:
            return grade_list
    def getLabId(labName):
        return db.session.query(Lab).filter(Lab.name==labName).all()

    def recordLab(labName):
        record_lab = Lab(name=labName)
        db.session.add(record_lab)
        db.session.commit()
        return record_lab.id

# 研究班のテーブル
class Team(db.Model):
    __tablename__ = "Team"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    labId = db.Column(db.Integer, nullable=False)
    name=db.Column(db.String(100),nullable=False)

    def recordTeam(teamName,labId):
        record_Team = Team(name=teamName,labId=labId)
        db.session.add(record_Team)
        db.session.commit()
        return record_Team.id
    
    def getTeamId(teamName):
        return db.session.query(Team).filter(Team.name==teamName).all()
    
    def getLabId(labId):
        return db.session.query(Team).filter(Team.labId==labId).all()

# スケジュールを作ったり、メンバの編集をする権限の管理
class Authority(db.Model):
    __tablename__ = "Authority"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)

# いつどこでやるのかを記録する
class Schedule(db.Model):
    __tablename__ = "Schedule"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    createdAt = db.Column(db.DATETIME,default=datetime.datetime.now(),nullable=False)
    labId = db.Column(db.Integer)
    createBy = db.Column(db.Integer,nullable=False) # UserId
    TeamId = db.Column(db.Integer)
    date = db.Column(db.DATETIME)
    Place=db.Column(db.String(100))

# 読みだすタイトル
class Title(db.Model):
    __tablename__ = "Title"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    createdAt = db.Column(db.DATETIME,default=datetime.datetime.now(),nullable=False)
    labId = db.Column(db.Integer)
    createBy = db.Column(db.Integer,nullable=False) # UserId
    TeamId = db.Column(db.Integer)

db.init_app(app)
with app.app_context():
    db.create_all()