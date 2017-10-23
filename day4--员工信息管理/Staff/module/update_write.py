# -*- coding: UTF-8 -*-
def update_write_in_file(filename,index,content):
    with open(filename,'r',encoding="utf-8") as f:
        lines = f.readlines()
    with open(filename, 'w', encoding="utf-8") as w:
        for j in range(len(lines)):
            if j == index + 1:
                w.write(content+"\n")
            else:
                w.write(lines[j])