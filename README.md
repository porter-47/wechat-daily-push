# 微信公众号每日推送

一个基于 GitHub Actions 的微信公众号模板消息自动推送工具，每天定时为关注者发送天气、诗词、生日提醒等个性化内容。

## 项目概述

| 项目 | 说明 |
|------|------|
| **语言** | Python 3.9 |
| **运行方式** | GitHub Actions 定时任务（每天北京时间 12:00） |
| **推送渠道** | 微信公众号模板消息 |
| **作者** | porter-47 |

## 核心功能

### 1. 天气预报
- 自动获取指定城市的当日天气
- 包含天气状况、最高/最低温度
- 支持全国 300+ 城市（通过 `cityinfo.py` 配置）

### 2. 古诗词推送
- 随机获取古诗词（支持多个 API 源）
- 包含诗词正文和出处
- 飞花令关键词随机选择

### 3. 生日提醒
- 支持公历和农历生日
- 自动计算最近的生日倒计时
- 生日当天发送祝福

### 4. 恋爱纪念日
- 记录在一起的日期
- 自动计算相恋天数

### 5. 智能问候
- 根据时间段自动切换问候语
  - 6:00-12:00：早安问候
  - 12:00-18:00：午安问候
  - 18:00 后：晚安问候

## 文件结构

```
weixin/
├── main.py              # 主程序
├── cityinfo.py          # 城市信息配置（300+ 城市）
├── config.txt           # 用户配置文件（需自行填写）
├── requirements.txt     # Python 依赖
├── .gitignore           # Git 忽略文件
└── .github/
    └── workflows/
        └── weixin.yml   # GitHub Actions 配置
```

## 配置说明

编辑 `config.txt` 文件，填入你的信息：

```json
{
  "app_id": "你的公众号appId",
  "app_secret": "你的公众号appSecret",
  "template_id": "模板消息id",
  "user": ["接收者openid"],
  
  "province": "省份",
  "city": "城市",
  
  "birthday1": {"name": "姓名", "birthday": "2000-01-01"},
  "birthday2": {"name": "姓名", "birthday": "r2000-12-31"},
  
  "love_date": "2022-01-01"
}
```

**配置项说明：**

| 配置项 | 说明 | 示例 |
|--------|------|------|
| app_id | 公众号 appId | wx1234567890 |
| app_secret | 公众号 appSecret | abcdef123456 |
| template_id | 模板消息 ID | xyz123... |
| user | 接收者 openid 列表 | ["openid1", "openid2"] |
| province | 所在省份 | 湖北 |
| city | 所在城市 | 武汉 |
| birthday1/2 | 生日配置 | name + birthday |
| love_date | 恋爱纪念日 | 2022-06-16 |

**农历生日：** 在日期前加 `r` 前缀，如 `"r2000-12-31"`

## 部署步骤

### 1. 准备公众号
- 注册微信公众号（服务号）
- 获取 `app_id` 和 `app_secret`
- 创建模板消息，获取 `template_id`

### 2. Fork 或克隆项目
```bash
git clone https://github.com/porter-47/weixin.git
cd weixin
```

### 3. 修改配置
编辑 `config.txt`，填入你的信息。

### 4. 启用 GitHub Actions
- 进入仓库 Settings → Actions → General
- 选择 "Allow all actions and reusable workflows"
- 保存配置

### 5. 测试运行
- 进入 Actions 页面
- 选择 "weixin" workflow
- 点击 "Run workflow" 手动测试

## 定时任务配置

```yaml
# .github/workflows/weixin.yml
schedule:
  # 北京时间中午 12:00（UTC 4:00）
  - cron: '0 4 * * *'
```

## 模板消息格式

推送内容包含以下字段：

| 字段 | 内容 | 示例 |
|------|------|------|
| first | 问候语 | 早安，今日诗意已送达 |
| keyword1 | 日期+纪念日 | 2026年5月29日 周四 ｜ 相恋第1465天 |
| keyword2 | 天气信息 | 多云 ｜ 18度 ~ 25度 ｜ 武汉 |
| keyword3 | 诗词正文 | 「山重水复疑无路，柳暗花明又一村。」 |
| keyword4 | 诗词出处 | 《游山西村》宋·陆游 |
| keyword5 | 生日提醒 | 距张三生日还有15天 |
| remark | 备注 | （可自定义） |

## 依赖说明

```
requests==2.28.1    # HTTP 请求
zhdate==0.1         # 农历日期处理
```

## 注意事项

1. **公众号类型**：需要服务号才能发送模板消息
2. **模板消息**：需要在公众号后台创建对应字段的模板
3. **用户关注**：接收者需要关注公众号才能收到消息
4. **API 限制**：微信模板消息有每日发送限制
5. **诗词 API**：使用了多个备用源，确保稳定性
6. **配置安全**：`config.txt` 包含敏感信息，请勿公开分享

## 诗词 API 源

| API | 说明 |
|-----|------|
| jinrishici.com | 今日诗词 API |
| saintic.com | 圣子 API |

## 许可证

MIT License

## 作者

- GitHub: [porter-47](https://github.com/porter-47)
- 项目地址: https://github.com/porter-47/weixin
