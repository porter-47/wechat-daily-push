# 微信公众号每日推送

[![GitHub stars](https://img.shields.io/github/stars/porter-47/wechat-daily-push?style=social)](https://github.com/porter-47/wechat-daily-push/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/porter-47/wechat-daily-push?style=social)](https://github.com/porter-47/wechat-daily-push/network/members)
[![GitHub issues](https://img.shields.io/github/issues/porter-47/wechat-daily-push)](https://github.com/porter-47/wechat-daily-push/issues)
[![GitHub license](https://img.shields.io/github/license/porter-47/wechat-daily-push)](https://github.com/porter-47/wechat-daily-push/blob/main/LICENSE)

> 🌅 每天早上 8 点，为你的公众号关注者送上天气、诗词、生日提醒

一个基于 GitHub Actions 的微信公众号模板消息自动推送工具，零服务器、零成本，开箱即用。

## ✨ 功能特性

- 🌤️ **天气预报** — 自动获取当日天气、温度
- 📜 **古诗词推送** — 每日随机诗词，附带飞花令
- 🎂 **生日提醒** — 支持公历和农历，自动倒计时
- ❤️ **恋爱纪念日** — 自动计算相恋天数
- 🌅 **智能问候** — 根据时间自动切换早/午/晚安

## 📸 效果展示

<!-- 请替换为你的实际截图 -->
<!-- ![推送效果](./screenshots/demo.png) -->

```
┌─────────────────────────────────────┐
│  早安，今日诗意已送达                │
├─────────────────────────────────────┤
│  2026年5月30日 周六 | 相恋第5000天  │
│  晴转多云 | 19℃ ~ 27℃ | 上海      │
│  「山重水复疑无路，柳暗花明又一村。」│
│  《游山西村》宋·陆游                │
│  距张三生日还有15天                 │
└─────────────────────────────────────┘
```

## 🚀 快速开始

### 1. Fork 项目

点击右上角 **Fork** 按钮，将项目复制到你的账号下。

### 2. 配置公众号信息

编辑 `config.txt` 文件：

```json
{
  "app_id": "你的公众号appId",
  "app_secret": "你的公众号appSecret",
  "template_id": "模板消息id",
  "user": ["接收者openid"],
  
  "province": "浙江",
  "city": "台州",
  
  "birthday1": {"name": "张三", "birthday": "1995-06-15"},
  "birthday2": {"name": "李四", "birthday": "r2000-12-31"},
  
  "love_date": "2010-01-01"
}
```

### 3. 启用 GitHub Actions

1. 进入仓库 **Settings** → **Actions** → **General**
2. 选择 **Allow all actions and reusable workflows**
3. 保存配置

### 4. 测试运行

1. 进入 **Actions** 页面
2. 选择 **weixin** workflow
3. 点击 **Run workflow** 手动测试

## 📋 配置说明

| 配置项 | 说明 | 示例 |
|--------|------|------|
| app_id | 公众号 appId | wx1234567890 |
| app_secret | 公众号 appSecret | abcdef123456 |
| template_id | 模板消息 ID | xyz123... |
| user | 接收者 openid 列表 | ["openid1"] |
| province | 所在省份 | 浙江 |
| city | 所在城市 | 上海 |
| birthday1/2 | 生日配置 | name + birthday |
| love_date | 恋爱纪念日 | 2010-01-01 |

**农历生日：** 在年份前加 `r` 前缀，如 `"r2000-12-31"`

## 📁 项目结构

```
wechat-daily-push/
├── main.py              # 主程序
├── cityinfo.py          # 城市信息配置（300+ 城市）
├── config.txt           # 用户配置文件
├── requirements.txt     # Python 依赖
├── LICENSE              # MIT 许可证
└── .github/
    └── workflows/
        └── weixin.yml   # GitHub Actions 配置
```

## ⏰ 推送时间

- **计划时间：** 北京时间 8:00
- **实际收到：** 8:00 - 8:15 之间
- **说明：** GitHub Actions 调度可能有 5-15 分钟延迟

## 📝 模板消息格式

| 字段 | 内容 | 示例 |
|------|------|------|
| first | 问候语 | 早安，今日诗意已送达 |
| keyword1 | 日期+纪念日 | 2026年5月30日 周六 ｜ 相恋第5000天 |
| keyword2 | 天气信息 | 晴转多云 ｜ 19℃ ~ 27℃ ｜ 台州 |
| keyword3 | 诗词正文 | 「山重水复疑无路，柳暗花明又一村。」 |
| keyword4 | 诗词出处 | 《游山西村》宋·陆游 |
| keyword5 | 生日提醒 | 距张三生日还有15天 |

## 🔧 高级配置

### 修改推送时间

编辑 `.github/workflows/weixin.yml`：

```yaml
schedule:
  # 北京时间 8:00（UTC 0:00）
  - cron: '0 0 * * *'
  
  # 北京时间 12:00（UTC 4:00）
  # - cron: '0 4 * * *'
  
  # 北京时间 20:00（UTC 12:00）
  # - cron: '0 12 * * *'
```

### 添加多个接收者

```json
{
  "user": ["openid1", "openid2", "openid3"]
}
```

## ❓ 常见问题

### Q: 如何获取 app_id 和 app_secret？

A: 登录 [微信公众平台](https://mp.weixin.qq.com/) → 开发 → 基本配置

### Q: 如何获取 template_id？

A: 公众号后台 → 功能 → 模板消息 → 添加模板

### Q: 如何获取用户 openid？

A: 公众号后台 → 用户管理 → 用户列表

### Q: 为什么收不到消息？

A: 
1. 确认用户已关注公众号
2. 确认模板消息字段正确
3. 查看 Actions 运行日志

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[MIT License](LICENSE)

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star 支持一下！

[![Star History Chart](https://api.star-history.com/svg?repos=porter-47/wechat-daily-push&type=Date)](https://star-history.com/#porter-47/wechat-daily-push&Date)

---

**作者：** [porter-47](https://github.com/porter-47)
