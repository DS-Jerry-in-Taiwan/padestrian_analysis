# 行人偵測與屬性分析服務化開發規劃（主流前後端分離服務架構）

本規劃依據主流 AI 服務開發流程，強調分層、模組化、容器化與前後端分離，並明確規劃各階段所需的開發流程。

---

## 1. 專案初始化與目錄結構

- 建立專案目錄與基本結構
- 建立 `requirements.txt`、`README.md`
- 初始化 Git 版本控管
- 設計前後端分離目錄（如 `backend/`、`frontend/`）
- 設定 Python 虛擬環境與前端開發環境（如 Node.js）
- 設定 Dockerfile、docker-compose 基礎檔案

---

## 2. 資料前處理工具設計（`backend/utils/`）

- 設計前處理中介層（PreprocessManager/Adapter），統一入口，支援影像/文字/其他型態前處理
- 建立 Registry/Factory 機制，集中管理所有前處理類
- 開發底層前處理類（如 CLIPImagePreprocessor、ViTImagePreprocessor、CLIPTextTokenizer 等）
- 撰寫單元測試，覆蓋前處理中介層、registry、底層類的主要功能
- 文件與型別提示補充

---

## 3. 模型架構設計與實作（`backend/models/`）

- 設計行人偵測模型（如 YOLO, Faster R-CNN），介面 `detect(image)`，可用預訓練模型或 stub/mock
- 設計屬性分析基底類別，統一接口（`analyze(image, boxes)`），方便擴充 label-based、prompt-based 分析器
- 開發 Label-based 屬性分析器、多標籤分類
- 開發 Prompt-based 屬性分析器（CLIP/Zero-shot）
- 實作模型訓練、驗證、推論方法，支援自動分流
- 支援模型 checkpoint 儲存/載入
- 撰寫單元測試，覆蓋偵測、屬性分析、訓練、推論等主要方法

---

## 4. 推論服務設計與整合（`backend/inference_service/`）

- 設計主流程控制層，協調前處理、模型推論、後處理等模組
- 整合前處理模組、模型管理與推論模組、後處理模組
- 實作快取、日誌、資料存取等輔助功能
- 撰寫單元測試，驗證主流程協調與各模組整合正確性

---

## 5. 後處理與結果封裝層（`backend/postprocess/`）

- 開發後處理模組，將模型原始輸出轉為結構化、語意化資訊
- 支援 dict、JSON、DataFrame 等格式
- 支援屬性分群、排序、信心分數過濾
- 提供 API 友善的回傳格式
- 撰寫單元測試，驗證後處理正確性

---

## 6. API 介面設計（`backend/api/`）

- 使用 FastAPI（或 Flask）設計 RESTful API
- 定義主要 API 端點（如 `/detect`、`/analyze`、`/pipeline`、`/health`）
- 設計請求/回應格式，參數驗證，支援 CORS
- 撰寫 API 文件（Swagger/OpenAPI）
- 撰寫 API 層單元測試與整合測試

---

## 7. 前端服務設計（`frontend/`）

- 使用 React/Vue/Svelte 等 SPA 框架
- 設計影像上傳、即時預覽、結果顯示、批次上傳與結果下載等功能
- 串接後端 API，設計資料流與狀態管理
- UI/UX 設計，支援響應式介面
- 撰寫前端單元測試與整合測試

---

## 8. 主程式整合與工作流設計（`backend/main.py`）

- 整合 API、推論主流程、前處理、模型推論、後處理、資料存取等模組
- 設計主程式入口與參數設定
- 撰寫範例執行腳本與啟動腳本

---

## 9. 單元測試與驗證（`backend/tests/`）

- 為 utils、models、inference_service、postprocess、api 撰寫測試案例
- 覆蓋率報告
- 持續整合（CI/CD）規劃

---

## 10. 文件撰寫與專案說明（`README.md`）

- 專案架構與功能說明
- 安裝與執行教學
- API 文件與範例
- 前端操作說明
- 模型訓練與推論流程說明

---

## 11. 部署與維運

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