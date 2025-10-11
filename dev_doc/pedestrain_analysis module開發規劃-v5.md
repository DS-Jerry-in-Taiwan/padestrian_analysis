# 行人偵測與屬性分析服務化開發規劃（主流前後端分離服務架構）

本規劃參考主流 AI 服務開發流程（如 FastAPI + 前端 SPA、RESTful API、模組化設計、CI/CD、可擴充性），  
並針對前端辨識服務需求，調整原有規劃，強化 API、後處理、前後端串接與部署流程。

---

## 1. 專案初始化與目錄結構

- [x] 建立專案目錄與基本結構
- [x] 建立 `requirements.txt`、`README.md`
- [x] 初始化 Git 版本控管
- [ ] 設計前後端分離目錄（如 `backend/`、`frontend/`）
- [ ] 設定 Python 虛擬環境與前端開發環境（如 Node.js）

---

## 2. 資料前處理工具設計（`backend/utils/`）

### 2.1 前處理中介層（PreprocessManager/Adapter）
- 統一入口，支援影像/文字/其他型態前處理
- API：`preprocess(data, mode='auto')`
- 支援外部注入、註冊新型態前處理類

### 2.2 Registry/Factory 機制
- 全域 registry 與工廠函數，集中管理所有前處理類
- 支援 decorator 註冊、動態擴充

### 2.3 底層前處理類
- 影像前處理（如 CLIPImagePreprocessor、ViTImagePreprocessor）
- 文字前處理（如 CLIPTextTokenizer、OpenCLIPTextTokenizer）
- 統一接口（`__call__`、`batch_preprocess`），支援例外處理、標準化輸出

### 2.4 單元測試
- 覆蓋前處理中介層、registry、底層類的主要功能
- 測試正常與異常情境

---

## 3. 模型架構設計與實作（`backend/models/`）

### 3.1 行人偵測模型
- 支援主流偵測模型（YOLO, Faster R-CNN），介面 `detect(image)`
- 可用預訓練模型或 stub/mock

### 3.2 屬性分析基底類別
- 統一接口（`analyze(image, boxes)`），方便擴充 label-based、prompt-based 分析器

### 3.3 Label-based 屬性分析器
- 多標籤分類，回傳每個 box 的屬性標籤

### 3.4 Prompt-based 屬性分析器
- CLIP/Zero-shot，根據 prompt 回傳屬性分數或標籤

### 3.5 模型訓練、驗證、推論方法
- 統一接口，支援自動分流

### 3.6 模型儲存與載入
- 支援模型 checkpoint 儲存/載入

### 3.7 單元測試
- 覆蓋偵測、屬性分析、訓練、推論等主要方法

---

## 4. 後處理與結果封裝層（`backend/postprocess/`）

- 將模型原始輸出轉為結構化、語意化資訊
- 支援 dict、JSON、DataFrame 等格式
- 支援屬性分群、排序、信心分數過濾
- 提供 API 友善的回傳格式

---

## 5. API 介面設計（`backend/api/`）

- 使用 FastAPI（或 Flask）設計 RESTful API
- 主要 API：
    - `/detect`：上傳影像，回傳偵測結果
    - `/analyze`：上傳影像與 boxes，回傳屬性分析結果
    - `/pipeline`：一鍵完成前處理→偵測→屬性分析→後處理
    - `/health`：健康檢查
- 支援 CORS，方便前端跨域調用
- 撰寫 API 文件（Swagger/OpenAPI）

---

## 6. 前端服務設計（`frontend/`）

- 使用 React/Vue/Svelte 等 SPA 框架
- 主要功能：
    - 影像上傳、即時預覽
    - 顯示偵測框與屬性分析結果
    - 支援批次上傳與結果下載
    - 與後端 API 串接
- UI/UX 設計，支援響應式介面

---

## 7. 主程式整合與工作流設計（`backend/main.py`）

- 整合前處理、模型推論、後處理、API 調用
- 設計主程式入口與參數設定
- 撰寫範例執行腳本

---

## 8. 單元測試與驗證（`backend/tests/`）

- 為 utils、models、api、postprocess 撰寫測試案例
- 覆蓋率報告
- 持續整合（CI/CD）規劃

---

## 9. 文件撰寫與專案說明（`README.md`）

- 專案架構與功能說明
- 安裝與執行教學
- API 文件與範例
- 前端操作說明
- 模型訓練與推論流程說明

---

## 10. 部署與維運

- Docker 化後端與前端服務
- 提供 docker-compose 一鍵部署
- 支援雲端部署（如 Azure、AWS、GCP）
- 設計日誌、監控、健康檢查

---

### 進階優化（可選）

- 支援 WebSocket 即時推播
- 前端支援拖拉/多檔上傳
- 後端支援 GPU/CPU 動態切換
- API 權限控管與用量統計

---

如需展開某一階段細節或 scaffold 程式碼，請隨時告知！