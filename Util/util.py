import os
import shutil
def Traversal(filedir):
    file_list=[]
    for root,dirs,files in os.walk(filedir): 
        for file in files:
            file_list.append(os.path.join(root,file)) 
        for dir in dirs:
            Traversal(dir)
    return file_list

def is_img(path):
    ext = os.path.splitext(path)[1]
    ext = ext.lower()
    if ext in ['.jpg','.png','.jpeg','.bmp']:
        return True
    else:
        return False

def is_video(path):
    ext = os.path.splitext(path)[1]
    ext = ext.lower()
    if ext in ['.mp4','.flv','.avi','.mov','.mkv','.wmv','.rmvb','.mts']:
        return True
    else:
        return False

def is_imgs(paths):
    tmp = []
    for path in paths:
        if is_img(path):
            tmp.append(path)
    return tmp

def is_videos(paths):
    tmp = []
    for path in paths:
        if is_video(path):
            tmp.append(path)
    return tmp  

def  writelog(path,log):
    f = open(path,'a+')
    f.write(log+'\n')
    f.close()


def makedirs(path):
    if os.path.isdir(path):
        print(path,'existed')
    else:
        os.makedirs(path)
        print('makedir:',path)

def clean_tempfiles(tmp_init=True):
    if os.path.isdir('./tmp'):   
        shutil.rmtree('./tmp')
    if tmp_init:
        os.makedirs('./tmp')
        os.makedirs('./tmp/video_voice')
        os.makedirs('./tmp/music/')
        os.makedirs('./tmp/video_imgs')
        os.makedirs('./tmp/output_imgs')

def file_init(opt):
    if not os.path.isdir(opt.result_dir):
        os.makedirs(opt.result_dir)
        print('makedir:',opt.result_dir)
    clean_tempfiles()

def get_bar(percent,num = 25):
    bar = '['
    for i in range(num):
        if i < round(percent/(100/num)):
            bar += '#'
        else:
            bar += '-'
    bar += ']'
    return bar+' '+str(round(percent,2))+'%'

def copyfile(src,dst):
    try:
        shutil.copyfile(src, dst)
    except Exception as e:
        print(e)

def second2stamp(s):
    floats = s
    h = int(s/3600)
    s = int(s%3600)
    m = int(s/60)
    s = int(s%60)
    floats = floats - int(floats) + s

    return "%02d:%02d:%.3f" % (h, m, floats)
