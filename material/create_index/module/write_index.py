from pathlib import Path
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
import pdfkit



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