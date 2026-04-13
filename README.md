# Concert Booking System

演唱會售票系統 — 一個用來練習資料庫操作的後端專案。

## 專案簡介

本專案模擬一個演唱會線上售票平台，涵蓋使用者註冊登入、演唱會瀏覽、座位選擇、訂票與付款等核心流程。主要目的是透過實作真實的業務場景，深入練習資料庫相關操作，包括：

- **資料表設計與關聯** — 使用者、演唱會、場館、座位區域、票券、訂單等多表關聯
- **交易與並發控制** — 搶票情境下的 race condition 處理、悲觀鎖 / 樂觀鎖實作
- **索引與查詢優化** — 針對高頻查詢建立適當索引，分析 query plan
- **資料庫遷移** — 使用 Alembic 管理 schema 變更
- **Seed 資料** — 自動產生測試用假資料

## Tech Stack

| 層級 | 技術 |
|------|------|
| Web Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL (asyncpg) |
| Migration | Alembic |
| Auth | JWT (PyJWT) + bcrypt |
| Validation | Pydantic v2 |
| Package Manager | PDM |
| Runtime | Python 3.13+ |


## 快速開始

### 前置需求

- Python 3.13+
- PostgreSQL
- PDM

### 安裝與啟動

```bash
# 安裝依賴
pdm install

# 設定環境變數（資料庫連線等）
cp .env.example .env

# 啟動開發伺服器
pdm run uvicorn app.main:app --reload
```

伺服器啟動後會自動執行 seed，產生 100 筆測試用使用者資料。

### API 文件

啟動後可至 `http://localhost:8000/docs` 查看 Swagger UI。

## 練習的 DB 主題

- 基本 CRUD 操作
- 使用者認證（註冊 / 登入 / JWT）
- 一對多 / 多對多關聯（演唱會 ↔ 場館、使用者 ↔ 訂單）
- Transaction 管理與錯誤回滾
- 並發搶票的鎖機制（`SELECT ... FOR UPDATE`）
- 分頁查詢（cursor-based / offset-based）
- 索引設計與 `EXPLAIN ANALYZE`
- Alembic migration 版本管理
- 軟刪除（soft delete）
- 資料聚合查詢（統計報表）

## License

MIT
