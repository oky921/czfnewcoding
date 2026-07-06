from __future__ import annotations

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "晴",
    1: "大部晴朗",
    2: "局部多云",
    3: "阴",
    45: "雾",
    48: "冻雾",
    51: "小毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    80: "阵雨",
    95: "雷暴",
}


async def geocode_city(city: str) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            GEOCODE_URL,
            params={
                "name": city,
                "count": 1,
                "language": "zh",
                "format": "json",
            },
        )
        resp.raise_for_status()
        data = resp.json()

    results = data.get("results") or []
    if not results:
        raise ValueError(f"没有找到城市: {city}")
    return results[0]


@mcp.tool()
async def get_weather(city: str, days: int = 1) -> str:
    days = max(1, min(days, 7))
    place = await geocode_city(city)

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            FORECAST_URL,
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min",
                "timezone": "auto",
                "forecast_days": days,
            },
        )
        resp.raise_for_status()
        data = resp.json()

    current = data["current"]
    daily = data["daily"]
    code = current.get("weather_code")
    desc = WEATHER_CODES.get(code, f"未知天气({code})")

    lines = [
        f"城市: {place['name']}, {place.get('country', '')}",
        f"当前天气: {desc}",
        f"当前温度: {current['temperature_2m']}°C",
        f"体感温度: {current['apparent_temperature']}°C",
        f"风速: {current['wind_speed_10m']} km/h",
        "",
        "未来天气:",
    ]

    for i in range(len(daily["time"])):
        lines.append(
            f"{daily['time'][i]}: "
            f"{daily['temperature_2m_min'][i]}°C ~ {daily['temperature_2m_max'][i]}°C"
        )

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()