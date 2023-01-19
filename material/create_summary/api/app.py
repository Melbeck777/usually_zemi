from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import datetime
import sys
import queue
import os
from pathlib import Path
sys.path.append("..")
from module.get_lab_data import GetLabMember
from module.get_lab_data import GetLabInfo
from module.read_summary import ReadSummary
from module.make_summary import MakeSummary

index_folder = "../../frontend/dist"
static_folder = "{}/_assets".format(index_folder)
reference_folder = ".."
app = Flask(__name__,static_folder=static_folder,template_folder=index_folder)
app.config["JSON_AS_ASCII"] = False
CORS(app)
TODAY = datetime.datetime.today()

def show_date(day):
    return "{}/{}/{}".format(day.year, day.month, day.day)

def split_content(content, presenter):
    res_content = []
    content_exit_flag = False
    for name in presenter:
        current_list = []
        for title in content[name]:
            if len(content[name][title]) == 0:
                current_list.append("")
                continue
            content_exit_flag = True
            current_txt = ""
            for txt in content[name][title]:
                if len(txt) == 0 or txt == "['']":
                    continue
                current_txt += "{}\n".format(txt)
            current_list.append(current_txt[:-1])
        res_content.append(current_list)
    return res_content, content_exit_flag

def list_to_string(str_list):
    res = ""
    for line in str_list:
        res += "{}\n".format(line)
    return res[:-1]

def summary_to_dict(summary, presenter):
    names = list(presenter.keys())
    titles = list(presenter[names[0]].keys())
    for index, name in enumerate(presenter):
        for title_index, title_name in enumerate(titles):
            if len(summary[index][title_index]) == 0:
                continue
            for content in summary[index][title_index].split("\n"):
                presenter[name][title_name].append(content)
    return presenter

def path_to_date(date_str):
    date = datetime.datetime.strptime(date_str, "%Y%m%d")
    print(date)
    res_str = "{}/{}/{}".format(date.year, date.month, date.day)
    return res_str

def date_to_path(date):
    return "{}{:0>2}{:0>2}".format(date.year,date.month, date.day)

def get_blank_material_list(fullname_list, folder, schedule):
    res_list = [[] for i in range(len(fullname_list))]
    today = datetime.datetime.today()
    for date in schedule:
        if today < date:
            continue
        path_date = date_to_path(date)
        date_str = path_to_date(path_date)
        date_folder = os.path.join(folder, path_date)
        flag_list = [False for i in range(len(fullname_list))]
        for now in Path(date_folder).glob("*.pdf"):    
            base_name_str = str(os.path.basename(now))
            for index, name in enumerate(fullname_list):
                print("name, ",name)
                if name in base_name_str:
                    print("{} in {}".format(name,now))
                    flag_list[index] = True
        for index in range(len(fullname_list)):
            if flag_list[index]:
                continue
            res_list[index].append(date_str)
    return res_list

@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html")


'''
return {
    [
        {
            year:int,
            lab_group:[
                {
                    group_name:str,
                    lab_name_list:list
                }
            ]
        }
    ]
}
'''
@app.route('/summary', methods=["GET"])
def get_summary_menu():
    LabInfo = GetLabInfo(reference_folder)
    years = LabInfo.get_year()
    res = []
    for year in years:
        LabMember = GetLabMember(year, reference_folder)
        lab_group_pair_list = LabMember.create_lab_group_pair()
        current_list = []
        for lab_name in lab_group_pair_list:
            current_list.append({"lab":lab_name, "group":lab_group_pair_list[lab_name]})
        res.append({"year":year, "lab_group":current_list})
    return jsonify(res)

'''
return {
    [
        lab:string,
        group:list
    ]
}
'''
# test_url = /summary/2022
@app.route('/summary/<int:year>', methods=['GET'])
def get_lab_group(year):
    res_lab_group_list = []
    LabMember = GetLabMember(year, reference_folder)
    lab_data = LabMember.create_lab_group_pair()
    for lab_name in lab_data:
        res_lab_group_list.append({"lab":lab_name,"group":lab_data[lab_name]})
    return jsonify(res_lab_group_list)


'''
return {
    lab_name:string,
    group_name:string,
    member:list,
    meeting:[
        {
            day:year/month/day.
            content:list[list],
            announcement:list,
            recorder:str,
            absence:str,
        }
    ],
    titles:list
}
'''
# test_url = /summary/2022/Test1/a
@app.route('/summary/<int:year>/<lab_name>/<group_name>/weekly', methods=['GET'])
def get_summary_data(year, lab_name, group_name):
    date = datetime.date(year, 4, 1)
    group_info = [lab_name, group_name]
    RS = ReadSummary(group_info, date, reference_folder=reference_folder)
    res_group_data = {"lab_name":lab_name, "group_name":group_name}
    member_list  = []
    meeting_list = []
    presenter = RS.LabData.get_presenter()
    member_list = list(presenter.keys())
    res_group_data["member"] = member_list
    schedule = RS.LabData.get_schedule(group_info)
    for index, day in enumerate(schedule):
        current_presenter = RS.LabData.get_presenter()
        current_dict = {"day":show_date(day),"content":[],"announcement":[], "recorder":"", "absence":""}
        today_summary_file_name = RS.get_summary_file_name(member_list[index%len(member_list)],day)
        if os.path.exists(today_summary_file_name) == False:
            current_dict["content"] = [["" for i in range(len(current_presenter[member_list[0]]))]for i in range(len(current_presenter))]
        else:
            content = RS.get_summary_contents(today_summary_file_name, current_presenter)
            current_dict["content"],empty_flag = split_content(content,current_presenter) 
            announcement = RS.get_announcements(today_summary_file_name,current_presenter)
            current_dict["announcement"] = list_to_string(announcement)
            current_dict["recorder"], current_dict["absence"] = RS.get_recorder_absence(today_summary_file_name)
        meeting_list.append(current_dict)
    res_group_data["blank"] = get_blank_material_list(RS.LabData.get_fullname_list(presenter), RS.LabData.pdf_folder, schedule)
    print("blank,",res_group_data["blank"])
    res_group_data["meeting"] = meeting_list
    res_group_data["titles"] = list(presenter[member_list[0]].keys())
    # print("res_group_data, ",res_group_data)
    return jsonify(res_group_data)


@app.route('/summary/<int:year>/<lab_name>/<group_name>/weekly/<int:day_index>', methods=['POST'])
def load_summary(year, lab_name, group_name, day_index):
    post_data = request.get_json()
    meeting   = post_data['meeting']
    sep_date_flag = post_data['sep_date_flag']
    edit_summary_content = meeting['content']
    announcement = meeting['announcement']
    recorder = meeting['recorder']
    absence = meeting['absence']
    if type(announcement) is not list:
        announcement = announcement.split("\n")
    if sep_date_flag:
        MS = MakeSummary([lab_name, group_name], day_index, reference_folder)
    else:
        sep_date = TODAY + datetime.timedelta(weeks=1)
        MS = MakeSummary([lab_name, group_name], day_index, reference_folder, sep_date)
    presenter = MS.LabData.get_presenter()
    edit_summary = summary_to_dict(edit_summary_content, presenter)
    MS.create_one_day_summary_edited(day_index,edit_summary,announcement,absence,recorder)
    return jsonify({})

'''
return {
    day:yyyy/mm/dd,
    announcement:list
    content:list[list],
    recorder:str
}
'''
@app.route('/summary/<int:year>/<lab_name>/<group_name>/weekly/<int:meeting_key>' , methods=['GET'])
def get_one_meeting(year, lab_name, group_name, meeting_key):
    group_info = [lab_name, group_name]
    date = datetime.datetime(year, 4, 1)
    RS = ReadSummary(group_info, date, reference_folder=reference_folder)
    schedule = RS.LabData.get_schedule(group_info)
    today = schedule[meeting_key]
    meeting = {"day":show_date(today), "announcement":[""]}
    presenter = RS.LabData.get_presenter()
    member_list = list(presenter.keys())
    file_name = RS.get_summary_file_name(member_list[meeting_key%len(member_list)],today)
    while os.path.exists(file_name) == False:
        continue
    content = RS.get_summary_contents(file_name, presenter)
    meeting["content"], content_exit_flag = split_content(content,presenter) 
    announcement = RS.get_announcements(file_name,presenter)
    meeting["announcement"] = list_to_string(announcement)
    if content_exit_flag:
        meeting["recorder"], meeting["absence"] = RS.get_recorder_absence(file_name)
    else:
        meeting["recorder"] = ""
        meeting["absence"] = ""
    res = {"meeting":meeting, "blank":get_blank_material_list(RS.LabData.get_fullname_list(presenter), RS.LabData.pdf_folder, schedule)}
    return jsonify(res)

'''
return {
    member:list,
    meeting_list:[
        {
            day:year/month/day.
            content:list,
            announcement:list   
        }
    ],
}
'''
# @app.route('/summary/<int:year>/<lab_name>/<group_name>/monthly', methods=['GET'])
# def get_month_show(year,lab_name, group_name, month): 


if __name__ == "__main__":
    app.run( port=5000, use_debugger=True, use_reloader=True)