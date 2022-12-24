from module.write_index import md_index
from module.write_index import write_index

make = write_index(".", ".\\zemi","md",["Test1", "a"])
make.write_index_file()
mi = md_index(".",".\\zemi")
mi.mark_to_pdf()