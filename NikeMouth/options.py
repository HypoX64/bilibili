import argparse

class Options():
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.initialized = False

    def initialize(self):
        self.parser.add_argument('-m','--media', type=str, default='./imgs/test.jpg',help='your image path or dir')
        self.parser.add_argument('-mode','--mode', type=str, default='all_face',help='all_face | only_mouth')
        self.parser.add_argument('-o','--output', type=str, default='image',help='output image or video')
        self.parser.add_argument('-t','--time', type=float, default=2.0,help='time of video')
        self.parser.add_argument('-f','--fps', type=float, default=25,help='fps of video')
        self.parser.add_argument('-s','--size', type=float, default=1.0,help='size of mouth')
        self.parser.add_argument('-i','--intensity', type=float, default=1.0,help='effect intensity')
        self.parser.add_argument('-a','--aspect_ratio', type=float, default=1.0,help='aspect ratio of mouth')
        self.parser.add_argument('-e','--ex_move', type=str, default='[0,0]',help='')
        self.parser.add_argument('-r','--result_dir', type=str, default='./result',help='')
        # self.parser.add_argument('--temp_dir', type=str, default='./tmp',help='')

        self.initialized = True

    def getparse(self):
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()

        self.opt.ex_move = eval(self.opt.ex_move)
        return self.opt

