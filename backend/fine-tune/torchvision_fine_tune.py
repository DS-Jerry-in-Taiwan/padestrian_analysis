import torch
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.datasets import CocoDetection
from torch.utils.data import DataLoader

def collate_fn(batch):
    return tuple(zip(*batch))

def convert_coco_target(target):
    # target: list of annotation dicts for一張圖
    boxes = []
    labels = []
    for obj in target:
        x, y, w, h = obj['bbox']
        boxes.append([x, y, x + w, y + h])
        labels.append(obj['category_id'])
    return {
        'boxes': torch.tensor(boxes, dtype=torch.float32),
        'labels': torch.tensor(labels, dtype=torch.int64)
    }

# set paths
data_dir = "/home/ubuntu/projects/pedestrian_attribute_recognition_30%/data"
train_ann_file = f"{data_dir}/CrowdHuman/crowdhuman/labels/coco/train.json"
val_ann_file = f"{data_dir}/CrowdHuman/crowdhuman/labels/coco/val.json"
train_img_dir = f"{data_dir}/CrowdHuman/crowdhuman/images/train/Images"
val_img_dir = f"{data_dir}/CrowdHuman/crowdhuman/images/val/Images"

# create dataset and dataloader
transform = transforms.Compose([
    transforms.ToTensor(),
])

train_dataset = CocoDetection(train_img_dir, train_ann_file, transform=transform)
val_dataset = CocoDetection(val_img_dir, val_ann_file, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=3, shuffle=True, collate_fn=collate_fn)
val_loader = DataLoader(val_dataset, batch_size=3, shuffle=False, collate_fn=collate_fn)


# Load a pre-trained model for evaluation
model = fasterrcnn_resnet50_fpn(weights="DEFAULT")

# modify class=2 (person) only
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, 2)

# device configuration
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

# Optimizer and learning rate sheduler
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)




# 訓練/驗證主流程
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for batch_idx, (images, targets) in enumerate(train_loader):
        images = [img.to(device) for img in images]
        targets = [convert_coco_target(t) for t in targets]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
        running_loss += losses.item()
        
        if (batch_idx + 1) % 10 == 0 or (batch_idx + 1) == len(train_loader):
            print(f"Epoch [{epoch+1}/{num_epochs}] Batch [{batch_idx+1}/{len(train_loader)}] Loss: {losses.item():.4f}")
        avg_loss = running_loss / len(train_loader)
        
    print(f"Epoch [{epoch+1}/{num_epochs}] Training Loss: {avg_loss:.4f}")
    lr_scheduler.step()


    # 驗證（簡單版）
    model.eval()
    with torch.no_grad():
        for images, targets in val_loader:
            images = [img.to(device) for img in images]
            outputs = model(images)
            # 可在此計算 mAP 或儲存推論結果

    print(f"Epoch {epoch+1} finished.")