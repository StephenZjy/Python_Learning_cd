import os.path
import shutil

import cv2
from csv_operator import write_points

def draw_pts_im(im, pts, color = (130, 139, 0)):
    for pt in pts:
        x, y = list(map(int, pt))
        cv2.circle(im, (x, y), 3, color, 2)
    return im

def draw_lines_im(im, lines, line_colors):
    for line, color in zip(lines, line_colors):
        pt1, pt2 = line
        x1, y1 = list(map(int, pt1))
        x2, y2 = list(map(int, pt2))
        cv2.line(im, (x1, y1), (x2, y2), color, 2)
    return im

def get_lines_from_pts(pts, line_info):
    length = len(pts)
    lines = []
    line_colors = []
    if length > 1:
        for i in range(length-1):
            id01, id02, color = line_info[i]
            line = pts[id01], pts[id02]
            lines.append(line)
            line_colors.append(color)
    return lines, line_colors


def draw_pts(image_file, pts, line_info):
    im = cv2.imread(image_file)
    if pts:
        lines, line_colors = get_lines_from_pts(pts, line_info)
        im = draw_lines_im(im, lines, line_colors)
        im = draw_pts_im(im, pts)
    return im 

def change_page(key, cur_id, min_id, max_id):
    if key == 97: # A
        cur_id = max(min_id, cur_id - 1)
    if key == 100: # D
        cur_id = min(max_id, cur_id + 1)
    if key == 98: # A
        cur_id = max(min_id, cur_id - 50)
    if key == 114: # D
        cur_id = min(max_id, cur_id + 50)
    return cur_id

def keyboard_events(key, pts, pts_file, cur_id, min_id, max_id):
    is_exit = False
    # 翻页 A, B, D, R
    if key in [97, 98, 114]:
        cur_id = change_page( key, cur_id, min_id, max_id)
        write_points(pts, pts_file)

    if key in [100]:
        cur_id = change_page(key, cur_id, min_id, max_id)
        write_points(pts, pts_file)
        next_pts_file = pts_file.replace(f"{cur_id -1}.csv", f"{cur_id}.csv")
        if not os.path.exists(next_pts_file):
            shutil.copy(pts_file, next_pts_file)
    
    # 删除
    if key == 255:
        if pts:
            pts.pop()

    if key == 122:
        if pts:
            pts.clear()

     # 退出
    if key == 27:
        is_exit = True

    
    return pts, cur_id, is_exit