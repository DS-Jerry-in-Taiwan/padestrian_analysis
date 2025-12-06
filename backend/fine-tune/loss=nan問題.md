你的 loss 變成 `nan`，這是訓練過程中常見的問題，通常有以下幾個主因：

---

## 1. **標準化（Normalize）導致數值爆炸**
你用了：
```python
transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
```
這是正確的，但**如果你的圖片本身不是 0~1 的 float tensor**，而是 0~255 的 uint8，這樣標準化會導致數值異常，進而讓 loss 變成 nan。

**解法：**  
- 確認 `transforms.ToTensor()` 一定要放在 `Normalize` 前面（你已經正確）。
- 確認圖片沒有損壞或格式異常。

---

## 2. **學習率過高**
- 你的學習率設為 `0.005`，對小資料集或小模型來說可能太高，容易導致 loss 爆炸變 nan。

**解法：**  
- 嘗試把學習率調低，例如 `0.001` 或 `0.0005`。

---

## 3. **訓練資料有異常（如 bbox 為負、標註錯誤）**
- 如果有 bbox 為負數、無效標註、空標註等，也會導致 loss nan。

**解法：**  
- 檢查你的 COCO 標註檔，確保 bbox 坐標與寬高都大於 0。
- 可以在 `convert_coco_target` 過濾掉寬高小於等於 0 的 bbox。

---

## 4. **資料增強或 resize 導致 bbox 無效**
- 如果 resize 後 bbox 超出圖片範圍，也可能導致 loss nan。

**解法：**  
- 確認 resize 後 bbox 還在圖片範圍內。

---

## 5. **模型初始化異常**
- 若模型分類頭未正確初始化，也可能導致 loss nan。

**你目前的初始化方式正確。**

---

## 建議你先這樣調整：

1. **降低學習率**  
   ```python
   optimizer = torch.optim.SGD(params, lr=0.001, momentum=0.9, weight_decay=0.0005)
   ```

2. **在 `convert_coco_target` 過濾無效 bbox**  
   ```python
   def convert_coco_target(target):
       boxes = []
       labels = []
       for obj in target:
           x, y, w, h = obj['bbox']
           if w > 0 and h > 0:
               boxes.append([x, y, x + w, y + h])
               labels.append(obj['category_id'])
       return {
           'boxes': torch.tensor(boxes, dtype=torch.float32),
           'labels': torch.tensor(labels, dtype=torch.int64)
       }
   ```

3. **訓練前檢查資料**  
   - 隨機取一張圖，印出其 bbox，確認都合理。

---

### 小結

- nan loss 通常是學習率過高、標註異常或標準化順序錯誤造成。
- 先降低學習率、過濾無效 bbox，再觀察 loss 是否正常。

如需 debug 輸出或進一步協助，請隨時告訴我！