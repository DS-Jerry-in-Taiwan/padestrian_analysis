# 行人偵測與屬性分析服務

## 1. 專案服務目標與框架

本專案致力於打造一套可擴充、可維護的行人偵測與屬性分析服務，支援主流前後端分離架構。  
服務涵蓋行人偵測、屬性分析（label-based 與 prompt-based）、模型訓練/推論、前處理與後處理等完整流程，並具備統一接口與模組化設計，便於擴展與集成。

---

## 2. 專案功能模組說明

- **前處理模組（preprocess/）**  
  - 負責文字與影像的標準化處理，支援多種 tokenizer（如 OpenCLIP、BERT、HuggingFace）。
- **模型模組（models/）**  
  - 行人偵測模型（YOLO, Faster R-CNN 等）
  - 屬性分析模型（Label-based、Prompt-based，支援多標籤分類與 vision-language 模型）
  - 統一訓練、推論、驗證接口
  - Checkpoint 儲存/載入
- **中介層（PreprocessManager/ModelManager）**  
  - 根據配置自動選擇並調用對應前處理與模型類
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
pedestrian_attribute_recognition/
├── preprocess/                          # 前處理模組
│   ├── __init__.py
│   ├── base_preprocessor.py            # 基礎前處理類
│   ├── PreprocessManager.py            # 前處理管理器
│   ├── registry.py                     # 註冊器
│   ├── clip_image_preprocessor.py      # CLIP 影像前處理
│   ├── vit_image_preprocessor.py       # ViT 影像前處理
│   ├── clip_text_preprocessor.py       # CLIP 文字前處理
│   ├── openclip_text_tokenizer.py      # OpenCLIP 文字分詞器
│   ├── openclip_text_tokenizer-v2.py   # OpenCLIP 文字分詞器 v2
│   ├── bert_text_prerpocessor.py       # BERT 文字前處理
│   └── read_image.py                   # 影像讀取工具
│
├── models/                              # 模型模組
│   ├── __init__.py
│   ├── attribute_analyzer_base.py      # 屬性分析基礎類
│   ├── label_based_attribute_analyzer.py      # 標籤式屬性分析器
│   ├── prompt_based_attribute_analyzer.py     # 提示式屬性分析器
│   └── pedestrian_detector.py          # 行人檢測器
│
├── tests/                               # 測試模組
│   ├── test_read_image.py              # 影像讀取測試
│   ├── data/                           # 測試資料
│   └── unit_tests/                     # 單元測試
│       ├── test_clip_images_preprocessor.py
│       ├── test_openclip_text_preprocessor.py
│       ├── test_bert_text_preprocessor.py
│       ├── test_preprocess_manage.py
│       └── test_registry.py
│
├── api/                                 # API 模組 (待開發)
│
├── utils/                               # 工具模組 (待開發)
│
├── fine-tune/                           # 模型微調相關
│   ├── Yolov8.py
│   ├── faster-R-CNN.py
│   ├── torchvision_fine_tune.py
│   ├── data.yml
│   ├── odgt_to_coco.py
│   ├── odgt_to_yolo.py
│   └── fine-tune開發規劃.md
│
├── data/                                # 資料集
│   ├── COCO/
│   ├── CrowdHuman/
│   ├── PA-100K/
│   └── d6-dice/
│
├── dev_doc/                             # 開發文檔
│   ├── framework/                      # 架構設計文檔
│   ├── CLIP_Preprocess.md
│   ├── module-framework.md
│   ├── pedestrain_analysis module開發規劃-v1~v7.md
│   ├── registery_preprocessor_module說明.md
│   └── 文字前處理類開發.md
│
├── main.py                              # 主程式入口
├── requirements.txt                     # Python 依賴套件
├── README.md                            # 專案說明文件
└── yolov8n.pt                          # YOLOv8 預訓練模型
```

---

## 聯絡與貢獻

如需協作或有任何建議，歡迎提交 issue 或 pull request！

---