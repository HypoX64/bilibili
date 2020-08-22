# NikeMouth
[更多有趣的代码](https://github.com/HypoX64/bilibili)
## 入门
### 前提要求
* python3
* [ffmpeg](http://ffmpeg.org/)

### 依赖
代码依赖于 opencv-python, face_recognition, 可以通过 pip install安装
```bash
pip install opencv-python
pip install face_recognition
```
### 克隆这个仓库
```bash
git clone https://github.com/HypoX64/bilibili.git
cd bilibili/NikeMouth
```
### 运行程序
```bash
python main.py -m "图片的路径或目录"
```
<img src="./imgs/test.jpg" alt="image" style="zoom:25%;" /> <img src="./imgs/test_out.jpg" alt="image" style="zoom:25%;" /><br>

## 更多的参数

|    选项    |        描述         |                 默认值                 |
| :----------: | :------------------------: | :-------------------------------------: |
|  -m | 图片的路径或目录 |                    './imgs/test.jpg'                    |
| -mode | 改变的模式，all_face　or  only_mouth | all_face |
|    -o    |    输出视频或图片image or video    |       image |
| -r | 结果储存的目录 | ./result |
| -i | 变换强度 |             1.0          |

