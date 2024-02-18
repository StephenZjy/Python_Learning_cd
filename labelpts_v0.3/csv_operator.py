import csv
import os

def read_points(csv_file):
    points = []
    if os.path.exists(csv_file):
        with open(csv_file) as f:
            reader = csv.reader(f)
            for row in reader:
                id, x, y = row
                points.append((float(x)*1024, float(y)*1024))
    return points

def write_points(points, csv_file):
    if not points:
        return
    with open(csv_file, 'w') as f:
        writer = csv.writer(f)
        for i, point in enumerate(points):
            writer.writerow([i, point[0]/1024, point[1]/1024])