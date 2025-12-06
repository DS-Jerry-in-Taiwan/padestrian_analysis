import json
from pathlib import Path
from PIL import Image
import os

def odgt_to_yolo(odgt_path, images_dir, labels_dir):
    """
    將 CrowdHuman 的 .odgt 標註轉換為 YOLO 格式，每張圖片產生一個 .txt 標註檔。
    """
    Path(labels_dir).mkdir(parents=True, exist_ok=True)
    with open(odgt_path, 'r', encoding='utf8') as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            img_name = item['ID']
            # 嘗試尋找圖片檔案
            img_path = None
            for ext in ('.jpg', '.png', '.jpeg'):
                p = Path(images_dir) / (img_name + ext)
                if p.exists():
                    img_path = str(p)
                    file_name = p.name
                    break
            if img_path is None:
                for ext in ('.jpg', '.png', '.jpeg'):
                    if img_name.endswith(ext):
                        file_name = Path(img_name).name
                        img_path = str(Path(images_dir) / img_name)
                        break
                else:
                    file_name = img_name
                    img_path = str(Path(images_dir) / img_name)
            # 取得圖片尺寸
            try:
                with Image.open(img_path) as im:
                    iw, ih = im.size
            except Exception:
                iw, ih = 0, 0
            # YOLO 標註檔案路徑
            label_path = Path(labels_dir) / (Path(file_name).stem + ".txt")
            with open(label_path, 'w', encoding='utf8') as lf:
                for gt in item.get('gtboxes', []):
                    fbox = gt.get('fbox')
                    if not fbox or iw == 0 or ih == 0:
                        continue
                    x, y, w, h = fbox
                    # 轉換為 YOLO 格式 (class x_center y_center width height)，且需歸一化
                    xc = x + w / 2
                    yc = y + h / 2
                    xc_n = xc / iw
                    yc_n = yc / ih
                    w_n = w / iw
                    h_n = h / ih
                    lf.write(f"0 {xc_n:.6f} {yc_n:.6f} {w_n:.6f} {h_n:.6f}\n")
    print(f"YOLO labels 已儲存於 {labels_dir}")

if __name__ == "__main__":
    odgt_path = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data/CrowdHuman/crowdhuman/annotation_val.odgt"
    images_dir = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data/CrowdHuman/crowdhuman/images/val/Images"
    labels_dir = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data/CrowdHuman/crowdhuman/labels/yolo/val"
    odgt_to_yolo(odgt_path, images_dir, labels_dir)