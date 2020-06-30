# OneImage2Video
用一个或一些图片生成视频<br>

## 入门
### 前提要求
* Linux or Windows
* python3
* [ffmpeg](http://ffmpeg.org/)
```bash
sudo apt-get install ffmpeg
```
### 依赖
代码依赖于 opencv-python, 可以通过 pip install安装
```bash
pip install opencv-python
```
### 克隆这个仓库
```bash
git clone https://github.com/HypoX64/bilibili.git
cd bilibili/OneImage2Video
```
### 运行程序
* 在main.py中修改你的视频路径以及图片路径
```python
# 在github看香蕉君
# pixel_imgs_dir = './pixel_imgs/github'
# pixel_imgs_resize = 0 # resize pixel_imgs, if 0, do not resize
# output_pixel_num = 52 # how many pixels in the output video'width 
# video_path = '../Video/素材/香蕉君/香蕉君_3.mp4'
# inverse = False
```
* run
```bash
python main.py
```


