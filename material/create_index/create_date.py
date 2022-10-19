import os
import datetime
import shutil
from pathlib import Path
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import markdown
from PyPDF2 import PdfFileReader
from pygments import highlight
from pygments.formatters import HtmlFormatter
import pdfkit
import pandas as pd

reference_folder = '.'
zemi_folder = '..'
template_folder = os.path.join(zemi_folder,'template') # your template folder
schedule_file = './schedule.txt' # zemi schedule
index_file = os.path.join(zemi_folder,'index/index.md') # Summary file of table of contes each slides.
my_group = ['精密', '構造物センシング']

with open('bullet_marks.txt', 'r', encoding='utf-8') as f:
    bullet_points_marks = f.read().split('\n')
with open(os.path.join(reference_folder,'ignore.txt'), 'r', encoding='utf-8') as f:
    ignores = f.read().split('\n')

def get_schedule(group_info):
    schedule = []
    term = 0
    today = datetime.datetime.today()
    if today.month < 3:
        term = 1
    path = '{}_schedule.csv'.format(today.year-term)
    data = pd.read_csv(path)
    columns = data.columns
    for index,now_date in enumerate(data[columns[0]]):
        now = "{} {}".format(now_date, data[group_info[1]][index])
        today = datetime.datetime.strptime(now,'%Y/%m/%d %H:%M')
        schedule.append(today)
    return schedule

def mark_to_html(file_name):
    with open(file_name,'r',encoding='utf-8') as f:
        text = f.read()
        style = HtmlFormatter(style='solarized-dark').get_style_defs('.codehilite')
        md = markdown.Markdown(extensions=['extra', 'codehilite'])
        body = md.convert(text)
        html = '<!doctype html><html lang="ja"><meta charset="UTF-8"><body>'
        html += '<style>{}</style>'.format(style)
        html += '''<style> table,th,td{
            border-collapse:collapse;
            border:1px solid #333;
            }</style> '''
        html += body+'</body></html>'
    return html

def html_to_pdf(html:str,output_file_name):
    path_to_pdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_pdf)
    pdfkit.from_string(html,output_file_name,configuration=config)


def mark_to_pdf(file):
    html = mark_to_html(file)
    html_to_pdf(html,file.replace('md','pdf'))

def get_bullet_name():
    path = 'READMe.md'
    bullets_name = {}
    target = '<!-- title -!>'
    with open(path, 'r', encoding='utf-8') as f:
        now_text = f.read().split('\n')
        rule_index = now_text.index('## Rule')
        for now_data in now_text[rule_index:]:
            if target in now_data:
                res = now_data.replace(' {}'.format(target),'').split(' ')[-1]
                bullets_name[res] = []
    return bullets_name

# Get data from slide pdf
def get_contents_value(file_name):
    current_contents = get_bullet_name()
    with open(file_name,'rb') as f:
        reader = PdfFileReader(f)
        page_numbers = reader.getNumPages()
        for index in range(page_numbers):
            now_text = reader.getPage(index).extract_text().split('\n')
            target_name = ''
            for title in current_contents:
                if title in now_text[0]:
                    target_name = title
                    if len(now_text) > 2:
                        now_text = now_text[1:-1]
                    elif len(now_text) == 2:
                        now_text = [now_text[1]]
            if target_name == '':
                continue
            pre_bullet  = False
            for it in now_text:
                it = remove_ignore(it)
                bullet_flag = False
                for bullet in bullet_points_marks:
                    if bullet not in it:
                        continue
                    bullet_flag = True
                    current_contents[target_name].append(it[it.index(bullet)+1:])
                if bullet_flag:
                    pre_bullet = bullet_flag
                    continue
                if pre_bullet and bullet_flag == False:
                    current_contents[target_name][-1] += it 
                    continue 
                current_contents[target_name].append(it)
    return current_contents

def remove_ignore(str):
    it = str
    for ignore in ignores:
        if ignore in it:
            it = it[len(ignore)+1:]
    return it

# Get data from index.md
def get_each_day_contents():
    each_days_contents = {}
    sep_date = datetime.datetime(2022,10,19,0,0)
    bullets = get_bullet_name()
    with open(index_file,'r', encoding='utf-8') as f:
        index_str = f.read()
        row = index_str.split('\n')
        current_date = ''
        for now in row:
            if now[0] == '-':
                current_date = now.split(' ')[1]
                current = datetime.datetime.strptime(current_date, '%Y/%m/%d')
                current_bullet = ''
                if sep_date < current:
                    each_days_contents[current_date] = {}
                else:
                    each_days_contents[current_date] = []
            elif sep_date < current:
                bullet_flag = False
                for bullet in bullets:
                    if bullet in now:
                        current_bullet = bullet
                        each_days_contents[current_date][current_bullet] = []
                        bullet_flag = True
                        continue
                if bullet_flag:
                    continue
                each_days_contents[current_date][current_bullet].append(now.split(' ')[1])
            else:
                each_days_contents[current_date].append(now.split(' ')[-1])
    return each_days_contents

def create_translate_folder(date, zemi_folder):
    to_name = os.path.join(zemi_folder,'{}_{}'.format(date.month, date.day))
    if os.path.exists(to_name) == False:
        shutil.copytree(template_folder, to_name)
    return to_name

def get_editor_name(path):
    return os.path.basename(path).split('_')[0]

def translate_pptx(date, zemi_folder):
    date_folder = create_translate_folder(date,zemi_folder)
    for ppt in Path(date_folder).glob('*.pptx'):
        editor_name = get_editor_name(ppt)
        to_name = os.path.join(date_folder, '{}_{:0>4}{:0>2}{:0>2}.pptx'.format(editor_name,current_date.year,current_date.month,current_date.day))
        if os.path.exists(to_name) == False:
            shutil.move(ppt,to_name)
            print('{} => {}'.format(ppt,to_name))
    return to_name.replace('pptx','pdf')

schedule = get_schedule(my_group)
index_data = get_each_day_contents()
new_line = 0
for current_date in schedule:
    pdf_path = translate_pptx(current_date, zemi_folder)
    day = '{}/{}/{}'.format(current_date.year,current_date.month,current_date.day)

    if os.path.exists(pdf_path) != True:
        continue
    if day in index_data:
        continue
    today_contents = get_contents_value(pdf_path)
    
    today_flag = True
    for index,target in enumerate(today_contents):
        if len(today_contents[target]) == 0:
            today_flag = False
        if index == 0:
            break
    if today_flag != True:
        continue
    with open(index_file,'a', encoding='utf-8') as index_f:
        index_f.write('\n- {}'.format(day))
        new_line += 1
        for point in today_contents:
            if len(today_contents[point]) == 0:
                continue
            new_line += 1
            index_f.write('\n\t- {}'.format(point))
            for cell in today_contents[point]:
                new_line += 1
                index_f.write('\n\t\t- {}'.format(cell.replace(' ','')))
if new_line > 0:
    mark_to_pdf(index_file)