import random
from time import time, localtime
import cityinfo
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os
import json
import logging

# ============================================================
# 日志配置
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# 飞花令关键词 & 天气图标
# ============================================================

FEIHUA_KEYWORDS = [
    "花", "月", "风", "云", "春", "山", "水", "雪",
    "梦", "酒", "剑", "心", "星", "雨", "柳", "梅",
    "竹", "兰", "菊", "莲", "鹤", "龙", "凤", "雁",
    "江", "海", "日", "天", "夜", "秋", "红", "翠",
]

WEATHER_LABEL = {
    "晴": "晴", "多云": "多云", "阴": "阴",
    "雨": "雨", "雪": "雪", "小雨": "小雨",
    "中雨": "中雨", "大雨": "大雨", "暴雨": "暴雨",
    "雷阵雨": "雷阵雨", "雾": "雾", "霾": "霾",
    "风": "风", "晴转多云": "晴转多云", "阵雨": "阵雨",
}

ELEGANT_COLORS = [
    "#4A90D9", "#5B8C5A", "#C9A96E", "#A6808A",
    "#6B8E9B", "#8B7355", "#7A9B7E", "#B8956A",
    "#5F7D8E", "#9B7E6B", "#6E8B5E", "#A08B7B",
    "#7A8B8B", "#8E7A6B", "#5E8B8B", "#9B8B7A",
]


def get_color():
    return random.choice(ELEGANT_COLORS)


def get_weather_label(weather_text):
    for k, v in WEATHER_LABEL.items():
        if k in weather_text:
            return v
    return "天气"


# ============================================================
# 诗词 API
# ============================================================

def get_poetry():
    """多 API 源获取诗词，同时随机飞花令关键词"""
    keyword = random.choice(FEIHUA_KEYWORDS)

    api_sources = [
        {
            "url": "http://v1.jinrishici.com/all.json",
            "parse": lambda d: (d["content"], f"《{d['origin']}》{d['author']}"),
            "method": "get",
        },
        {
            "url": "https://hub.saintic.com/openservice/sentence/all.json",
            "parse": lambda d: (
                d["data"].get("content") or d["data"].get("name", ""),
                f"{d['data'].get('name','')} · {d['data'].get('author','佚名')}",
            ),
            "method": "get",
        },
    ]

    for src in api_sources:
        try:
            if src["method"] == "get":
                r = get(src["url"], headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
            if r.status_code == 200:
                verse, origin = src["parse"](r.json())
                if verse:
                    return verse.strip(), origin, keyword
        except Exception as e:
            logger.warning(f"诗词 API 请求失败: {e}")
            continue

    logger.warning("所有诗词 API 均失败，使用默认诗词")
    return "山重水复疑无路，柳暗花明又一村。", "《游山西村》宋·陆游", "山"


# ============================================================
# 微信 API
# ============================================================

def get_access_token(config):
    """获取微信 access_token"""
    app_id = config["app_id"]
    app_secret = config["app_secret"]
    post_url = (
        "https://api.weixin.qq.com/cgi-bin/token"
        "?grant_type=client_credential&appid={}&secret={}"
        .format(app_id, app_secret)
    )
    try:
        response = get(post_url, timeout=10)
        response.raise_for_status()
        result = response.json()
        if "access_token" not in result:
            logger.error(f"获取 access_token 失败: {result}")
            sys.exit(1)
        return result["access_token"]
    except Exception as e:
        logger.error(f"获取 access_token 异常: {e}")
        sys.exit(1)


def get_weather(province, city):
    """获取天气信息"""
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        logger.error(f"找不到城市: {province} - {city}")
        sys.exit(1)

    t = int(round(time() * 1000))
    headers = {
        "Referer": f"http://www.weather.com.cn/weather1d/{city_id}.shtml",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        )
    }
    url = f"http://d1.weather.com.cn/dingzhi/{city_id}.html?_={t}"
    
    try:
        response = get(url, headers=headers, timeout=10)
        response.encoding = "utf-8"
        response_data = response.text.split(";")[0].split("=")[-1]
        response_json = json.loads(response_data)
        weatherinfo = response_json["weatherinfo"]
        weather = weatherinfo["weather"]
        temp = weatherinfo["temp"].rstrip("℃")
        tempn = weatherinfo["tempn"].rstrip("℃")
    except Exception as e:
        logger.warning(f"获取天气失败: {e}")
        weather, temp, tempn = "未知", "--", "--"
    
    return weather, temp, tempn


def get_birthday(birthday, year, today):
    """计算生日倒计时"""
    birthday_year = birthday.split("-")[0]
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        year_date = ZhDate(year, r_mouth, r_day).to_datetime().date()
        birthday_month = year_date.month
        birthday_day = year_date.day
    else:
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        year_date = date(year, birthday_month, birthday_day)

    if today > year_date:
        if birthday_year[0] == "r":
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


# ============================================================
# 模板消息发送
# ============================================================

def send_message(to_user, access_token, city_name, weather, max_temperature,
                 min_temperature, verse, origin, keyword, config):
    """发送微信模板消息"""
    week_list = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]

    # ---- 组装各字段 ----

    # first: 问候语
    hour = localtime().tm_hour
    if 6 <= hour < 12:
        greeting = "早安，今日诗意已送达"
    elif 12 <= hour < 18:
        greeting = "午安，偷得浮生半日闲"
    else:
        greeting = "晚安，枕边诗意入梦来"

    # keyword1: 日期 + 纪念日
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    date_str = f"{year}年{month}月{day}日 {week}  |  相恋第{love_days}天"

    # keyword2: 天气（合并城市+天气+温度）
    label = get_weather_label(weather)
    weather_str = f"{label}  |  {min_temperature}度 ~ {max_temperature}度  |  {city_name}"

    # keyword3: 诗词正文
    verse_str = f"「{verse}」"

    # keyword4: 出处
    origin_str = origin

    # keyword5: 最近的生日提醒
    birth_nearest = None
    birth_nearest_days = 9999
    for k, v in config.items():
        if k.startswith("birth"):
            try:
                d = int(get_birthday(v["birthday"], year, today))
                if d < birth_nearest_days:
                    birth_nearest_days = d
                    birth_nearest = v
            except Exception as e:
                logger.warning(f"计算生日失败: {e}")
    
    if birth_nearest:
        if birth_nearest_days == 0:
            love_str = f"今天是{birth_nearest['name']}的生日，生日快乐！"
        else:
            love_str = f"距{birth_nearest['name']}生日还有{birth_nearest_days}天"
    else:
        love_str = ""

    # remark
    remark_str = ""

    # ---- 发送 ----
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "",
        "topcolor": "#5B8C5A",
        "data": {
            "first":    {"value": greeting,     "color": "#7A8B8B"},
            "keyword1": {"value": date_str,     "color": "#6B8E9B"},
            "keyword2": {"value": weather_str,  "color": "#4A90D9"},
            "keyword3": {"value": verse_str,    "color": "#5B8C5A"},
            "keyword4": {"value": origin_str,   "color": "#A6808A"},
            "keyword5": {"value": love_str,     "color": "#C9A96E"},
            "remark":   {"value": remark_str,   "color": "#8B7355"},
        }
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        )
    }
    
    try:
        resp = post(
            url=f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}",
            headers=headers,
            json=data,
            timeout=10
        ).json()

        errcode = resp.get("errcode", -1)
        if errcode == 0:
            logger.info(f"推送成功 → {to_user}")
        elif errcode == 40037:
            logger.error("推送失败：模板id不正确")
        elif errcode == 40036:
            logger.error("推送失败：模板id为空")
        elif errcode == 40003:
            logger.error("推送失败：微信号不正确")
        else:
            logger.error(f"推送失败: {resp}")
    except Exception as e:
        logger.error(f"发送消息异常: {e}")


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = json.loads(f.read())
    except FileNotFoundError:
        logger.error("推送失败，config.txt 不存在")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"推送失败，config.txt 格式错误: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"读取配置文件失败: {e}")
        sys.exit(1)

    accessToken = get_access_token(config)
    users = config["user"]
    province, city = config["province"], config["city"]
    weather, max_temp, min_temp = get_weather(province, city)
    verse, origin, keyword = get_poetry()

    logger.info(f"开始推送，共 {len(users)} 个用户")
    for user in users:
        send_message(user, accessToken, city, weather, max_temp, min_temp,
                     verse, origin, keyword, config)
    logger.info("推送完成")
