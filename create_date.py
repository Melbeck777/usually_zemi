import os
import datetime
import shutil
from pathlib import Path
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO
import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
import pdfkit


with open('bullet_marks.txt', 'r', encoding='utf-8') as f:
    bullet_points_marks = f.read().split('\n')

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

def get_contents_value(file_name):
    current_contents = []

    with open(file_name,'rb') as f:
        resource_manager = PDFResourceManager()
        output = StringIO()
        LapPrams = LAParams()
        text_converter = TextConverter(resource_manager, output, laparams=LapPrams)
        page_interpreter = PDFPageInterpreter(resource_manager,text_converter)
        for index,now in enumerate(PDFPage.get_pages(f)):
            if index == 1:
                page_interpreter.process_page(now)
        output_text = output.getvalue()
        output.close()
        text_converter.close()
    
    non_mark_count = 0
    for contents in output_text.split('\n'):
        if non_mark_count == 2:
            break
        elif len(contents) == 0:
            continue
        elif contents[0] in bullet_points_marks:
            current_contents.append(contents[1:])
        else:
            non_mark_count += 1
    return current_contents

template_folder = './template' # your template folder
schedule_file = './schedule.txt' # zemi schedule
index_file = 'index/index.md' # Summary file of table of contes each slides.

each_days_contents = {}
with open(index_file,'r', encoding='utf-8') as f:
    index_str = f.read()
    row = index_str.split('\n')
    current_date = ''
    current_contents = []
    for now in row:
        if now[0] == '-':
            if len(current_contents) > 0:
                each_days_contents[current_date] = current_contents
                current_contents = []
            current_date = now.split(' ')[1]
        else:
            current_contents.append(now.split(' ')[-1])
print(each_days_contents)

with open(schedule_file, 'r', encoding='utf-8') as f:
    reader = f.read().split('\n')
    for now in reader:
        current_date = datetime.datetime.strptime(now, '%Y/%m/%d')
        date_folder_name = '{}_{}'.format(current_date.month,current_date.day)
        if os.path.exists(date_folder_name) == False:
            shutil.copytree(template_folder,date_folder_name)
        for ppt in Path(date_folder_name).glob("*.pptx"):
            editor_name = os.path.basename(ppt).split('_')[0]
            to_name = os.path.join(date_folder_name, '{}_{:0>4}{:0>2}{:0>2}.pptx'.format(editor_name,current_date.year,current_date.month,current_date.day))
            if os.path.exists(to_name) == False:
                shutil.move(ppt,to_name)
                print('{} => {}'.format(ppt,to_name))
        day = '- {}/{}/{}'.format(current_date.year,current_date.month,current_date.day)
        pdf_name = to_name.replace('pptx','pdf')
        if os.path.exists(pdf_name) == True:
            today_contents = get_contents_value(pdf_name)            
            if index_str.count(day) == 0:
                with open(index_file,'a', encoding='utf-8') as index_f:
                    index_f.write('\n{}'.format(day))
                    for cell in today_contents:
                        index_f.write('\n\t- {}'.format(cell))
        mark_to_pdf(index_file)