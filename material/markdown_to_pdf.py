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

file = 'README.md'
html = mark_to_html(file)
html_to_pdf(html,file.replace('md','pdf'))