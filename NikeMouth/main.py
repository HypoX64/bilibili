import os
import sys
import numpy as np
import cv2
import normal2nike
sys.path.append("..")
from Util import util,ffmpeg
from options import Options
opt = Options().getparse()

util.file_init(opt)

if os.path.isdir(opt.media):
    files = util.Traversal(opt.media)
else:
    files = [opt.media]

for file in files:
    img = cv2.imread(file)
    h,w = img.shape[:2]
    if opt.output == 'image':
        img = normal2nike.convert(img,opt.size,opt.intensity,opt.aspect_ratio,opt.ex_move,opt.mode)
        cv2.imwrite(os.path.join(opt.result_dir,os.path.basename(file)), img)
    elif opt.output == 'video':
        frame = int(opt.time*opt.fps)
        for i in range(frame):
            tmp = normal2nike.convert(img,opt.size,i*opt.intensity/frame,opt.aspect_ratio,
                opt.ex_move,opt.mode)[:4*(h//4),:4*(w//4)]
            cv2.imwrite(os.path.join('./tmp/output_imgs','%05d' % i+'.jpg'), tmp)
        cv2.imwrite(os.path.join(opt.result_dir,os.path.basename(file)), tmp)
        ffmpeg.image2video(
            opt.fps,
            './tmp/output_imgs/%05d.jpg',
            None,
            os.path.join(opt.result_dir,os.path.splitext(os.path.basename(file))[0]+'.mp4'))

# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()