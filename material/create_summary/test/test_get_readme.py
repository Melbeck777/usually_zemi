import re

test_list = ["1. 2cat", "10. 3port", "10.1"]
for it in test_list:
    target = re.compile(r"\d+\. ")
    if target.match(it) != None:
        print(it)