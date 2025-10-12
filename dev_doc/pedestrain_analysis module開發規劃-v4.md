以下是行人偵測與屬性分析模組化開發的步驟清單與各階段 checklist：

---

## 行人偵測與屬性分析模組化開發步驟

### 1. 專案初始化與目錄結構確認
- [x] 建立專案目錄與基本結構
- [x] 建立 `requirements.txt` 與 `README.md`
- [x] 初始化 Git 版本控管

---

### 2. 資料前處理工具設計（`utils/`）

#### 工作目標
- 建立可重複使用的前處理工具，支援行人偵測與屬性分析任務。
- 確保資料格式一致、標註解析正確，並具備基本資料增強能力。
- 提供單元測試，確保工具穩定可靠。

#### 2.1 前處理中介層（PreprocessManager/Adapter）
 設計統一入口的 PreprocessManager 類，支援影像/文字/其他型態的前處理。
 定義統一 API（如 preprocess(data, mode='auto')）。
 支援外部注入與自動分流。

   ##### 1. 明確需求與接口設計
   - 目標：設計一個統一入口的 PreprocessManager 類，支援影像、文字、其他型態的前處理。
   - 介面：`preprocess(data, mode='auto')`，根據資料型態自動分流。
   - 支援外部注入底層前處理類（如 image_preprocessor, text_tokenizer）。

   ---

   ### 2. 設計 PreprocessManager 類別骨架
   - 定義初始化方法，支援註冊/注入底層前處理類。
   - 定義 `preprocess` 方法，根據 mode 或資料型態自動分流。
   - 預留註冊/工廠機制（如 registry dict）。

   ---

   ### 3. 實作自動分流邏輯
   - 根據輸入資料型態（如 numpy array、PIL Image、str、list），自動選擇對應的底層前處理類。
   - 支援 mode 參數強制指定處理型態（如 mode='image'、mode='text'）。

   ---

   ### 4. 支援外部注入與擴充
   - 支援外部傳入自訂的 image_preprocessor、text_tokenizer。
   - 預留註冊新型態前處理類的介面（如 register_preprocessor）。

   ---

   ### 5. 定義底層前處理類的統一接口
   - 規範所有底層前處理類都要有 `__call__` 或 `process` 方法，方便 PreprocessManager 調用。

   ---

   ### 6. 單元測試與驗證
   - 測試影像、文字、未知型態的自動分流與處理。
   - 測試外部注入與註冊新前處理類的功能。

   ---

   ### 7. 文件與型別提示
   - 為類別與方法加上 docstring、型別提示，說明用途與參數。

#### 2.2 Registry/Factory 機制
 實作 registry（註冊表）與工廠模式，管理所有底層前處理類。
 提供 decorator 或註冊函數，方便擴充新型態/新模型。

   ##### 1. 階段目標
   - 建立統一的 registry（註冊表）與工廠模式，集中管理所有底層前處理類（如影像、文字、音訊等）。
   - 提供 decorator 或註冊函數，讓新型態/新模型的前處理類能方便擴充與自動註冊。
   - 讓 PreprocessManager 或其他模組能根據名稱或型態自動取得對應的前處理類，提升模組化與可維護性。


   ##### 2. 階段工項

   **設計 registry 結構**
      -[x] 建立全域或模組級的 registry dict，儲存所有前處理類的名稱與對應類別/實例。

   **實作註冊 decorator 或函數**
      -[x] 提供 `@register_preprocessor(name)` decorator 或 `register_preprocessor(name, cls)` 函數，讓新前處理類可自動註冊到 registry。

   **設計工廠方法**
      -[x] 實作 `get_preprocessor(name, **kwargs)` 工廠函數，根據名稱動態建立或取得對應的前處理類。
      開發步驟
         1. 設計 registry 結構
            - registry 可存放類別或實例。
               **實作工廠函數 get_preprocessor(name, kwargs)
         2. 先從 registry 取得物件。
            - 判斷是類別還是實例：
               若是類別，則用 **kwargs 初始化並回傳新實例。
               若是實例，則直接回傳。
         3. 型別提示與註解
            - 為工廠函數加上 docstring 與型別提示。
         4. 單元測試
            - 測試取得類別、取得實例、傳入初始化參數等情境。

   **整合至 PreprocessManager**
      -[x] 讓 PreprocessManager 能透過 registry/factory 取得並調用對應的前處理類，支援自動分流與擴充。

      開發步驟
         1. 在 PreprocessManager 中引入 registry 的工廠方法

         2. import get_preprocessor（以及 registry dict）到 PreprocessManager。
         修改 preprocess 方法分流邏輯

         3. 當 mode 不是 image/text 或 auto 判斷不到型態時，嘗試從 registry 取得對應的前處理類並調用。
         支援自動分流與擴充

         4. 讓使用者可直接用 mode 指定新型態（如 'audio'、'video'），PreprocessManager 自動查詢 registry 並調用。
         型別提示與註解

         為方法加上 docstring、型別提示，說明用途與參數。

   **單元測試與驗證**
      -[x] 測試註冊、查詢、動態建立、分流等功能，確保 registry/factory 機制穩定可靠。

   **文件與型別提示**
      -[x] 為 registry、decorator、工廠方法加上 docstring 與型別提示，說明用途與參數。
---

#### 2.3 底層前處理類
 影像前處理類（如 CLIPImagePreprocessor、ViTImagePreprocessor）
 文字前處理類（如 CLIPTextTokenizer、OpenCLIPTextTokenizer）
 支援批次與單張處理、例外處理、標準化輸出

   ---

   #### 1. 階段目標

   - 建立可擴充的影像與文字前處理類（如 `CLIPImagePreprocessor`、`ViTImagePreprocessor`、`CLIPTextTokenizer`、`OpenCLIPTextTokenizer`）。
   - 規範所有前處理類的統一接口（如 `__call__` 或 `process` 方法），方便 PreprocessManager 調用。
   - 支援批次與單張資料處理，例外處理（如格式錯誤、空資料），並保證標準化輸出格式（如 numpy array、token ids）。
   - 方便後續擴充新模型或新型態前處理類。

   ---


   #### 2. 階段工項

   1. **設計抽象基底類別**
      - 定義 `ImagePreprocessorBase`、`TextTokenizerBase` 等抽象類，規範所有前處理類必須實作的接口（如 `__call__`、`process`）。
      - 加入型別提示與 docstring。
      ---
      #### 1. 明確需求與接口規範
      - 目標：建立統一的影像與文字前處理抽象基底類別，規範所有前處理類的接口。
      - 所有底層前處理類都需繼承這些基底類，並強制實作指定方法（如 `__call__`、`process_batch`）。

      ---

      #### 2. 選擇抽象類設計方式
      - 使用 Python 標準庫 `abc`（Abstract Base Class）與 `@abstractmethod`，強制子類必須實作接口。

      ---

      #### 3. 類別骨架設計
      - 定義 `ImagePreprocessorBase`、`TextTokenizerBase` 等抽象類。
      - 規範必須實作的方法（如 `__call__`、`process_batch`）。
      - 可選擇性提供預設方法（如批次處理可預設呼叫單張處理）。

      ---

      #### 4. 型別提示與 docstring
      - 為類別與方法加上型別提示，提升可讀性與靜態檢查效果。
      - 詳細撰寫 docstring，說明用途、參數、回傳型態與例外狀況。

      ---

      #### 5. 單元測試
      - 測試繼承基底類時，若未實作抽象方法會報錯。
      - 測試正確繼承與覆寫時能正常運作。

      ---

      #### 6. 文件補充
      - 在專案文件或 README 中說明抽象基底類的設計理念與使用方式。

      ---

   2. **實作影像前處理類**
      - 實作 `CLIPImagePreprocessor`、`ViTImagePreprocessor` 等，支援 resize、normalize、格式轉換。
      - 支援單張與批次處理（如 `__call__(self, image)`、`process_batch(self, images)`）。
      - 例外處理：格式錯誤、尺寸不符時拋出明確錯誤。

         #### 1. 明確需求與接口設計
         - 目標：實作 `CLIPImagePreprocessor`、`ViTImagePreprocessor` 等影像前處理類，支援 resize、normalize、格式轉換。
         - 所有類需繼承 `BaseImagePreprocessor`，統一實作 `__call__`（單張）與 `batch_preprocess`（批次）方法。

         ---

         #### 2. 選擇影像處理庫
         - 建議使用 Pillow（PIL）、numpy，必要時可用 torchvision。

         ---

         #### 3. 類別骨架設計
         - 定義建構子（`__init__`）支援目標尺寸、normalize 參數等。
         - 實作 `__call__` 方法：單張影像 resize、normalize、格式轉換。
         - 實作 `batch_preprocess` 方法：批次處理，呼叫單張方法。

         ---

         #### 4. 例外處理
         - 檢查輸入型態（如 PIL.Image、numpy.ndarray），型態錯誤時拋出 ValueError。
         - 檢查尺寸、格式，錯誤時拋出明確錯誤。

         ---

         #### 5. 標準化輸出
         - 輸出統一為 numpy array（或 torch tensor，視需求）。
         - 文件註解說明輸出格式。

         ---

         #### 6. 單元測試
         - 測試正常情境（單張/批次）、異常情境（型態錯誤、尺寸不符）、normalize 參數等。

         ---

         #### 7. 文件與型別提示
         - 為類別與方法加上 docstring、型別提示，說明用途、參數、回傳型態與例外狀況。


   3. **實作文字前處理類**
      - 實作 `CLIPTextTokenizer`、`OpenCLIPTextTokenizer` 等，支援分詞、編碼、padding。
      - 支援單句與批次處理（如 `__call__(self, text)`、`process_batch(self, texts)`）。
      - 例外處理：空字串、非法字元時拋出明確錯誤。

   4. **標準化輸出格式**
      - 規範所有前處理類的輸出格式（如影像回傳 numpy array，文字回傳 token ids 或 tensor）。
      - 文件註解說明各類型的標準化格式。

   5. **單元測試**
      - 覆蓋單張、批次、例外情境，確保前處理類穩定可靠。

   6. **文件與型別提示**
      - 為所有類別與方法加上 docstring、型別提示，說明用途、參數、回傳型態與例外狀況。

   ---


#### 2.4 單元測試
 覆蓋中介層、registry、底層類的主要功能

#### 工作流程與步驟
1. **資料集格式分析與規劃**
   - 確認原始資料集格式（如影像檔案、標註檔案結構）。
   - 設計統一的資料結構（如 class 或 dict），方便後續處理。
##### 工作內容
    - 確認原始資料集格式（如影像檔案、標註檔案結構）。
    - 盤點資料來源（公開資料集、自建資料集）。
    - 分析標註檔案格式（COCO、VOC、CSV、JSON 等）。
    - 設計統一的資料結構（如 Python class 或 dict），方便後續處理。
    - 規劃資料夾結構與命名規則。
#### 1. 資料集格式分析與規劃 Checklist
- [x] 盤點資料來源
- [x] 確認影像與標註檔案格式
- [x] 分析標註檔案內容
- [x] 設計統一資料結構
- [x] 規劃資料夾結構與命名規則

2. **影像讀取與預處理函式**
   - 實作影像讀取（支援 jpg/png 等格式）。
   - 實作影像 resize、normalize 等預處理方法。
   - 支援批次處理與單張處理。

##### 工作內容
- 實作影像讀取（支援 jpg/png 等格式）。
- 實作影像 resize、normalize 等預處理方法。
- 支援批次處理與單張處理。

#### 開發工項
- 實作影像讀取函式（支援 jpg/png，單張/批次）
   1. 明確需求：支援 jpg/png 格式，能讀取單張或多張影像檔案。
   2. 選擇影像處理庫：推薦使用 Pillow（PIL）、OpenCV 或 torchvision。
   3. 設計 API：
      - 單張讀取：`read_image(path)`
      - 批次讀取：`read_images(list_of_paths)`
   4. 處理格式判斷：自動判斷檔案格式，支援 jpg/png。
   5. 例外處理：檔案不存在、格式錯誤時回傳錯誤訊息或跳過。
   6. 回傳標準化資料結構：如 numpy array 或 PIL Image。
   7. 單元測試：覆蓋正常、異常、批次、空列表等情境。
   8. 文件註解：說明函式用途、參數、回傳型態與例外狀況。

- 實作影像 resize 方法（可自訂目標尺寸）
   1. 明確需求：支援將影像調整為指定尺寸（如 224x224），可選擇插值方式。
   2. 選擇影像處理庫：推薦使用 Pillow（PIL）、OpenCV 或 torchvision。
   3. 設計 API：
      - 單張 resize：`resize_image(image, size, interpolation)`
      - 批次 resize：`resize_images(list_of_images, size, interpolation)`
   4. 支援多種插值方式：如 PIL 的 `Image.BILINEAR`、`Image.NEAREST`、`Image.LANCZOS`。
   5. 例外處理：輸入非影像物件、尺寸格式錯誤時回傳錯誤訊息或跳過。
   6. 回傳標準化資料結構：如 PIL Image 或 numpy array。
   7. 單元測試：覆蓋正常、異常、批次、空列表、不同插值等情境。
   8. 文件註解：說明函式用途、參數、回傳型態與例外狀況。


- 實作影像 normalize 方法（標準化像素值，支援多種模式）
   1. 明確需求：將影像像素值標準化，支援多種模式（如 0~1、-1~1、均值/標準差正規化）。
   2. 選擇影像處理庫：推薦使用 numpy、Pillow（PIL）、torchvision。
   3. 設計 API：
      - 單張 normalize：`normalize_image(image, mode, mean=None, std=None)`
      - 批次 normalize：`normalize_images(list_of_images, mode, mean=None, std=None)`
   4. 支援多種模式：
      - min-max 標準化（0~1）
      - 均值/標準差正規化（(x-mean)/std）
      - -1~1 標準化
      - 自訂 mean/std
   5. 例外處理：輸入非影像物件、模式錯誤、mean/std 格式錯誤時回傳錯誤訊息或跳過。
   6. 回傳標準化資料結構：如 numpy array 或 torch tensor。
   7. 單元測試：覆蓋正常、異常、批次、空列表、不同模式等情境。
   8. 文件註解：說明函式用途、參數、回傳型態與例外狀況。

- 前處理流程可組合（如 compose，方便串接多步驟）
- 支援例外處理（檔案不存在、格式錯誤等）
- 單元測試覆蓋主要工具函式（各種輸入情境）


##### Checklist
- [x] 影像讀取函式（單張/批次）
- [x] 影像 resize 方法
- [x] 影像 normalize 方法
- [x] 前處理流程可組合（如 compose）
- [x] 支援例外處理（檔案不存在、格式錯誤等）


#### Checklist
- [x] 資料集格式分析與規劃
- [x] 影像讀取與預處理函式



#### 待優化方向
   3. **標註檔解析工具**
      - 解析標註檔（如 COCO、VOC、CSV、JSON 等格式）。
      - 將標註轉換為統一格式（如 bounding box、屬性標籤）。
   4. **資料增強（Augmentation）模組**
      - 實作常用增強方法（如隨機翻轉、裁剪、亮度調整）。
      - 可選用第三方套件（如 albumentations、torchvision transforms）。
   5. **單元測試覆蓋主要工具函式**
      - 為每個工具函式撰寫測試案例。
      - 確保各種輸入情境下都能正確處理。


#### Checklist
- [ ] 標註檔解析工具
- [ ] 資料增強（Augmentation）模組
- [ ] 單元測試覆蓋主要工具函式


---

## 3. 模型架構設計與實作（models）

### 階段目標
- 建立可擴充、模組化的模型架構，支援行人偵測與屬性分析兩大任務。
- 提供統一接口，方便串接訓練、推論、API 與多種屬性分析方法（label-based、prompt-based）。
- 讓主流程能以最小可行架構完成「影像→偵測→屬性分析→結果」的自動化處理。

---

### 開發工項

1. **行人偵測模型 class（如 YOLO, Faster R-CNN）**
   - 實作行人偵測模型 class，支援 `detect(image)` 介面，回傳 bounding boxes、信心分數等。
   - 可先用預訓練模型或 stub。

      ### 開發步驟

      1. **需求明確化**
         - 介面：`detect(image)`，輸入單張影像（numpy array 或 tensor），回傳 bounding boxes、scores（可選：labels）。
         - 輸出格式建議：`List[Dict]`，每個 dict 包含 box、score、label。

      2. **選擇實作方式**
         - MVP 階段建議直接用 torchvision 預訓練 Faster R-CNN 或 YOLOv5（ultralytics/yolov5）。
         - 若無 GPU 或只需 stub，可先寫一個隨機產生 box 的 mock class。

      3. **設計偵測模型基礎 class**
         - 例如 `PedestrianDetector`，封裝模型初始化、前處理、推論、後處理。

      4. **實作 detect 方法**
         - 包含：影像前處理（如 resize/normalize）、模型推論、後處理（如 NMS、格式轉換）。

      5. **測試與驗證**
         - 用一張測試圖檔驗證 detect 輸出格式正確。
         - 可寫簡單單元測試：輸入隨機圖，檢查回傳型態與欄位。


      #### 待優化方向
      6. **可選：支援 batch detect**
         - 若有需求，可擴充支援多張影像 batch 偵測。

2. **屬性分析基底類別（`AttributeAnalyzerBase`，統一接口）**
   - 定義抽象基底類別，規範屬性分析器的統一接口（如 `analyze(image, boxes)`）。
   - 方便後續擴充 label-based、prompt-based 兩種分析器。

   屬性分析基底類別（`AttributeAnalyzerBase`）的開發步驟如下：

   ---

   ### AttributeAnalyzerBase 開發步驟

   ```
   AttributeAnalyzerBase（屬性分析基底類別）是一個「抽象基底類別」，用來規範所有「行人屬性分析器」的統一接口。
   它的主要用途是：

   統一所有屬性分析器的寫法與用法，讓主流程或 API 可以用同一種方式呼叫不同的屬性分析器（如 label-based、prompt-based）。
   強制所有子類都要實作 analyze(image, boxes) 方法，確保每個分析器都能針對影像與偵測到的 bounding boxes 回傳屬性分析結果。
   方便後續擴充、維護與替換分析器，不用改動主流程。
   簡單來說：
   它是「所有屬性分析器的共同規格」，讓你可以 plug-and-play 不同分析器，主程式不用管底層細節，只要呼叫 analyze 就能取得每個 box 的屬性結果。
   ```
   1. **明確需求與接口設計**
      - 目標：定義一個抽象基底類別，規範所有屬性分析器的統一接口。
      - 主要方法：`analyze(image, boxes)`，輸入影像與偵測到的 bounding boxes，回傳每個 box 的屬性分析結果。
      - 可擴充性：方便後續繼承（如 label-based、prompt-based 分析器）。

   2. **選擇繼承方式**
      - 建議使用 Python 標準庫 `abc`（Abstract Base Class）來定義抽象方法，強制子類必須實作。

   3. **實作基底類別**
      - 定義 `AttributeAnalyzerBase` 類別，繼承 `abc.ABC`。
      - 定義抽象方法 `analyze(self, image, boxes)`。
      - 可加上初始化方法 `__init__`，方便子類擴充。

   4. **撰寫註解與型別提示**
      - 為方法加上 docstring，說明參數型態與回傳格式。
      - 建議用型別提示（type hint）提升可讀性。

   5. **（可選）設計簡單單元測試**
      - 測試子類繼承時，若未實作 `analyze` 會報錯。
      - 測試正確繼承與覆寫時能正常運作。

   ---


3. **Label-based 屬性分析器（`LabelBasedAttributeAnalyzer`，多標籤分類）**
   - 實作多標籤分類的屬性分析器 class，繼承自基底類別。
   - 介面設計：`analyze(image, boxes)`，回傳每個 box 的屬性標籤。

   Label-based 屬性分析器（`LabelBasedAttributeAnalyzer`）開發步驟如下：



   ### Label-based AttributeAnalyzer 開發步驟

   1. **明確需求與介面設計**
      - 目標：針對每個 bounding box，進行多標籤屬性分類（如性別、年齡、服裝等）。
      - 介面：`analyze(image, boxes)`，輸入單張影像與多個 box，回傳每個 box 的屬性標籤（dict）。

   2. **繼承基底類別**
      - 繼承 `AttributeAnalyzerBase`，強制實作 `analyze` 方法。

   3. **模型選擇與初始化**
      - 可先用 stub（隨機產生屬性）或簡單的多標籤分類模型（如 torchvision resnet、MLP）。
      - 若有訓練好的屬性分類模型，可在此初始化。

   4. **實作 analyze 方法**
      - 對每個 box，crop 出對應區域，進行前處理（resize、normalize）。
      - 將每個 crop 丟入屬性分類模型，取得多標籤預測結果。
      - 將每個 box 的屬性結果組成 dict，回傳 List[Dict]。

   5. **型別提示與註解**
      - 為方法加上型別提示與 docstring，說明輸入輸出格式。

   6. **（可選）單元測試與 stub**
      - 先實作 stub 版本（隨機產生屬性），確保流程可跑通。
      - 後續可替換為真實模型。

---


4. **Prompt-based 屬性分析器（`PromptBasedAttributeAnalyzer`，CLIP/Zero-shot）**
   - 實作 CLIP/Zero-shot 風格的 prompt-based 屬性分析器 class，繼承自基底類別。
   - 介面設計：`analyze(image, boxes, prompts)`，回傳每個 box 的屬性分數或標籤。

      ## Prompt-based 屬性分析器（PromptBasedAttributeAnalyzer）開發步驟
      ---

      ### 1. 明確需求與介面設計
         - 目標：針對每個 bounding box，利用 CLIP/Zero-shot 方法，根據 prompt 判斷屬性分數或標籤。
         - 介面：`analyze(image, boxes, prompts)`，輸入單張影像、偵測框與 prompt 列表，回傳每個 box 的屬性分數或標籤。

      ### 2. 繼承基底類別
         - 繼承 `AttributeAnalyzerBase`，強制實作 `analyze` 方法。

      ### 3. 模型選擇與初始化
         - 選用 CLIP（如 OpenAI CLIP、HuggingFace CLIP）等支援 Zero-shot 的模型。
         - 初始化 CLIP 模型與 tokenizer，支援多種 prompt 輸入。

      ### 4. 前處理與特徵提取
         - 對每個 box crop 出對應區域，進行前處理（resize、normalize）。
         - 將每個 crop 轉為 CLIP 輸入格式，提取影像特徵。
         - 將 prompts 轉為 CLIP 文本特徵。

      ### 5. 相似度計算與屬性判斷
         - 計算每個 crop 與所有 prompt 的相似度分數。
         - 根據分數決定每個 box 的屬性標籤（可設閾值或取最大分數）。

      ### 6. 回傳結構化結果
         - 將每個 box 的屬性分數或標籤組成 dict，回傳 List[Dict] 或 List[List]。

      ### 7. 型別提示與註解
         - 為方法加上型別提示與 docstring，說明輸入輸出格式。

      ### 8. 單元測試與 stub
         - 先實作 stub 版本（隨機分數），確保流程可跑通。
         - 後續可替換為真實 CLIP 模型。

5. **模型訓練、驗證、推論方法（根據分析器類型分流）**
   - 實作訓練、驗證、推論流程，可根據分析器類型自動分流。
   - 介面設計：`train()`, `validate()`, `predict()`。

6. **模型儲存與載入介面（通用/分流）**
   - 提供模型儲存、載入方法，支援通用與分流（label-based/prompt-based）格式。

7. **prompt 設定/管理介面（prompt-based專用）**
   - 設計 prompt 管理工具，方便 prompt-based 分析器設定、切換、儲存 prompt。

8. **單元測試覆蓋主要模型方法（兩種流程都要）**
   - 為偵測、屬性分析、訓練、推論等主要方法撰寫單元測試，確保各種情境下功能正確。

---

### Checklist

- [x] 行人偵測模型 class（如 YOLO, Faster R-CNN）
- [x] 屬性分析基底類別（`AttributeAnalyzerBase`，統一接口）
- [x] Label-based 屬性分析器（`LabelBasedAttributeAnalyzer`，多標籤分類）
- [ ] Prompt-based 屬性分析器（`PromptBasedAttributeAnalyzer`，CLIP/Zero-shot）
- [ ] 模型訓練、驗證、推論方法（根據分析器類型分流）
- [ ] 模型儲存與載入介面（通用/分流）
- [ ] prompt 設定/管理介面（prompt-based專用）
- [ ] 單元測試覆蓋主要模型方法（兩種流程都要）

---

## 4. 後處理與結果封裝層

### 工作目標
- 在模型推論後，設計一層後處理與訊息封裝，將原始輸出轉為結構化、語意化資訊。
- 支援格式化（如 dict、JSON、DataFrame）、屬性分群、排序、信心分數過濾等。
- 方便前端、API、CLI 等消費端直接使用。

#### Checklist
- [ ] 設計後處理與封裝介面
- [ ] 支援多種輸出格式
- [ ] 可根據需求自訂封裝內容

---

### 5. API 介面設計（`api/`）

#### Checklist
- [ ] 設計 API 架構（如 FastAPI）
- [ ] 實作模型推論 API
- [ ] 實作資料上傳/查詢 API
- [ ] API 測試腳本與文件

---

### 6. 主程式整合與工作流設計（`main.py`）
#### Checklist
- [ ] 整合資料前處理、模型推論、API 調用流程
- [ ] 設計主程式入口與參數設定
- [ ] 撰寫範例執行腳本

---

### 7. 單元測試與驗證（`tests/`）
#### Checklist
- [ ] 為 utils、models、api 撰寫測試案例
- [ ] 測試覆蓋率報告
- [ ] 持續整合（CI）規劃

---

### 8. 文件撰寫與專案說明（`README.md`）
#### Checklist
- [ ] 專案架構與功能說明
- [ ] 安裝與執行教學
- [ ] API 文件與範例
- [ ] 模型訓練與推論流程說明

---

如需展開某一階段細節或開始 scaffold 程式碼，請告知！