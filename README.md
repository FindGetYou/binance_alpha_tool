# Binance Alpha Tool – Quick Start

本项目包含后端 FastAPI 和前端 React（Vite）。后端负责行情与计算，前端提供可交互 UI。

## 环境准备
- Python ≥ 3.12（推荐 venv 虚拟环境）
- Node.js ≥ 18（Vite 5 需要）

## 后端启动
1) 创建虚拟环境并安装依赖
   - python -m venv .venv
   - source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
   - pip install -r backend/requirements.txt

2) 可选：设置环境变量（见下文“系统参数”）或直接修改 backend/config/config.py:1

3) 启动服务
   - uvicorn backend.main:app --reload

4) 健康检查
   - GET http://127.0.0.1:8000/health

5) API 快测
   - 计算价差
     - POST http://127.0.0.1:8000/api/calc/price-range
     - Body:
       {"price_now":"1","per_volume":"100","waste_lower":"3","waste_upper":"5","fee_amount_token":"2"}
     - 预期：diff_lower=0.01000000, diff_upper=0.03000000
   - 价格查询（REST 聚合近 N 笔成交，返回 last/avg/vwap）
     - GET /api/alpha/price?alphaId=BTCUSDT  # 直接交易对
     - GET /api/alpha/price?alphaId=KOGE     # 作为 Base，会自动拼接 USDT
     - GET /api/alpha/price?alphaId=ALPHA_118
       - 若存在本地映射或外部列表，会解析为对应交易对

6) Alpha Token 列表数据源（3 选 1）
   - 设置 ALPHA_TOKENS_API 指向你的对外服务（支持数组、{data: [...]} 或映射 {alphaId: symbol}）
   - 或使用本地文件：复制 backend/data/alpha_tokens.example.json:1 为 backend/data/alpha_tokens.json:1，并按需补充
   - 若两者都未配置，后端会返回空数组，前端可用 Custom 模式手动输入

## 前端启动
1) 配置后端地址
   - cd frontend
   - cp .env.example .env
   - 根据需要修改 .env 中的 VITE_API_BASE（默认 http://127.0.0.1:8000）

2) 安装依赖并启动
   - npm install
   - npm run dev
   - 打开 http://127.0.0.1:5173

## 前端交互说明
- 顶部 Token 选择支持搜索；也可切换 Custom 手动输入（ALPHA_118USDT）
- Realtime Price 区域：固定展示 15 条，最新在最上；不滚动、不闪烁，表头显示 Time/Last/Avg/VWAP，Symbol 作为副标题
- Calculator 在页面顶部；输入修改或点击 Calculate 调用后端计算接口
- 显示规则：价格与结果统一 8 位小数，ROUND_HALF_UP（四舍五入）
- 若需要修改 Realtime Price 可视条数，调整常量：frontend/src/App.tsx:17

## 系统参数（环境变量，可覆盖 backend/config/config.py 默认值）
- 数值与舍入
  - DECIMAL_PLACES：默认 8（统一显示 8 位小数）
  - LOG_LEVEL：默认 INFO
- 代理（REST）
  - USE_PROXY：默认 true
  - HTTP_PROXY：例如 http://127.0.0.1:7890（必须包含 http:// 或 https:// 前缀）
  - 说明：本项目对 httpx 使用环境代理（trust_env），无需在代码中配置 proxies
- 代理（WebSocket，预留）
  - SOCKS_HOST：默认 127.0.0.1
  - SOCKS_PORT：默认 7891（仅 WS 使用，REST 不走 SOCKS5）
- 速率与重试
  - RATE_LIMIT_WINDOW_SECONDS：默认 60
  - RATE_LIMIT_MAX_REQUESTS：默认 60
  - RETRY_MAX_ATTEMPTS：默认 3
  - RETRY_BACKOFF_BASE：默认 0.25（秒）
  - RETRY_BACKOFF_FACTOR：默认 2.0
- 外部接口与交易对规则
  - BINANCE_REST_BASE：默认 https://www.binance.com
  - DEFAULT_TRADES_LIMIT：默认 50（聚合最近 N 笔）
  - ALPHA_TOKENS_API：可选，外部 Token 列表接口或本地 JSON 路径
  - ALPHA_SYMBOL_SUFFIX：默认 USDT（Base 拼接为 Base+USDT）
- 前端
  - VITE_API_BASE：前端调用的后端地址（在 frontend/.env）

## 常见问题
- 列表接口 500：确认 ALPHA_TOKENS_API 为完整 URL（http/https）或有效的本地 JSON 路径
- 代理无效：请确保 HTTP_PROXY 带协议前缀（如 http://127.0.0.1:7890）；REST 不使用 SOCKS5
- 列表为空：前端可用 Custom 手动输入；或创建 backend/data/alpha_tokens.json 映射
