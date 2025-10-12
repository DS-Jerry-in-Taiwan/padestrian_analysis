# 行人偵測與屬性分析服務化開發規劃（主流前後端分離服務架構）

本規劃依據主流 AI 服務開發流程，強調分層、模組化、容器化與前後端分離。  
每個階段皆明確定義**目標**與**Checklist**，確保開發成果符合預期。

---

## 1. 專案初始化與目錄結構

**目標：**  
建立清晰、可維護的專案基礎架構，方便團隊協作與後續擴展。

#### 工項與檢查點

- **專案目錄結構設計**
  - [ ] 是否已明確區分前端（frontend/）與後端（backend/）？
  - [ ] 是否有 utils、models、api、postprocess、inference_service、tests 等子目錄？
  - [ ] 是否有 docs 或 dev_doc 目錄存放設計文件？

- **基礎設定檔建立**
  - [ ] 是否有 requirements.txt（後端）、package.json（前端）？
  - [ ] 是否有 README.md 並初步說明專案？
  - [ ] 是否有 .gitignore 並排除不必要檔案？

- **版本控管初始化**
  - [ ] 是否已初始化 Git 並建立主分支？
  - [ ] 是否有基本的 commit 規範或分支策略？

- **開發環境可啟用**
  - [ ] Python 虛擬環境可正常啟動並安裝依賴？
  - [ ] 前端 Node.js 環境可正常啟動並安裝依賴？

- **容器化基礎**
  - [ ] 是否有 Dockerfile（前端、後端各自一份）？
  - [ ] 是否有 docker-compose.yml 可一鍵啟動前後端？
**Checklist：**
- [x] 完成專案目錄與基本結構規劃
- [x] 建立 `requirements.txt`、`README.md`
- [x] 完成 Git 初始化與 .gitignore 設定
- [x] 前後端分離目錄（如 `backend/`、`frontend/`）明確
- [x] Python 虛擬環境、前端開發環境（Node.js）可正常啟用
- [x] 提供 Dockerfile、docker-compose 基礎檔案

---

## 2. 資料前處理工具設計（`backend/utils/`）

**目標：**  
具備可擴充、可組合的前處理工具，支援影像、文字等多型態資料，並可單元測試。

#### 工項與檢查點

- **前處理中介層設計**
  - [x] 是否有 PreprocessManager/Adapter，統一調用各型態前處理？
  - [x] 是否支援 mode='auto' 或明確指定前處理流程？

- **Registry/Factory 機制**
  - [x] 是否有註冊/管理前處理類的 registry/factory？
  - [x] 是否支援外部注入、動態擴充新型態前處理？

- **底層前處理類**
  - [ ] 是否有影像前處理類（如 CLIPImagePreprocessor、ViTImagePreprocessor）？

  - [ ] 是否有文字前處理類（如 CLIPTextTokenizer 等）？
  
  - [ ] 是否統一接口（如 `__call__`、`batch_preprocess`），支援例外處理與標準化輸出？

- **單元測試**
  - [ ] 是否有覆蓋前處理中介層、registry、底層類的單元測試？
  - [ ] 是否測試正常與異常情境？

- **型別提示與文件**
  - [ ] 是否有型別提示（type hints）？
  - [ ] 是否有必要的模組/類別/方法文件？


**Checklist：**
- [x] 前處理中介層（PreprocessManager/Adapter）可統一調用各型態前處理
- [x] Registry/Factory 機制可動態註冊/管理前處理類
- [x] 影像、文字等底層前處理類可獨立覆用
- [x] 前處理模組有單元測試，涵蓋正常與異常情境
- [x] 具備型別提示與必要文件

---

## 3. 模型架構設計與實作（`backend/models/`）

**目標：**  
建立可擴充、可維護的模型架構，支援主流偵測與屬性分析模型，並可訓練、推論、測試。

**Checklist：**
- [x] 行人偵測模型（如 YOLO, Faster R-CNN）可推論與訓練
- [x] 屬性分析基底類別可擴充 label-based、prompt-based 分析器
- [x] Label-based、Prompt-based 屬性分析器可正確推論
- [x] 模型訓練、驗證、推論方法統一接口
- [ ] 模型可 checkpoint 儲存/載入
- [ ] 模型模組有單元測試，涵蓋主要功能

---

## 4. 推論服務設計與整合（`backend/inference_service/`）

**目標：**  
主流程可協調前處理、模型推論、後處理等模組，並支援快取、日誌、資料存取等輔助功能。

**Checklist：**
- [ ] 主流程控制層可依序調用前處理、推論、後處理
- [ ] 可整合多模型與多任務推論
- [ ] 支援快取、日誌、資料存取等輔助功能
- [ ] 主流程有單元測試，驗證模組協調正確性

---

## 5. 後處理與結果封裝層（`backend/postprocess/`）

**目標：**  
將模型原始輸出轉為結構化、語意化資訊，並支援多種回傳格式與後處理功能。

**Checklist：**
- [ ] 後處理模組可將模型輸出轉為 dict、JSON、DataFrame 等格式
- [ ] 支援屬性分群、排序、信心分數過濾等功能
- [ ] 提供 API 友善的回傳格式
- [ ] 後處理模組有單元測試，驗證功能正確性

---

## 6. API 介面設計（`backend/api/`）

**目標：**  
提供標準化、易於串接的 RESTful API，支援主要業務流程與健康檢查。

**Checklist：**
- [ ] 使用 FastAPI（或 Flask）設計 RESTful API
- [ ] 定義 `/detect`、`/analyze`、`/pipeline`、`/health` 等端點
- [ ] API 支援請求/回應格式驗證、CORS
- [ ] 提供自動化 API 文件（Swagger/OpenAPI）
- [ ] API 層有單元測試與整合測試

---

## 7. 前端服務設計（`frontend/`）

**目標：**  
提供友善的用戶操作介面，支援影像上傳、結果顯示與 API 串接。

**Checklist：**
- [ ] 使用 SPA 框架（React/Vue/Svelte）完成主頁面
- [ ] 支援影像上傳、即時預覽、結果顯示
- [ ] 支援批次上傳與結果下載
- [ ] 可正確串接後端 API
- [ ] 前端有單元測試與整合測試

---

## 8. 主程式整合與工作流設計（`backend/main.py`）

**目標：**  
整合所有後端模組，提供一鍵啟動與範例執行流程。

**Checklist：**
- [ ] 整合 API、推論主流程、前處理、模型推論、後處理、資料存取等模組
- [ ] 設計主程式入口與參數設定
- [ ] 提供範例執行腳本與啟動腳本

---

## 9. 單元測試與驗證（`backend/tests/`）

**目標：**  
確保各模組功能正確、流程穩定，並具備自動化測試與持續整合能力。

**Checklist：**
- [ ] 為 utils、models、inference_service、postprocess、api 撰寫測試案例
- [ ] 產生測試覆蓋率報告
- [ ] 配置持續整合（CI/CD）流程

---

## 10. 文件撰寫與專案說明（`README.md`）

**目標：**  
讓新成員或用戶能快速理解、安裝、使用與擴充專案。

**Checklist：**
- [ ] 說明專案架構與功能
- [ ] 提供安裝與執行教學
- [ ] API 文件與範例
- [ ] 前端操作說明
- [ ] 模型訓練與推論流程說明

---

## 11. 部署與維運

**目標：**  
實現一鍵部署、可監控、可維運的前後端服務。

**Checklist：**
- [ ] Docker 化後端與前端服務
- [ ] 提供 docker-compose 一鍵部署
- [ ] 支援雲端部署（如 Azure、AWS、GCP）
- [ ] 設計日誌、監控、健康檢查

---

### 進階優化（可選）

**目標：**  
提升用戶體驗、系統效能與安全性。

**Checklist：**
- [ ] 支援 WebSocket 即時推播
- [ ] 前端支援拖拉/多檔上傳
- [ ] 後端支援 GPU/CPU 動態切換
- [ ] API 權限控管與用量統計

---

如需展開某一階段細節或 scaffold 程式碼，請隨時告知！