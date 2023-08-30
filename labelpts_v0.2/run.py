
from utils import parse_cfg, get_pt_dis
from file_operator import load_files
from csv_operator import read_points, write_points
from cv_operator import draw_pts, keyboard_events
import cv2
import yaml


class PtsLabel(object):
    def __init__(self, cfg_file) -> None:
        super(PtsLabel, self).__init__()
        self.parse_cfg(cfg_file)
        self.init_cv()
        self.init_images()
        self.first_read = True
        self.cfg_file = cfg_file

        self.choose_pt_id = -1
        self.is_selecting_all = False

    def init_images(self):
        self.images_files = load_files(self.file_dir, file_type='png')
        if not self.images_files:
            raise FileNotFoundError(' no images!')
        self.min_id = 0
        self.max_id = len(self.images_files) - 1
        print(self.cur_id, self.max_id)
    
    def init_cv(self):
        self.window = cv2.namedWindow("image", 0)
        #cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
        cv2.setMouseCallback("image", self.on_EVENT_LBUTTONDOWN)
    
    def parse_cfg(self, cfg_file):
        self.file_dir, self.cur_id, self.line_info, self.max_pts_num = parse_cfg(cfg_file)
    
    def get_min_distance(self, x, y):
        id = 0
        distance = 9999
        for idx, pt in enumerate(self.pts):
            dis = get_pt_dis(pt, (x,y))
            if dis < distance:
                distance = dis
                id = idx
        return id, distance
    
    # 鼠标事件
    def on_EVENT_LBUTTONDOWN(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # 判断距离 近：选中点 远：增加点
            id, distance = self.get_min_distance(x, y)
            if distance < 20:
                self.choose_pt_id = id
            else:
                if len(self.pts) < self.max_pts_num:
                    self.pts += [[x, y]]
            
        if event == cv2.EVENT_MOUSEMOVE:
            # 如果是选中状态 放下点
            if self.choose_pt_id != -1:
                self.pts[self.choose_pt_id] = [x, y]

            if self.is_selecting_all:  # 新增的移动所有点逻辑
                for idx, pt in enumerate(self.pts):
                    self.pts[idx] = [x - self.selected_pts_offset[0][idx], y - self.selected_pts_offset[1][idx]]

        if event == cv2.EVENT_LBUTTONUP:
            if self.choose_pt_id != -1:
                self.choose_pt_id = -1

            if self.is_selecting_all:
                self.is_selecting_all = False

        if event == cv2.EVENT_LBUTTONDBLCLK:  # 新增的双击事件逻辑
            self.choose_pt_id = -1
            self.is_selecting_all = True
            self.selected_pts_offset = [x - pt[0] for pt in self.pts], [y - pt[1] for pt in self.pts]

    def update_cfg(self):
        with open(self.cfg_file) as f:
            cfg = yaml.safe_load(f)
            cfg['cur_id'] = self.cur_id
        
        with open(self.cfg_file, 'w') as f:
            yaml.dump(cfg, f) 



    def run(self):
        is_exit = False
        while is_exit == False:
            image_file = self.images_files[self.cur_id]
            pts_file = image_file.replace('png', 'csv')
            if self.first_read == True:
                self.pts = read_points(pts_file)
                self.first_read = False
            img = draw_pts(image_file, self.pts, self.line_info)
            cv2.imshow("image", img)
            key = cv2.waitKey(1)
            self.pts, cur_id, is_exit = keyboard_events(key, self.pts, pts_file, self.cur_id, self.min_id, self.max_id)
            if cur_id != self.cur_id:
                self.cur_id = cur_id
                self.first_read = True
                self.update_cfg()
                print(self.cur_id, self.max_id)


if __name__ == '__main__':
    cfg_file = './cfg.yaml'
    pts_label = PtsLabel(cfg_file)
    pts_label.run()