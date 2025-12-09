# Inference Pipeline 開發規劃

## 階段一：基礎推論流程建構

### 階段目標
- 建立標準化的推論 pipeline，涵蓋前處理、模型推論、後處理、結果回傳。
- 確保 pipeline 可擴展、可維護，便於後續效能優化與監控。

1. **前處理模組設計與實作**
   - 定義 PreprocessManager 介面與責任（如影像/文字前處理、tokenizer、正規化等）
   - 實作基礎前處理類別（如 BaseImagePreprocessor, BaseTextTokenizer）
   - 設計 registry/factory 機制，支援多種前處理策略

2. **多模型推論流程支援**
   - 整理現有 YOLO、Faster R-CNN、CLIP 等模型推論 API
   - 設計 ModelManager 或類似抽象層，統一推論入口
   - 測試多模型切換與推論結果一致性

3. **後處理模組設計與實作**
   - 定義 PostprocessManager 介面與責任（分群、排序、信心分數過濾等）
   - 實作常用後處理方法（如 NMS、分群、top-k 選擇）
   - 支援多格式輸出（JSON、CSV、可視化等）

4. **PipelineController 串接**
   - 設計 PipelineController，負責協調前處理、模型推論、後處理
   - 實作 run() 或主流程方法，確保資料流正確
   - 撰寫簡易主程式或 CLI，驗證 pipeline 可用性

5. **API 服務包裝**
   - 使用 FastAPI 建立 RESTful API 入口
   - 定義 Pydantic 資料模型，驗證輸入/輸出格式
   - 實作推論 API 路由，串接 PipelineController

6. **單元測試覆蓋**
   - 為 PreprocessManager、PostprocessManager、PipelineController 撰寫 pytest 單元測試
   - 測試 API 端點（可用 httpx 或 FastAPI TestClient）
   - 確認各環節異常處理與邊界情境

### Checklist
- [x] 前處理模組（PreprocessManager）設計與實作
- [x] 支援多模型（YOLO, Faster R-CNN, CLIP 等）推論流程
- [x] 後處理模組（PostprocessManager）設計與實作（分群、排序、過濾）
- [x] PipelineController 串接前處理、推論、後處理
- [x] API 服務（FastAPI）包裝 pipeline，支援 RESTful 請求
- [x] 單元測試覆蓋 pipeline 各環節

---

## 階段二：推論效能優化

### 階段目標
- 優化推論延遲（latency）、提升吞吐量（throughput）、降低資源消耗。
- 為面試展示提供具體效能數據與優化手法。

## 階段二：推論效能優化 — 開發步驟

### 1. 支援 batch inference 與非同步請求
- 分析現有 pipeline，設計 batch 輸入資料結構
- 修改前處理、模型推論、後處理流程，支援多張影像/多筆資料同時處理
- FastAPI 路由支援 async/await，提升併發能力
- 撰寫單元測試驗證 batch/async 行為

### 2. 模型 ONNX 化與推論加速
- 研究現有模型（YOLO、Faster R-CNN、CLIP）是否支援 ONNX 匯出
- 使用 `torch.onnx.export` 或官方工具將模型轉為 ONNX
- 整合 ONNX Runtime 或 TensorRT，替換原本的推論引擎
- 比較原生與加速後的推論效能

### 3. Docker 映像瘦身與資源限制
- 優化 Dockerfile，減少不必要的套件與檔案
- 使用多階段建構（multi-stage build）
- 設定 Docker 資源限制（如 memory、CPU、GPU）
- 驗證容器啟動速度與資源佔用

### 4. pipeline 內部 profiling
- 在 pipeline 各階段（前處理、推論、後處理）加上時間戳記
- 使用 `time`、`logging` 或 `PyTorch Profiler` 進行效能分析
- 收集 latency、throughput、memory usage 等數據

### 5. 效能基準測試腳本
- 撰寫自動化效能測試腳本（可用 Python、ab、wrk、locust 等工具）
- 模擬多種請求量、資料型態，收集 latency、throughput、memory usage
- 整理測試報告，便於優化前後對比

### 6. 效能優化前後對比報告
- 彙整優化前後的效能數據（表格、圖表）
- 分析瓶頸與優化成效
- 撰寫報告或簡報，便於面試/展示

---

**實作建議：**
- 先從 batch/async 支援與 profiling 開始，快速取得效能數據
- 再進行 ONNX 化、推論加速與 Docker 瘦身
- 每步驟完成後，建議立即測試、記錄數據與截圖存證

### Checklist
- [ ] 支援 batch inference 與非同步請求
- [ ] 模型 ONNX 化與推論加速（如 ONNX Runtime、TensorRT）
- [ ] Docker 映像瘦身與資源限制（memory, CPU, GPU）
- [ ] pipeline 內部 profiling（PyTorch Profiler、time breakdown）
- [ ] 效能基準測試腳本（latency, throughput, memory usage）
- [ ] 效能優化前後對比報告

---

## 階段三：推論監控與告警

### 階段目標
- 建立推論服務監控體系，實現 SLA 追蹤、異常告警、效能可視化。

### Checklist
- [ ] Prometheus metrics 暴露（latency, throughput, error rate, GPU utilization）
- [ ] Grafana dashboard 視覺化推論指標
- [ ] SLA 追蹤與異常告警（如 p95 latency、error rate）
- [ ] 日誌與請求追蹤（logging, tracing）
- [ ] 監控指標文件與 dashboard 截圖

---

## 階段四：推論成本與部署優化

### 階段目標
- 降低推論運算成本，提升部署彈性與可維護性。

### Checklist
- [ ] 多模型/多任務動態調度（如多模型共用 GPU）
- [ ] 支援動態 batch size、資源自動調整
- [ ] Docker Compose/K8s 部署腳本
- [ ] 成本分析報告（token/dollar, infra sizing）
- [ ] 一鍵啟動與自動化部署腳本

---

## 階段五：面試展示與文件補強

### 階段目標
- 完善文件、測試、展示材料，強化面試說服力。

### Checklist
- [ ] API 文件（Swagger/OpenAPI、自動生成）
- [ ] 安裝與啟動教學（README、腳本）
- [ ] 前端展示頁（可選，顯示推論結果/效能指標）
- [ ] 測試覆蓋率報告、CI/CD 配置
- [ ] 面試用簡報/流程圖/效能數據整理

---

> 建議每階段完成後，立即補充對應文件與測試，確保成果可展示、可驗證。