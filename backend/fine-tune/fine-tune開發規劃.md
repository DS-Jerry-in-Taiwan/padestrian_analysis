# 行人偵測模型 Fine-tune MVP 開發規劃（以 CrowdHuman 為例）

---

## 1. 資料集準備階段

### 目標
- 取得 CrowdHuman 資料集，並轉換為適合訓練的格式（如 YOLO 或 COCO）。

### Checklist
- [x] 申請並下載 CrowdHuman 資料集（images + 標註檔）
- [x] 解析 `.odgt` 標註格式，確認 `fbox` 為標註來源
- [x] 撰寫標註格式轉換腳本（轉為 YOLO txt 或 COCO json）
- [x] 整理訓練/驗證集資料夾結構（images/train, images/val, labels/train, labels/val）
- [x] 隨機劃分訓練/驗證集，確保場景多樣性
- [x] 檢查標註轉換正確性（隨機抽查標註與圖片對應）

## CrowdHuman 標註格式轉換與資料整理：開發工項

### 1. 解析 `.odgt` 標註檔
- 撰寫 Python 腳本，讀取並解析 CrowdHuman 的 `.odgt` 標註檔。
- 針對每張圖片，提取 `fbox`（full body bbox）資訊。

### 2. 標註格式轉換
- 將每張圖片的 bbox 轉換為 YOLO txt 或 COCO json 格式。
  - YOLO 格式：`class x_center y_center width height`（座標需歸一化）
  - COCO 格式：生成標準 COCO 格式的 json 標註檔

### 3. 資料夾結構整理
- 建立如下結構，將圖片與標註依訓練/驗證集分開存放：
dataset/ images/ train/ val/ labels/ train/ val/

### 4. 隨機劃分訓練/驗證集
- 撰寫腳本，將圖片隨機分配到 train/val，確保場景多樣性。

### 5. 標註轉換正確性檢查
- 隨機抽查部分圖片與標註，確認 bbox 與圖片對應正確。
- 可視化部分標註（畫框）以人工驗證。


### 代辦：
  #### 6. 文件與腳本整理
  - 撰寫 README 或說明文件，記錄轉換流程與注意事項。
  - 保存所有轉換與檢查腳本，方便重複執行。

---

如需 YOLO/COCO 轉換腳本範例、資料夾結構初始化腳本，請告知你要用哪一種格式，我可以直接產生對應程式碼！
---

## 2. 訓練流程設計階段

### 目標
- 建立可重複執行的 fine-tune 訓練流程。

## 2. 訓練流程設計階段：工項拆解

### 1. 選定訓練框架
- 決定使用 YOLOv8、torchvision、MMDetection 等其中一個作為 fine-tune 平台。

    ### torchvision fine-tune 工項

      1. 準備資料集
        - 確認 images/train、images/val 與對應標註（COCO 格式 json）已就緒。

      2. 撰寫 Dataset 與 DataLoader
        - 使用 torchvision.datasets.CocoDetection 或自訂 Dataset 讀取 COCO 格式標註。

      3. 選擇並初始化模型
        - 例如 torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        - 修改分類頭（num_classes=2，背景+person）

      4. 撰寫訓練主流程
        - 包含 optimizer、scheduler、訓練/驗證迴圈。

      5. 設定超參數
        - epochs、batch size、learning rate 等。

      6. 支援 resume/斷點訓練
        - 儲存/載入 checkpoint。

      7. 訓練過程保存最佳模型
        - 根據驗證集 mAP 或 loss 自動保存。

      8. 評估與可視化
        - 計算 mAP，並可視化部分推論結果。

### 2. 撰寫訓練腳本
- 撰寫包含資料載入（Dataset/DataLoader）、模型初始化、訓練主流程（train loop）的訓練腳本。

### 3. 設定分類頭
- 只偵測 person（設定類別數為 1，並對應標註格式）。

### 4. 設定訓練超參數
- 包含 epochs、batch size、learning rate、imgsz（輸入尺寸）等。

### 5. 支援 resume/斷點訓練
- 訓練過程可從中斷點繼續（儲存 checkpoint）。

### 6. 訓練過程中保存最佳模型權重
- 根據驗證集指標自動保存最佳模型。

### Checklist
- [ ] 選定訓練框架（YOLOv8 或 torchvision）
- [ ] 撰寫訓練腳本（含資料載入、模型初始化、訓練流程）
- [ ] 設定分類頭（只偵測 person）
- [ ] 設定訓練超參數（epochs, batch size, learning rate, imgsz）
- [ ] 支援 resume/斷點訓練
- [ ] 訓練過程中保存最佳模型權重

---

## 3. 評估與驗證階段

### 目標
- 客觀評估模型效果，確保達到 MVP 標準。

### Checklist
- [ ] 撰寫自動化評估腳本（計算 mAP、precision、recall）
- [ ] 用 CrowdHuman 驗證集進行評估
- [ ] 支援可視化推論結果（畫框、標註分數）
- [ ] 分析失敗案例（漏檢、誤檢）
- [ ] 記錄各階段指標（訓練 loss、驗證 mAP）

---

## 4. MVP 交付與優化階段

### 目標
- 交付可用的行人偵測模型，並規劃後續優化方向。

### Checklist
- [ ] 整理訓練與評估流程文件
- [ ] 保存最終模型權重與推論腳本
- [ ] 提供模型推論 API 或 demo
- [ ] 彙整失敗案例與改進建議
- [ ] 規劃下一步（如資料增強、混合自有資料、進階模型 backbone）

---

## 附註

- 每個階段完成後，務必進行 checklist 檢查，確保流程可複製、可驗證。
- 以 MVP 為目標，先達到「可用、可評估、可交付」，再逐步優化。

---

如需範例腳本、標註轉換工具或訓練/評估 pipeline 範本，請隨時提出！