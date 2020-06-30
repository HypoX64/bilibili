import os,json
import subprocess

# ffmpeg 3.4.6

def args2cmd(args):
    cmd = ''
    for arg in args:
        cmd += (arg+' ')
    return cmd

def run(args,mode = 0):

    if mode == 0:
        cmd = args2cmd(args)
        os.system(cmd)

    elif mode == 1:
        '''
        out_string = os.popen(cmd_str).read()
        For chinese path in Windows
        https://blog.csdn.net/weixin_43903378/article/details/91979025
        '''
        cmd = args2cmd(args)
        stream = os.popen(cmd)._stream
        sout = stream.buffer.read().decode(encoding='utf-8')
        return sout

    elif mode == 2:
        p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sout = p.stdout.readlines()
        return sout


def video2image(videopath, imagepath, fps=0, start_time=0, last_time=0):
    args = ['ffmpeg', '-i', '"'+videopath+'"']
    if last_time!=0:
        args += ['-ss', start_time]
        args += ['-t', last_time]
    if fps != 0:
        args += ['-r', fps]
    args += ['-f', 'image2','-q:v','-0',imagepath]
    run(args)
        
def video2voice(videopath,voicepath,samplingrate=0):
    args = ['ffmpeg', '-i', '"'+videopath+'"']
    if samplingrate != 0:
        args += ['-ar', str(samplingrate)]
    args += [voicepath]
    run(args)

def image2video(fps,imagepath,voicepath,videopath):
    os.system('ffmpeg -y -r '+str(fps)+' -i '+imagepath+' -vcodec libx264 -b 12M '+'./tmp/video_tmp.mp4')
    os.system('ffmpeg -i ./tmp/video_tmp.mp4 -i "'+voicepath+'" -vcodec copy -acodec aac '+videopath)

def get_video_infos(videopath):
    args =  ['ffprobe -v quiet -print_format json -show_format -show_streams', '-i', '"'+videopath+'"']

    out_string = run(args,mode=1)

    infos = json.loads(out_string)
    try:
        fps = eval(infos['streams'][0]['avg_frame_rate'])
        endtime = float(infos['format']['duration'])
        width = int(infos['streams'][0]['width'])
        height = int(infos['streams'][0]['height'])
    except Exception as e:
        fps = eval(infos['streams'][1]['r_frame_rate'])
        endtime = float(infos['format']['duration'])
        width = int(infos['streams'][1]['width'])
        height = int(infos['streams'][1]['height'])

    return fps,endtime,height,width

def cut_video(in_path,start_time,last_time,out_path,vcodec='h265'):
    if vcodec == 'copy':
        os.system('ffmpeg -ss '+start_time+' -t '+last_time+' -i "'+in_path+'" -vcodec copy -acodec copy '+out_path)
    elif vcodec == 'h264':    
        os.system('ffmpeg -ss '+start_time+' -t '+last_time+' -i "'+in_path+'" -vcodec libx264 -b 12M '+out_path)
    elif vcodec == 'h265':
        os.system('ffmpeg -ss '+start_time+' -t '+last_time+' -i "'+in_path+'" -vcodec libx265 -b 12M '+out_path)

def continuous_screenshot(videopath,savedir,fps):
    '''
    videopath: input video path
    savedir:   images will save here
    fps:       save how many images per second
    '''
    videoname = os.path.splitext(os.path.basename(videopath))[0]
    os.system('ffmpeg -i "'+videopath+'" -vf fps='+str(fps)+' -q:v -0 '+savedir+'/'+videoname+'_%06d.jpg')
