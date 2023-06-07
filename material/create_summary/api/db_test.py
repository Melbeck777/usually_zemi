import sys
sys.path.append("..")
from api.model.model import db, Lab, Team, Schedule, User

from api.__init__ import app
lab_names = ["精密メカトロシステム","制御システム","None"]
team_names = [["構造物センシング","マイクロロボット","自立移動ロボット"],["湿原ロボット","体操"]]


def record_and_select():
    for index, team in enumerate(team_names):
        labs = Lab.getLabId(lab_names[index])
        lab_id = labs[0].id
        check_lab = Team.getLabId(lab_id)
        if len(check_lab) > 0:
            continue
        for team_name in team:
            Team.recordTeam(teamName=team_name,labId=lab_id)
    teams = db.session.query(Team).all()
    for team in teams:
        lab = db.session.query(Lab).get(team.labId)
        print(team.id,lab.name,team.name)

with app.app_context():
    lab = db.session.query(Lab).get(0)
    print("out\n{}, {}".format(lab,type(lab)))