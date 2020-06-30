import os
import cv2
import numpy as np

import sys
sys.path.append("..")
from Util import util,ffmpeg
'''
                                                                                                               ,
                                                             ,+nnDDDDn1+                                     n@@@1
                   +&MMn                                  1D@@@@@@@@@@@@@&n,                                1@@@@@1
                  D@@@@@,                               nM@@@@@@@@@@@@@@@@@@&+                             1@@@@@@@1
                1M@@@@@@,                             +M@@@@D,,,,,,,,,,,1@@@@@D                          +D@@@@@@@@@D+
        ,1nn,  &@@@@@@@@nnnnnnnn1,                   +@@@@@@M&&&&1 ,&&&&M@@@@@@&                 ,nD&&M@@@@@@@@@@@@@@@@@M&&Dn,
      ,M@@@@1 ,@@@@@@@@@@@@@@@@@@@D                  @@@@@@@@@&1+,  +1DM@@@@@@@@n                &@@@@@@@@@@@@@@@@@@@@@@@@@@@&
      1@@@@@1 ,@@@@@@@@@@@@@@@@@@@n                 n@@@@@@@D  +n1  D1, +M@@@@@@M                 1M@@@@@@@@@@@@@@@@@@@@@@@Mn
      1@@@@@1 ,@@@@@@@@@@@@@@@@@@M                  D@@@@@@n ,M@@D ,@@@n ,@@@@@@@                   1M@@@@@@@@@@@@@@@@@@@Mn
      1@@@@@1 ,@@@@@@@@@@@@@@@@@@+                  1@@@@@@, D@@@D ,@@@@  &@@@@@M                     D@@@@@@@@@@@@@@@@@D
      1@@@@@1 ,@@@@@@@@@@@@@@@@@D                    M@@@@@1,&@@@D ,@@@@1,M@@@@@1                      @@@@@@@@@@@@@@@@@,
      1@@@@@1 ,@@@@@@@@@@@@@@@@@,                    +@@@@@@@@@@@D ,@@@@@@@@@@@D                      +@@@@@@@@@@@@@@@@@+
      1@@@@@1 ,@@@@@@@@@@@@@@@@n                      ,M@@@@@@@@@&+n@@@@@@@@@@n                       n@@@@@@@@@@@@@@@@@D
       D@@@@1 ,@@@@@@@@@@@@@@M1                         1M@@@@@@@@@@@@@@@@@@D,                        M@@@@@MD1+1nM@@@@@@
         ,++   ++++++++++++,                              +nM@@@@@@@@@@@MD1                           nMMD1,        1DMMD
                                                              ,+1nnnn1+,
'''

# 在github看香蕉君
# pixel_imgs_dir = './pixel_imgs/github'
# pixel_imgs_resize = 0 # resize pixel_imgs, if 0, do not resize
# output_pixel_num = 52 # how many pixels in the output video'width 
# video_path = '../Video/素材/香蕉君/香蕉君_3.mp4'
# inverse = False

# 用香蕉看香蕉君
pixel_imgs_dir = './pixel_imgs/banana'
pixel_imgs_resize = 40 # resize pixel_imgs, if 0, do not resize
output_pixel_num = 48 # how many pixels in the output video'width 
video_path = '../Video/素材/香蕉君/香蕉君_3.mp4'
inverse = True

# ------------------------- Load Blocks -------------------------
pixels = []
pixel_paths = os.listdir(pixel_imgs_dir)
pixel_paths.sort()
if inverse:
 pixel_paths.reverse()
for path in pixel_paths:
    pixel = cv2.imread(os.path.join(pixel_imgs_dir,path))
    if pixel_imgs_resize != 0:
        pixel = cv2.resize(pixel,(pixel_imgs_resize,pixel_imgs_resize))
    pixels.append(pixel)
pixel_size = pixels[0].shape[0]
if len(pixels)>2:
    level = 255//len(pixels)
else:
    level = 32
print(pixels[0].shape)

# ------------------------- Prcessing Video -------------------------
fps,endtime,height,width = ffmpeg.get_video_infos(video_path)
scale = height/width

# util.clean_tempfiles(False)
# util.makedirs('./tmp/vid2img')
# util.makedirs('./tmp/output_img')
# ffmpeg.video2image(video_path, './tmp/vid2img/%05d.png')
# ffmpeg.video2voice(video_path, './tmp/tmp.mp3')

# ------------------------- Video2Block -------------------------
print('Video2Block...')
img_names = os.listdir('./tmp/vid2img')
img_names.sort()
for img_name in img_names:
    img = cv2.imread(os.path.join('./tmp/vid2img',img_name))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (output_pixel_num,int(output_pixel_num*scale)))
    
    h,w = img.shape
    out_img = np.zeros((h*pixel_size,w*pixel_size,3), dtype = np.uint8)
    for i in range(h):
        for j in range(w):
            index = np.clip(img[i,j]//level,0,len(pixels)-1)
            out_img[i*pixel_size:(i+1)*pixel_size,j*pixel_size:(j+1)*pixel_size] = pixels[index]
    out_img = out_img[:(h*pixel_size//2)*2,:(w*pixel_size//2)*2]
    cv2.imwrite(os.path.join('./tmp/output_img',img_name), out_img)

# ------------------------- Block2Video -------------------------
ffmpeg.image2video(fps, './tmp/output_img/%05d.png', './tmp/tmp.mp3', './result.mp4')
