import datetime
import pandas as pd
import os
from pathlib import Path

# dayの初期値
TODAY = datetime.datetime.today()
TERM = 0
if TODAY.month < 4:
    TERM = 1

read_path = 'read_path.txt'
data_path_dict = {}

with open(read_path,'r', encoding="utf-8") as f:
    txt = f.read().split("\n")
    for row in txt:
        now = row.split(',')
        data_path_dict[now[0]] = now[1]

class GetLabInfo:
    def __init__(self, reference_folder=data_path_dict["reference"]):
        self.reference_folder = reference_folder
        self.member_folder = data_path_dict["member"]

    def get_year(self):
        res = []
        for file in Path(self.member_folder).glob("*.csv"):
            base_name = os.path.basename(file)
            print("base_name, ",base_name)
            year = base_name.split("_")[0]
            if year in res:
                continue
            res.append(year)
        return res

class GetLabMember:
    def __init__(self, year=TODAY.year-TERM, reference_folder=data_path_dict["reference"]):
        self.reference_folder = reference_folder
        self.year = year
        self.member_data_file = os.path.join(data_path_dict["member"], "{}_member.csv".format(str(self.year)))
        print("member_data_file : {}".format(self.member_data_file))
        self.member_data = pd.read_csv(self.member_data_file)
        
        # 研究室，研究班，学年，氏, 氏名
        self.target_index = [9,11,0,1,5]
        self.teacher_label = "教員"
        self.b3_label = "B3"
        self.columns = self.member_data.columns

        # 研究室に所属する学年のカテゴリーとそのカテゴリーの最大人数
        # B4, M1~2, D1~3
        self.degree_order = {'D':[3,3], 'M':[2,2], 'B':[1,4]} 
        self.lab_group_list = self.get_lab_group_list()
        self.all_lab_member = self.get_lab_member()
        
        # 二回目のゼミ以降
        self.sep_date = datetime.datetime(2022,10,13)

    # 複数の研究室と協働でメンバーの情報を共有しているため、研究室名の取得
    def get_lab_names(self):
        res = []
        for it in self.all_lab_member:
            if type(it) is float:
                continue
            res.append(it)
        return res

    def get_lab_group_list(self):
        res = []
        now_targets = [self.columns[self.target_index[0]], self.columns[self.target_index[1]]]
        lab_group_list = self.member_data[now_targets].drop_duplicates()

        for index in lab_group_list[now_targets[0]].keys():
            lab_name = lab_group_list[now_targets[0]][index]
            group_name = lab_group_list[now_targets[1]][index]
            if type(group_name) is float:
                continue
            res.append([lab_name, group_name])
        res = sorted(res)
        return res

    def create_lab_group_pair(self):
        res = {}
        lab_names = self.get_lab_names()
        for name in lab_names:
            res[name] = []
        for pair in self.lab_group_list:
            res[pair[0]].append(pair[1])
        return res

    # メンバーデータを取得する際の形を先に作っておく
    def create_lab_model(self):
        res = {}
        for element in self.lab_group_list:
            if element[0] not in res:
                res[element[0]] = {}
                res[element[0]][self.teacher_label] = []
                res[element[0]][self.b3_label] = []
            res[element[0]][element[1]] = {}
            for degree in self.degree_order:
                for index in range(self.degree_order[degree][0]):
                    res[element[0]][element[1]][str("{}{}".format(degree, str(self.degree_order[degree][1]-index)))] = []               
        return res

    # 研究室のメンバーを分類
    # 研究室 > 班 > 学年
    def get_lab_member(self):
        columns = self.member_data.columns
        lab_member = self.create_lab_model()
        for index, lab_name in enumerate(self.member_data[columns[self.target_index[0]]]):
            group_name  = self.member_data[columns[self.target_index[1]]][index]
            degree      = self.member_data[columns[self.target_index[2]]][index]
            person_name = self.member_data[columns[self.target_index[3]]][index]

            if degree == self.teacher_label:
                lab_member[lab_name][self.teacher_label].append(person_name)
            elif degree == self.b3_label:
                lab_member[lab_name][self.b3_label].append([person_name, group_name])
            elif (type(group_name) is float) or (type(degree) is float) or (type(person_name) is float):
                continue
            else:
                lab_member[lab_name][group_name][degree].append(person_name)
        return lab_member
    
    # member.csvから研究室名と班名の対応リストを取得する
    def get_group(self, lab_name):
        group_list = []
        for group_name in self.all_lab_member[lab_name]:
            if group_name == '教員' or group_name == 'B3':
                continue
            elif group_name in group_list:
                continue
            else:
                group_list.append([lab_name,group_name])
        return group_list
    
    # 記載する項目の取得
    def get_title_names(self):
        path = os.path.join("..","READMe.md")
        title_names = []
        target = '<!-- title -!>'
        with open(path, 'r', encoding='utf-8') as f:
            now_text = f.read().split('\n')
            rule_index = now_text.index('## Rule')
            for now_data in now_text[rule_index:]:
                if target in now_data:
                    res = now_data.replace(' {}'.format(target),'').split(' ')[-1]
                    title_names.append(res)
        return title_names

    def get_schedule(self, group_info):
        schedule_path = os.path.join(data_path_dict["schedule"],"{}_schedule.csv".format(self.year))
        print(schedule_path)
        schedule = pd.read_csv(schedule_path, encoding="utf-8")
        group_schedule = []
        for index, element in enumerate(schedule["day"]):
            current_day = datetime.datetime.strptime("{} {}".format(element, schedule[group_info[1]][index]),"%Y/%m/%d %H:%M")
            group_schedule.append(current_day)
        return group_schedule

class GetLabData(GetLabMember):
    def __init__(self, group_info, day, reference_folder=data_path_dict["reference"]):
        self.group_info = group_info
        self.day = day
        self.term = self.get_term()
        self.pdf_folder = data_path_dict["pdf"].format(group_info[1], self.day.year)
        self.out_folder = data_path_dict["out"].format(group_info[1], self.day.year)
        super().__init__(day.year-self.term,reference_folder)
    
    
    def get_fullname_list(self, presenter):
        fullname_list = []
        for index, row in enumerate(self.member_data[self.columns[self.target_index[4]]]):
            if self.member_data[self.columns[self.target_index[0]]][index] != self.group_info[0] or self.member_data[self.columns[self.target_index[1]]][index] != self.group_info[1]:
                continue
            fullname_list.append(row)

        res_fullname_list = []
        for presenter_name in presenter: 
            for name in fullname_list:
                if presenter_name in name:
                    res_fullname_list.append(name.replace(" ",""))
                    break
        print(res_fullname_list)
        return res_fullname_list

    def get_term(self,day=None):
        if day is None:
            day = self.day
        if day.month < 4:
            return 1
        return 0
    
    # 発表者の情報を取得する
    def get_presenter(self):
        presenter = {}
        titles = self.get_title_names()
        group_data = self.all_lab_member[self.group_info[0]][self.group_info[1]]
        for degree in group_data:
            if len(group_data[degree]) == 0:
                continue
            for person in group_data[degree]:
                presenter[person] = {}
                for title in titles:
                    presenter[person][title] = []
        return presenter
    
    def get_professor(self):
        res = ""
        print(self.all_lab_member[self.group_info[0]])
        for name in self.all_lab_member[self.group_info[0]][self.teacher_label]:
            res += name + "教授, "
        return res

    def get_B3(self):
        res = ""
        b3_students = self.all_lab_member[self.group_info[0]][self.b3_label]
        for b3 in b3_students:
            if self.sep_date < self.day and self.group_info[1] != b3[1]:
                continue
            res += ", " + b3[0]
        return res

    # 議事録を編集する順番を取得する
    def get_edit_order(self):
        edit_order = []
        lab_member = self.all_lab_member[self.group_info[0]]
        degree_order = {'D':[3,3], 'M':[2,2], 'B':[2,4]}
        group_member = lab_member[self.group_info[1]]
        for it in degree_order:
            for index in range(degree_order[it][0]):
                current_degree = it+str(degree_order[it][1]-index)
                if current_degree not in group_member:
                    continue
                for person in group_member[current_degree]:
                    edit_order.append(person)
        return edit_order

    # ある班のゼミに参加する人を取得する
    # 発表者ではない教授やB3を含む。発表者ではない人について記録することはない
    def get_participant(self,absences=[]):
        lab_member = self.all_lab_member[self.group_info[0]]
        participants = self.get_professor()
        degree_order = {'D':[3,3], 'M':[2,2], 'B':[2,4]}
        group_member = lab_member[self.group_info[1]]
        for it in degree_order:
            for index in range(degree_order[it][0]):
                current_degree = it+str(degree_order[it][1]-index)
                if current_degree not in group_member:
                    continue
                for pi in range(len(group_member[current_degree])):
                    if group_member[current_degree][pi] in absences:
                        continue
                    participants += "{}, ".format(group_member[current_degree][pi])
        if 'B3' in lab_member:
            participants += self.get_B3()
        if participants[-2:] == ", ":
            participants = participants[:-2]
        print("get_professor = {}".format(self.get_professor()))
        print("get_B3 = {}".format(self.get_B3()))
        print("participants = {}".format(participants))
        return participants

    '''
    pdf/20221010
    のように班員の資料が保存されたフォルダがあるのでそれを作るための準備
    '''
    def today_summary_folder(self,date=None):
        if date == None:
            date = self.day
        return '{:0>4}{:0>2}{:0>2}'.format(str(date.year),str(date.month),str(date.day))
