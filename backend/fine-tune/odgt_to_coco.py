import json
from pathlib import Path
import argparse
from PIL import Image
import cv2
import numpy as np

def odgt_to_coco(odgt_path, images_dir, out_json):
    images = []
    annotations = []
    ann_id = 1
    img_id_map = {}
    img_size_map = {}
    with open(odgt_path, 'r', encoding='utf8') as f:
        for idx, line in enumerate(f):
            if not line.strip():
                continue
            item = json.loads(line)
            img_name = item['ID']
            # 如果 ID 沒有副檔名，可嘗試找檔案存在的副檔名
            img_path = None
            for ext in ('.jpg', '.png', '.jpeg'):
                p = Path(images_dir) / (img_name + ext)
                if p.exists():
                    img_path = str(p)
                    file_name = p.name
                    break
            if img_path is None:
                # 若 ID 已包含副檔名或是絕對路徑
                for ext in ('.jpg','.png','.jpeg'):
                    if img_name.endswith(ext):
                        file_name = Path(img_name).name
                        img_path = str(Path(images_dir) / img_name)
                        break
                else:
                    file_name = img_name
                    img_path = str(Path(images_dir) / img_name)
            img_id = idx + 1
            img_id_map[img_name] = img_id
            # 讀取圖片尺寸
            try:
                with Image.open(img_path) as im:
                    iw, ih = im.size
            except Exception:
                iw, ih = 0, 0
            img_size_map[img_id] = (iw, ih)
            images.append({"id": img_id, "file_name": file_name, "width": iw, "height": ih})
            for gt in item.get('gtboxes', []):
                fbox = gt.get('fbox')
                if not fbox: 
                    continue
                x, y, w, h = fbox
                bbox = [x, y, w, h]
                area = w * h
                ann = {
                    "id": ann_id,
                    "image_id": img_id,
                    "category_id": 1,    # 1 -> person
                    "bbox": bbox,
                    "area": area,
                    "iscrowd": 0,
                    "attributes": {}    # 可放額外欄位
                }
                annotations.append(ann)
                ann_id += 1
    coco = {
        "images": images,
        "annotations": annotations,
        "categories": [{"id": 1, "name": "person"}]
    }
    # 確保目標資料夾存在
    Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, 'w', encoding='utf8') as fo:
        json.dump(coco, fo, ensure_ascii=False, indent=2)
    print(f"Saved COCO json to {out_json}. images: {len(images)}, annotations: {len(annotations)}")
    return coco, img_size_map

if __name__ == "__main__":
    odgt_path = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data/CrowdHuman/crowdhuman/annotation_val.odgt"
    images_dir = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data/CrowdHuman/crowdhuman/images/val/Images"
    out_json = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data/CrowdHuman/crowdhuman/labels/coco/val.json"
    coco, img_size_map = odgt_to_coco(odgt_path, images_dir, out_json)

    # 打印部分結果並搭配圖片路徑
    print("\n--- COCO Annotation Summary ---")
    print(f"images: {len(coco['images'])}, annotations: {len(coco['annotations'])}, categories: {[c['name'] for c in coco['categories']]}")
    print("\n前3張圖片資訊：")
    for img in coco['images'][:3]:
        img_id = img.get('id')
        fname = img.get('file_name')
        w = img.get('width', '?')
        h = img.get('height', '?')
        img_path = str(Path(images_dir) / fname)
        boxes = [a for a in coco['annotations'] if a['image_id'] == img_id]
        print(f"Image id={img_id}, file={fname}, path={img_path}, size=({w}x{h}), #boxes={len(boxes)}")
        for a in boxes:
            bbox = a.get('bbox')
            cat = a.get('category_id')
            area = a.get('area')
            print(f"  bbox={bbox}, category={cat}, area={area}")

        # 用cv2畫出bbox並show
        if Path(img_path).exists():
            img_cv = cv2.imread(img_path)
            for a in boxes:
                x, y, bw, bh = map(int, a.get('bbox'))
                cv2.rectangle(img_cv, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
            cv2.imshow(f"Image id={img_id}", img_cv)
            cv2.waitKey(0)
            cv2.destroyAllWindows()