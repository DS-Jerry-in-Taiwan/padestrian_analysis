graph TD
    subgraph 用戶端
        FE[前端服務容器（如 React/Vue SPA）]
    end

    subgraph 伺服器端
        BE[後端API服務容器（如 FastAPI/Flask）]
        DB[(資料儲存/檔案系統)]
        subgraph ML[模型推論服務容器]
            GW[API Gateway/入口]
            PRE[前處理模組]
            MM[模型管理與推論]
            POST[後處理模組]
            CACHE[資料存取/快取]
        end
    end

    FE -- RESTful API 請求 --> BE
    BE -- 讀寫/存取 --> DB
    BE -- 請求推論 --> GW
    GW -- 請求驗證/路由 --> PRE
    PRE -- 處理後資料 --> MM
    MM -- 推論結果 --> POST
    POST -- 結構化結果 --> GW
    MM -- 中間結果/日誌 --> CACHE
    PRE -- 快取/查詢 --> CACHE
    POST -- 結果存取 --> CACHE