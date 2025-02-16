import os  
import chardet  
import re  # 添加正则表达式模块

# 定义全局变量
utf8files = 0
solvedfiles = 0

def convert_to_utf8(file_path):  
    global utf8files, solvedfiles
    with open(file_path, 'rb') as f:  
        content = f.read()  
        source_encoding = chardet.detect(content)['encoding']  
        if source_encoding is None:  
            common_encodings = ['utf-8', 'gbk', 'gb2312', 'iso-8859-1', 'gb18030','shiftjis']
            for encoding in common_encodings:
                try:
                    content = content.decode(encoding)
                    source_encoding = encoding
                    with open(file_path, 'w', encoding = 'utf-8') as f:  
                        f.write(content)
                    print(f"[{file_path}] is converted from {source_encoding} to utf-8")
                    return
                except:
                    continue
            print(f"[{file_path}] Can't detect the encoding")
        else:
            if source_encoding.lower() == 'utf-8' or source_encoding.lower() == 'ascii':
                utf8files += 1
                print(f"[{file_path}] is already a utf-8 file.")
                return
            content = content.decode(source_encoding)  
            with open(file_path, 'w', encoding = 'utf-8') as f:  
                f.write(content)
                f.close()
            print(f"[{file_path}] is converted from {source_encoding} to utf-8")
            solvedfiles += 1
        f.close()

def convert_folder_to_utf8(folder_path):
    global filesTail
    for filename in os.listdir(folder_path):  
        # 不扫描隐藏目录
        if filename[0] == '.':
            continue
        file_path = os.path.join(folder_path, filename)  
        # 处理fileIgnore中的匹配的文件，支持正则表达式
        if is_ignore_file(filename):
            print(f"[{filename}]Skiped by ignore")
            continue
        if os.path.isdir(file_path):  
            convert_folder_to_utf8(file_path)
        else:
            if filename.split('.')[-1] in filesTail:
                convert_to_utf8(file_path)
            else:
                print(f"[{file_path}]Skiped")

def is_ignore_file(file_path):
    global fileIgnore
    for ignore in fileIgnore:
        if re.match(ignore, file_path):  # 使用正则表达式进行匹配
            return True
    return False

filesTail = ['txt','cs','c','cpp','h','hpp','java','py','js','html','css','xml','json','md','sh','bat','sql','php','asp','aspx','jsp','lua','rb','pl','go','swift','kt','scala','groovy','ts','vue','dart','r','m','mm']
# 支持正则表达式
fileIgnore = []
# 遍历文件夹中的所有文件  
if __name__ == '__main__':
    ignoreFile = ".redecodeignore"
    if os.path.exists(ignoreFile):
        with open(ignoreFile, 'r') as f:
            fileIgnore = f.read().split('\n')
    fileIgnore = list(filter(None, fileIgnore))
    print(f"ignore files: {fileIgnore}")
    folder_path = input('input your file root path:')
    while not os.path.isdir(folder_path):
        folder_path = input('input your file root path:')
    # 递归遍历文件夹中的所有文件
    convert_folder_to_utf8(folder_path)
    print(f"There is {utf8files} utf-8 files and {solvedfiles} files are converted")
    if solvedfiles == 0:
        print("Congratunations, all files are already utf-8")

