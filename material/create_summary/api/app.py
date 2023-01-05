from flask import Flask, render_template, jsonify
from flask_cors import CORS
import datetime
import sys
import os
sys.path.append("..")
from module.get_lab_data import get_lab_member
from module.read_summary import read_summary

index_folder = "../../frontend/dist"
static_folder = "{}/_assets".format(index_folder)
print(index_folder)
print(static_folder)
app = Flask(__name__,static_folder=static_folder,template_folder=index_folder)
app.config["JSON_AS_ASCII"] = False
CORS(app)

def show_date(day):
    return "{}/{}/{}".format(day.year, day.month, day.day)

def split_content(content, presenter):
    res_content = []
    for name in presenter:
        current_txt = ""
        for title in content[name]:
            if len(content[name][title]) == 0:
                continue
            current_txt += title
            for txt in content[name][title]:
                if len(txt) == 0:
                    continue
                current_txt += "\n\t{}".format(txt)
        res_content.append(current_txt)
    return res_content

@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html")

'''
return {
    [
        lab:lab_name, // string
        group:group //list
    ]
}
'''
# test_url = /summary/2022
@app.route('/summary/<int:year>', methods=['GET'])
def get_lab_group(year):
    date = datetime.date(year,4,1)
    res_lab_group_list = []
    lab_member = get_lab_member(date, "..")
    lab_data = lab_member.create_lab_group_pair()
    for lab_name in lab_data:
        res_lab_group_list.append({"lab":lab_name,"group":lab_data[lab_name]})
    return jsonify(res_lab_group_list)

'''
return {
    lab_name:name,
    group_name:name,
    member:[],
    meeting:[
        {
            day:date,
            content:content
        }
    ]
}
'''

# test_url = /summary/2022/Test1/a
@app.route('/summary/<int:year>/<lab_name>/<group_name>', methods=['GET'])
def get_summary_data(year, lab_name, group_name):
    print("{}, {}, {}".format(year, lab_name, group_name))
    date = datetime.date(year, 4, 1)
    group_info = [lab_name, group_name]
    read_summary_object = read_summary(group_info, date, reference_folder="..")
    res_group_data = {"lab_name":lab_name, "group_name":group_name}
    member_list  = []
    meeting_list = []
    presenter = read_summary_object.lab_data.get_presenter()
    for name in presenter:
        member_list.append(name)
    res_group_data["member"] = member_list
    schedule = read_summary_object.lab_data.get_schedule(group_info)
    for index, day in enumerate(schedule):
        current_dict = {"day":show_date(day)}
        today_summary_file_name = read_summary_object.get_summary_file_name(member_list[index%len(member_list)],day)
        if os.path.exists(today_summary_file_name) == False:
            current_dict["content"] = ["" for i in range(len(presenter))]
        else:
            content = read_summary_object.get_summary_contents(today_summary_file_name, presenter)
            current_dict["content"] = split_content(content,presenter)
        meeting_list.append(current_dict)
    res_group_data["meeting"] = meeting_list
    return jsonify(res_group_data)

if __name__ == "__main__":
    app.run( port=5000, use_debugger=True, use_reloader=True)