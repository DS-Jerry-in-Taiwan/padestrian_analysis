# 行人偵測與屬性分析服務

## 1. 專案服務目標與框架

本專案致力於打造一套可擴充、可維護的行人偵測與屬性分析服務，支援主流前後端分離架構。  
服務涵蓋行人偵測、屬性分析（label-based 與 prompt-based）、模型訓練/推論、前處理與後處理等完整流程，並具備統一接口與模組化設計，便於擴展與集成。

---

## 2. 專案功能模組說明

- **前處理模組（backend/preprocess/）**  
  - 負責文字與影像的標準化處理，支援多種 tokenizer（如 OpenCLIP、BERT、HuggingFace）。
- **模型模組（backend/models/）**  
  - 行人偵測模型（YOLO, Faster R-CNN 等）
  - 屬性分析模型（Label-based、Prompt-based，支援多標籤分類與 vision-language 模型）
  - 統一訓練、推論、驗證接口
  - Checkpoint 儲存/載入
- **主流程控制層（backend/inference_service/）**  
  - 串接前處理、模型推論、後處理，對外提供統一推論接口
- **API 模組（backend/api/）**  
  - 提供 RESTful API 介面（待開發）
- **單元測試模組（tests/）**  
  - 覆蓋前處理、模型推論、訓練等主要功能，確保系統穩定

---

## 3. 專案流程說明

1. **資料輸入**  
   - 使用者上傳影像或文字描述，進入前處理模組。
2. **前處理**  
   - 文字：分詞、tokenize、padding、mask 等（依模型自動選擇對應 tokenizer）
   - 影像：標準化、resize、增強等
3. **模型推論**  
   - 行人偵測模型先進行偵測，產生候選框
   - 屬性分析模型（label-based 或 prompt-based）對偵測結果進行屬性推論
4. **結果輸出**  
   - 回傳結構化的偵測框與屬性資訊
5. **模型訓練/驗證（可選）**  
   - 支援統一接口進行模型訓練、驗證與 checkpoint 管理

---

## 目錄結構簡介

```
pedestrian_attribute_recognition_30%/
├── backend/
│ ├── fine-tune/ # 模型微調與訓練腳本
│ ├── preprocess/ # 前處理模組
│ ├── models/ # 模型與分析器
│ ├── api/ # API 介面 (待開發)
│ ├── postprocess/ # 後處理模組 (可擴充)
│ ├── inference_service/ # 推論主流程 (pipeline 控制)
│ └── main.py # 主流程入口
│
├── frontend/ # 前端服務 (待開發)
├── data/ # 資料集與原始數據
├── tests/ # 單元測試與測試資料
├── dev_doc/ # 開發文檔與設計規劃
├── requirements.txt # Python 依賴套件
├── README.md # 專案說明文件
├── yolov8n.pt # YOLOv8 預訓練模型
├── .gitignore
├── read_annotation.py
├── read_image-original.py
└── insatll_sequentialThinking.sh
```

- **主流程入口**：`backend/main.py`
- **前處理/後處理/模型/推論流程**：皆集中於 `backend/` 子目錄
- **前端**：`frontend/`（可獨立開發與部署）
- **開發文檔**：`dev_doc/`
- **測試**：`tests/`
- **資料集**：`data/`

---
## 聯絡與貢獻

如需協作或有任何建議，歡迎提交 issue 或 pull request！

---