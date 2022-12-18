import datetime
import pandas as pd


class get_lab_member:
    def __init__(self):
        self.day = datetime.datetime.today()
        self.term = self.get_term()
        self.member_data_file = "./member/{}_member.xlsx".format(str(self.day.year-self.term))
        self.member_data = pd.read_excel(self.member_data_file)

        # 研究室，研究班，学年，氏
        self.target_index = [9,11,0,1]
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
    
    def get_term(self):
        term = 0
        if self.day.month < 4:
            term += 1
        return term

    def get_lab_group_list(self):
        res = []
        lab_group_list = self.member_data[[self.columns[self.target_index[0]], self.columns[self.target_index[1]]]]
        for index, element in enumerate(lab_group_list[self.columns[self.target_index[1]]]):
            if type(element) is float:
                continue
            res.append([lab_group_list[self.columns[self.target_index[0]]][index], element])
        return res

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
            else:
                lab_member[lab_name][group_name][degree].append(person_name)
        return lab_member

    # member.xlsxから研究室名と班名の対応リストを取得する
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
    
    # 議事録を編集する順番を取得する
    def get_edit_order(self, group_info):
        lab_member = self.all_lab_member[group_info[0]]
        edit_order = []
        degree_order = {'D':[3,3], 'M':[2,2], 'B':[2,4]}
        group_member = lab_member[group_info[1]]
        for it in degree_order:
            for index in range(degree_order[it][0]):
                current_degree = it+str(degree_order[it][1]-index)
                if current_degree not in group_member:
                    continue
                for person in group_member[current_degree]:
                    edit_order.append(person)
        return edit_order

    # ある班のゼミに参加する人を取得する
    def get_participant(self, group_info):
        lab_member = self.all_lab_member[group_info[0]]
        participants = self.get_professor(group_info)
        degree_order = {'D':[3,3], 'M':[2,2], 'B':[2,4]}
        group_member = lab_member[group_info[1]]
        for it in degree_order:
            for index in range(degree_order[it][0]):
                current_degree = it+str(degree_order[it][1]-index)
                if current_degree not in group_member:
                    continue
                for person in group_member[current_degree]:
                    participants += ', {}'.format(person)
        if 'B3' in lab_member:
            participants += self.get_B3(group_info)
        return participants

    def get_professor(self, group_info):
        res = ""
        for name in self.all_lab_member[group_info[0]][self.teacher_label]:
            res += name + "教授, "
        return res

    def get_B3(self, group_info):
        res = ""
        b3_students = self.all_lab_member[group_info[0]][self.b3_label]
        for b3 in b3_students:
            if self.sep_date < self.day and group_info[1] != b3[1]:
                continue
            res += ", " + b3[0]
        return res