import os
import cv2
import numpy as np

import sys
sys.path.append("..")
from Util import util,ffmpeg


# 用校徽看badapple
imgs_dir = './pixel_imgs/university/base'
highlight_dir = './pixel_imgs/university/highlight'
background_dir = './pixel_imgs/university/background'
cut_size = 79
pixel_resize = 0 # resize pixel_imgs, if 0, do not resize
output_pixel_num = 18 # how many pixels in the output video'width 
video_path = '../Video/素材/bad_apple_bbkkbk/BadApple.flv'
change_frame = 2
# ------------------------- Load Blocks -------------------------
pixels = []
img_names = os.listdir(imgs_dir)
img_names.sort()
for name in img_names:
    img = cv2.imread(os.path.join(imgs_dir,name))
    for h in range(img.shape[0]//cut_size):
        for w in range(img.shape[1]//cut_size):  
            pixel = img[h*cut_size:(h+1)*cut_size,w*cut_size:(w+1)*cut_size]      
            if pixel_resize != 0:
                pixel = cv2.resize(pixel,(pixel_resize,pixel_resize),interpolation=cv2.INTER_AREA)
            pixels.append(pixel)
pixel_size = pixels[0].shape[0]

# highlight
img_names = os.listdir(highlight_dir)
img_names.sort()
for name in img_names:
    pixel = cv2.imread(os.path.join(highlight_dir,name))
    pixel = cv2.resize(pixel,(pixel_size,pixel_size),interpolation=cv2.INTER_AREA)
    for i in range(10):
        pixels.append(pixel)

pixels = np.array(pixels)


# background
background_name = os.listdir(background_dir)[0]
background = cv2.imread(os.path.join(background_dir,background_name))
background = cv2.resize(background,(pixel_size,pixel_size),interpolation=cv2.INTER_AREA)


# ------------------------- Prcessing Video -------------------------
fps,endtime,height,width = ffmpeg.get_video_infos(video_path)
scale = height/width

util.clean_tempfiles(False)
util.makedirs('./tmp/vid2img')
util.makedirs('./tmp/output_img')
ffmpeg.video2image(video_path, './tmp/vid2img/%05d.png')
ffmpeg.video2voice(video_path, './tmp/tmp.mp3')

# ------------------------- Video2Block -------------------------
print('Video2Block...')
img_names = os.listdir('./tmp/vid2img')
img_names.sort()
frame = 0
for img_name in img_names:
    img = cv2.imread(os.path.join('./tmp/vid2img',img_name))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (output_pixel_num,int(output_pixel_num*scale)),interpolation=cv2.INTER_AREA)
    
    h,w = img.shape
    if frame %change_frame == 0:
        indexs = np.random.randint(0, pixels.shape[0]-1, (h,w))
    out_img = np.zeros((h*pixel_size,w*pixel_size,3), dtype = np.uint8)
    for i in range(h):
        for j in range(w):
            #index = np.clip(img[i,j]//level,0,len(pixels)-1)
            if img[i,j] < 64:
                out_img[i*pixel_size:(i+1)*pixel_size,j*pixel_size:(j+1)*pixel_size] = pixels[indexs[i,j]]
            else:
                out_img[i*pixel_size:(i+1)*pixel_size,j*pixel_size:(j+1)*pixel_size] = background

    out_img = out_img[:(h*pixel_size//2)*2,:(w*pixel_size//2)*2]
    cv2.imwrite(os.path.join('./tmp/output_img',img_name), out_img)
    frame += 1
# ------------------------- Block2Video -------------------------
ffmpeg.image2video(fps, './tmp/output_img/%05d.png', './tmp/tmp.mp3', './result.mp4')
