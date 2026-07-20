# AI 足迹 MCP Server

AI 足迹的 Model Context Protocol (MCP) 服务，可在 ModelScope MCP 广场使用。

## 功能

- 🔍 搜索足迹
- ➕ 添加足迹  
- 📋 列出/查看足迹
- ✏️ 更新足迹
- 📁 管理分类和标签
- 👥 共享分类协作
- 🔗 生成邀请链接

## 配置

| 环境变量 | 说明 | 必填 |
|----------|------|:---:|
| `FOOTPRINTS_TOKEN` | Agent Token（在 ai.ocean94.com 个人中心获取） | ✅ |
| `FOOTPRINTS_ENDPOINT` | API 地址（默认 https://ai.ocean94.com） | ❌ |

## 获取 Token

1. 打开 https://ai.ocean94.com
2. 个人中心 → 接入Agent → 访问令牌
3. 复制 Token（格式：`FA_xxxxxxxxxxxx`）

## 本地运行

```bash
pip install -r requirements.txt
FOOTPRINTS_TOKEN=FA_xxx python server.py
```

## 部署到 ModelScope

1. 访问 https://www.modelscope.cn/mcp
2. 创建 MCP 服务 → 可托管部署
3. 上传 `server.py` 和 `requirements.txt`
4. 设置环境变量 `FOOTPRINTS_TOKEN`
