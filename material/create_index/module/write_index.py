import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
import pdfkit
import os
from .setup_material import setup_material


## mdのインデックスを作成し、pdf変換するクラス
class md_index:
    def __init__(self, reference_folder, zemi_folder):
        self.setup_material = setup_material(reference_folder, zemi_folder)
        self.file_name = os.path.join(self.setup_material.index_folder, "index.md")

    def mark_to_html(self):
        with open(self.file_name,'r',encoding='utf-8') as f:
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

    def html_to_pdf(self, html:str,output_file_name):
        path_to_pdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_to_pdf)
        pdfkit.from_string(html,output_file_name,configuration=config)

    def mark_to_pdf(self):
        html = self.mark_to_html()
        self.html_to_pdf(html,self.file_name.replace('md','pdf'))
