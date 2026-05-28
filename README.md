# Concert Booking System

演唱會售票系統 — 一個用來練習資料庫操作的後端專案。

## 專案簡介

本專案模擬一個演唱會線上售票平台，涵蓋使用者註冊登入、演唱會瀏覽、座位選擇與訂票等核心流程。主要目的是透過實作真實的業務場景，深入練習資料庫相關操作，包括：

- **資料表設計與關聯** — 使用者、演唱會、票券種類、訂單等多表關聯
- **交易與並發控制** — 搶票情境下的 race condition 處理、Redis 原子操作防超賣
- **Seed 資料** — 自動產生測試用假資料

## Tech Stack

| 層級 | 技術 |
|------|------|
| Web Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL (asyncpg) |
| Cache | Redis (redis-py asyncio) |
| Migration | Alembic |
| Auth | JWT (PyJWT) + bcrypt |
| Validation | Pydantic v2 |
| Package Manager | PDM |
| Runtime | Python 3.13+ |


## 快速開始

### 前置需求

- Python 3.13+
- PostgreSQL
- Redis
- PDM

### 安裝與啟動

```bash
# 安裝依賴
pdm install

# 設定環境變數
cp .env.example .env
# 編輯 .env，填入你的 DATABASE_URL 與 SECRET_KEY

# 建立資料庫
createdb booking

# 套用 migration，建立所有 table
pdm run alembic upgrade head

# 啟動開發伺服器
pdm run uvicorn app.main:app --reload
```

伺服器啟動後會自動執行 seed，寫入 100 筆測試用使用者與演唱會資料。

### API 文件

啟動後可至 `http://localhost:8000/docs` 查看 Swagger UI。

## 練習的 DB 主題

- 基本 CRUD 操作
- 使用者認證（註冊 / 登入 / JWT）
- 一對多關聯（Concert → TicketTier、User → Booking）
- Transaction 管理與錯誤回滾
- 並發搶票控制（Redis `DECRBY` 原子操作，避免 DB 鎖耗盡 connection pool）

## License

MIT
