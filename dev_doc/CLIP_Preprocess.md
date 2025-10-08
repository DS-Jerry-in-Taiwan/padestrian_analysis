根據你目前的 `CLIPImagePreprocessor` 代碼與前述開發規劃，這部分的每個階段目標與步驟如下：

---

### 階段目標

1. **設計統一的影像前處理類接口**
   - 目標：所有影像前處理類都需繼承 `BaseImagePreprocessor`，統一接口，方便管理與擴充。

2. **實作 CLIPImagePreprocessor**
   - 目標：實現符合 CLIP 模型需求的影像前處理流程，包括 resize、normalize、格式轉換，並支援單張與批次處理。

3. **嚴謹的例外處理**
   - 目標：對輸入型態、shape、通道數進行檢查，遇到不符時拋出明確錯誤。

4. **標準化與格式轉換**
   - 目標：將影像數值正規化，並轉換為深度學習常用的 CHW 格式。

---

### 階段步驟

#### 1. 設計與繼承
- 定義 `BaseImagePreprocessor` 抽象基底類。
- `CLIPImagePreprocessor` 繼承基底類，實作必要方法。

#### 2. 初始化參數
- 在 `__init__` 設定輸出尺寸（size）、標準化均值（mean）、標準差（std）。
- 參數預設為 CLIP 官方推薦值。

#### 3. 單張影像處理（`__call__`）
- 檢查輸入型態（PIL.Image 或 numpy.ndarray）。
- 若為 numpy，轉為 PIL.Image。
- 轉為 RGB，resize 成指定尺寸。
- 轉為 numpy 陣列並縮放到 [0, 1]。
- 檢查通道數是否為 3。
- 用 mean/std 進行標準化（廣播處理）。
- 轉換為 CHW 格式。
- 回傳處理後的 numpy 陣列。

#### 4. 批次處理（`batch_preprocess`）
- 接收多張影像（list），逐張呼叫 `__call__`。
- 回傳所有處理後的 numpy 陣列 list。

#### 5. 例外處理
- 輸入型態錯誤、shape 不符、通道數不符時，拋出 ValueError。

#### 6. 文件與型別提示
- 為類別與方法加上 docstring、型別提示，說明用途、參數、回傳型態與例外狀況。

---

如需針對每個階段展開細節或補充範例，請告知！