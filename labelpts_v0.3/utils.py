import yaml
import os

def parse_cfg(cfg_file):
    if not os.path.exists(cfg_file):
        raise FileNotFoundError(f"Cfg file {cfg_file} does not exist")
    
    with open(cfg_file) as f:
        cfg = yaml.safe_load(f)

    file_dir = cfg.get('file_dir')
    if not file_dir:
        raise ValueError("file_dir not specified in cfg")
    
    cur_id = cfg.get('cur_id', 0)

    pts_num = cfg.get('max_pts_num', 0)

    lines = []
    for i, line_dict in enumerate(cfg['lines'].values()):
        start_id, end_id = tuple(int(c) for c in line_dict['id'].split(', '))
        color = line_dict['color']
        color = tuple(int(c) for c in color.split(', '))        
        line = [start_id, end_id, color]
        lines.append(line)

    return file_dir, cur_id, lines, pts_num

def get_pt_dis(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return abs(x1 - x2) + abs(y1 - y2)

if __name__ == '__main__':
    file_dir, cur_id, lines = parse_cfg('./cfg.yaml')
    print(file_dir, cur_id)
    for line in lines:
        print(line)