import os
from pathlib import Path
from openpyxl import Workbook
import pandas as pd
import random
import datetime
import shutil

labels = ["学年","氏","名","セイ","メイ","氏名","セイメイ","学籍番号","メアド","研究室","大臣","研究班"]

first_name = {"山田":"ヤマダ","岡田":"オカダ","西田":"ニシダ",
                "本田":"ホンダ","井口":"イグチ","千堂":"センドウ",
                "三浦":"ミウラ","神山":"カミヤマ","長野":"ナガノ",
                "安藤":"アンドウ","斎藤":"サイトウ","志摩":"シマ",
                "森":"モリ","田畑":"タバタ","津田":"ツダ"}
last_name = {"薫":"カオル","亮":"リョウ","康太":"コウタ",
                "秀樹":"ヒデキ","玲央":"レオ","和樹":"カズキ",
                "亮太":"リョウタ","健之":"タケユキ","一":"ハジメ",
                "綾瀬":"アヤセ","理子":"リコ","南":"ミナミ",
                "圭祐":"ケイスケ","真司":"シンジ","拓実":"タクミ"}

def to_list(dict):
    return [key for key in dict.keys()]

first_keys = to_list(first_name)
last_keys  = to_list(last_name)

def get_key():
    first_key = first_keys[random.randrange(len(first_keys))]
    last_key  =  last_keys[random.randrange(len(last_keys))]
    return first_key, last_key

def to_name(first_key, last_key):
    full_name = "{} {}".format(first_key,last_key)
    furigana  = "{} {}".format(first_name[first_key],last_name[last_key])
    return full_name, furigana

def print_list(list):
    for index, element in enumerate(list):
        print("{}:{}".format(index,element))

def to_email_address(number):
    return number+"@mail.com"

degrees = {"教員":"16999","M2":"21002","M1":"22002","B4":"19001","B3":"20001"}
degrees_key = to_list(degrees)
lab_names = ["Test1", "Test2"]
group_names = ["a","b","c",""]

def create_test_member():
    full_names = []
    wb = Workbook()
    ws = wb.active
    ws.append(labels)

    with open("test_member.txt") as f:
        read = f.read().split("\n")
        for line in read:
            current_index = [int(x) for x in line.split(",")]
            first_key, last_key = get_key()
            full_name, furigana = to_name(first_key, last_key)
            while (full_name in full_names):
                first_key, last_key = get_key()
                full_name, furigana = to_name(first_key,last_key)
            degree_key = degrees_key[current_index[0]]
            student_number = degrees[degree_key]+"{:0>3}".format(str(random.randrange(100)))
            lab_name = lab_names[current_index[1]]
            group_name = group_names[current_index[2]]
            full_names.append(full_name)
            ws.append([degree_key,first_key,last_key,first_name[first_key],last_name[last_key],full_name,furigana,student_number,to_email_address(student_number),lab_name,'',group_name])
    wb.save('member/2022_member.xlsx')

def get_member_name():
    df = pd.read_excel('member/2022_member.xlsx')
    return df

def create_pdf_directory(lab_names, group_names):
    base_path = "pdf"
    schedule = get_schedule()
    for lab in lab_names:
        for group in group_names:
            for day in schedule:
                current_directory = os.path.join(base_path, lab, group, "{}{:0>2}{:0>2}".format(day.year,day.month,day.day))
                os.makedirs(current_directory)

def get_schedule():
    read = pd.read_csv("./schedule/2022_schedule.csv")
    res = []
    for index,day in enumerate(read["day"]):
        res.append(datetime.datetime.strptime(day, "%Y/%m/%d"))
    return res

def get_target_schedule(group_name):
    read = pd.read_csv("./schedule/2022_schedule.csv")
    res = []
    for index,day in enumerate(read["day"]):
        res.append(datetime.datetime.strptime("{} {}".format(day,read[group_name][index]), "%Y/%m/%d %H:%M"))
    return res

def date_to_path(day):
    return "{}{:0>2}{:0>2}".format(day.year,day.month,day.day)


def copy_pptx(lab_name, group_name):
    df = get_member_name()
    group_member = df[(df[labels[-3]]==lab_name) & (df[labels[-1]]==group_name)]
    template_pptx = "template/name_year_month_day.pptx"
    base_path = os.path.join("pdf",lab_name,group_name)
    schedule = get_schedule()
    
    for day in schedule:
        current_day = date_to_path(day)
        for person in group_member[labels[5]]:
            person_pptx_path = os.path.join(base_path,current_day,"{}_{}.pptx".format(person.replace(" ",""), current_day))
            shutil.copy(template_pptx,person_pptx_path)
            # print(person_pptx_path)
create_pdf_directory(lab_names, group_names[:3])
for lab_name in lab_names:
    for group_name in group_names[:3]:
        copy_pptx(lab_name, group_name)