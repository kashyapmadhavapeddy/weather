import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="AtmosPulse · Live Weather", page_icon="🌦️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif; background-color: #050a14; color: #dce7f7; }
.stApp { background: linear-gradient(135deg, #050a14 0%, #0c1628 50%, #071020 100%); background-attachment: fixed; }
header[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 2rem 3rem 2rem 3rem !important; max-width: 1400px; }
.atmos-title { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 3rem; background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; line-height: 1.1; }
.atmos-sub { font-family: 'Space Mono', monospace; font-size: 0.75rem; color: #475569; letter-spacing: 3px; text-transform: uppercase; margin-top: 4px; }
.mood-banner { border-radius: 16px; padding: 1.2rem 2rem; margin: 1rem 0; display: flex; align-items: center; gap: 1.2rem; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.2rem; box-shadow: 0 4px 24px rgba(0,0,0,0.3); }
.mood-emoji { font-size: 2.5rem; }
.mood-title { font-size: 1.3rem; font-weight: 800; }
.mood-desc { font-size: 0.85rem; font-weight: 400; opacity: 0.85; font-family: 'Space Mono', monospace; margin-top: 2px; }
.score-card { background: linear-gradient(145deg, #0f1d35, #0a1628); border: 1px solid #1e3a5f; border-radius: 20px; padding: 1.8rem; text-align: center; position: relative; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.4); }
.score-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #34d399, #38bdf8, #818cf8); border-radius: 20px 20px 0 0; }
.score-number { font-family: 'Syne', sans-serif; font-size: 4rem; font-weight: 800; line-height: 1; }
.score-label { font-family: 'Space Mono', monospace; font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase; color: #64748b; margin-bottom: 0.5rem; }
.score-verdict { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 600; margin-top: 0.5rem; }
.score-bar-bg { background: #1e3a5f; border-radius: 10px; height: 8px; margin: 0.8rem 0; overflow: hidden; }
.score-bar-fill { height: 8px; border-radius: 10px; }
.best-day-card { background: linear-gradient(145deg, #0f1d35, #0a1628); border: 1px solid #1e3a5f; border-radius: 16px; padding: 1.2rem 1.4rem; box-shadow: 0 4px 24px rgba(0,0,0,0.4); position: relative; overflow: hidden; }
.best-day-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; border-radius: 16px 16px 0 0; }
.best-day-card.sunny::before { background: linear-gradient(90deg, #f59e0b, #fcd34d); }
.best-day-card.rainy::before { background: linear-gradient(90deg, #38bdf8, #818cf8); }
.best-day-card.windy::before { background: linear-gradient(90deg, #34d399, #38bdf8); }
.best-day-title { font-family: 'Space Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; color: #64748b; margin-bottom: 0.4rem; }
.best-day-value { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800; color: #f0f9ff; }
.best-day-sub { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: #94a3b8; margin-top: 0.3rem; }
.metric-card { background: linear-gradient(145deg, #0f1d35, #0a1628); border: 1px solid #1e3a5f; border-radius: 16px; padding: 1.4rem 1.6rem; position: relative; overflow: hidden; transition: transform 0.2s; box-shadow: 0 4px 24px rgba(0,0,0,0.4); }
.metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #38bdf8, #818cf8); border-radius: 16px 16px 0 0; }
.metric-card:hover { transform: translateY(-2px); }
.metric-label { font-family: 'Space Mono', monospace; font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; color: #64748b; margin-bottom: 0.5rem; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 2.4rem; font-weight: 800; color: #f0f9ff; line-height: 1; }
.metric-unit { font-family: 'Space Mono', monospace; font-size: 0.8rem; color: #38bdf8; margin-left: 4px; }
.metric-sub { font-size: 0.78rem; color: #94a3b8; margin-top: 0.4rem; font-family: 'Space Mono', monospace; }
.section-header { font-family: 'Space Mono', monospace; font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase; color: #38bdf8; border-left: 2px solid #38bdf8; padding-left: 0.7rem; margin: 1.8rem 0 1rem 0; }
.alert-danger { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); border-radius: 10px; padding: 0.8rem 1rem; color: #fca5a5; font-family: 'Space Mono', monospace; font-size: 0.78rem; margin-bottom: 0.5rem; }
.alert-warn { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); border-radius: 10px; padding: 0.8rem 1rem; color: #fcd34d; font-family: 'Space Mono', monospace; font-size: 0.78rem; margin-bottom: 0.5rem; }
.alert-ok { background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3); border-radius: 10px; padding: 0.8rem 1rem; color: #6ee7b7; font-family: 'Space Mono', monospace; font-size: 0.78rem; margin-bottom: 0.5rem; }
.stTextInput input { background: #0f1d35 !important; border: 1px solid #1e3a5f !important; border-radius: 10px !important; color: #dce7f7 !important; font-family: 'Space Mono', monospace !important; font-size: 0.9rem !important; }
.stTextInput input:focus { border-color: #38bdf8 !important; box-shadow: 0 0 0 2px rgba(56,189,248,0.2) !important; }
.stButton button { background: linear-gradient(135deg, #0ea5e9, #6366f1) !important; border: none !important; border-radius: 10px !important; color: white !important; font-family: 'Space Mono', monospace !important; font-size: 0.8rem !important; letter-spacing: 1px !important; padding: 0.5rem 1.5rem !important; transition: opacity 0.2s !important; }
.stButton button:hover { opacity: 0.85 !important; }
hr { border-color: #1e3a5f !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #050a14; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 10px; }
.footer { font-family: 'Space Mono', monospace; font-size: 0.65rem; color: #334155; text-align: center; letter-spacing: 2px; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #0f1d35; }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"
FORECAST_URL = f"{BASE_URL}/forecast"
CURRENT_URL  = f"{BASE_URL}/weather"
AIR_URL      = f"{BASE_URL}/air_pollution"

def get_current_weather(city):
    try:
        r = requests.get(CURRENT_URL, params={"q": city, "appid": API_KEY, "units": "metric"}, timeout=8)
        r.raise_for_status(); return r.json()
    except: return None

def get_forecast(city):
    try:
        r = requests.get(FORECAST_URL, params={"q": city, "appid": API_KEY, "units": "metric", "cnt": 40}, timeout=8)
        r.raise_for_status(); return r.json()
    except: return None

def get_air_quality(lat, lon):
    try:
        r = requests.get(AIR_URL, params={"lat": lat, "lon": lon, "appid": API_KEY}, timeout=8)
        r.raise_for_status(); return r.json()
    except: return None

def wind_direction(deg):
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    return dirs[round(deg / 45) % 8]

def aqi_label(aqi):
    labels = {1:("Good","ok"),2:("Fair","ok"),3:("Moderate","warn"),4:("Poor","danger"),5:("Very Poor","danger")}
    return labels.get(aqi, ("Unknown","ok"))

def calculate_weather_score(temp, humidity, wind_spd, vis, aqi, rain):
    score = 100
    if temp > 42: score -= 35
    elif temp > 38: score -= 25
    elif temp > 35: score -= 15
    elif temp < 5: score -= 30
    elif temp < 10: score -= 15
    elif 20 <= temp <= 30: score += 5
    if humidity > 85: score -= 20
    elif humidity > 75: score -= 10
    elif humidity < 20: score -= 10
    elif 40 <= humidity <= 65: score += 5
    if wind_spd > 60: score -= 25
    elif wind_spd > 40: score -= 15
    elif wind_spd > 25: score -= 5
    if vis < 1: score -= 20
    elif vis < 3: score -= 10
    if aqi:
        if aqi >= 5: score -= 25
        elif aqi >= 4: score -= 15
        elif aqi >= 3: score -= 5
    if rain > 7.5: score -= 20
    elif rain > 2.5: score -= 10
    return max(0, min(100, score))

def score_verdict(score):
    if score >= 85: return "🌟 Perfect day to go outside!", "#34d399"
    elif score >= 70: return "😊 Good conditions overall", "#38bdf8"
    elif score >= 55: return "🙂 Fairly pleasant outside", "#818cf8"
    elif score >= 40: return "😐 Manageable but not ideal", "#f59e0b"
    elif score >= 25: return "😟 Stay cautious outdoors", "#f97316"
    else: return "🏠 Better to stay indoors", "#ef4444"

def get_mood(desc, temp, rain, wind_spd, vis, humidity, city_name):
    d = desc.lower()
    if "thunderstorm" in d: return "⛈️", "Thunderstorm Alert!", "Stay indoors — dangerous conditions outside", "rgba(99,102,241,0.15)", "#6366f1"
    elif "snow" in d: return "❄️", "Snowfall Detected!", "Bundle up and drive carefully today", "rgba(186,230,253,0.1)", "#7dd3fc"
    elif rain > 7.5 or "heavy rain" in d: return "🌧️", "Heavy Rain Warning!", "Carry an umbrella — roads may be slippery", "rgba(56,189,248,0.12)", "#38bdf8"
    elif "rain" in d or "drizzle" in d: return "🌦️", "Light Rain Expected", "A light umbrella would be handy today", "rgba(56,189,248,0.08)", "#7dd3fc"
    elif vis < 2 or "fog" in d or "mist" in d or "haze" in d: return "🌫️", "Low Visibility — Fog Alert", "Drive slowly and use fog lights", "rgba(148,163,184,0.1)", "#94a3b8"
    elif temp > 40: return "🔥", "Extreme Heat Warning!", "Stay hydrated and avoid outdoor activity", "rgba(239,68,68,0.12)", "#ef4444"
    elif temp > 35: return "☀️", "Hot Day Ahead!", "Stay hydrated and limit time outdoors", "rgba(245,158,11,0.12)", "#f59e0b"
    elif wind_spd > 50: return "💨", "Strong Winds Today!", "Secure loose objects — gusty conditions", "rgba(52,211,153,0.1)", "#34d399"
    elif humidity > 85: return "💧", "Very Humid Conditions", "Feels sticky outside — stay cool indoors", "rgba(129,140,248,0.1)", "#818cf8"
    elif "clear" in d and temp <= 32: return "🌤️", f"Beautiful Day in {city_name}!", "Perfect weather — enjoy the outdoors!", "rgba(52,211,153,0.1)", "#34d399"
    elif "cloud" in d: return "⛅", "Partly Cloudy Today", "Mild and comfortable — great for a walk", "rgba(100,116,139,0.1)", "#94a3b8"
    else: return "🌡️", "Check Conditions Before Going Out", "Monitor the dashboard for updates", "rgba(56,189,248,0.08)", "#38bdf8"

def get_best_days(df):
    df = df.copy()
    df["date"] = df["datetime"].dt.date
    daily = df.groupby("date").agg(
        max_temp=("temp","max"), min_temp=("temp","min"),
        avg_humidity=("humidity","mean"), max_wind=("wind_kph","max"), total_rain=("rain","sum")
    ).reset_index()
    daily["outdoor_score"] = (
        (daily["total_rain"] == 0).astype(int) * 40 +
        ((daily["max_temp"] >= 18) & (daily["max_temp"] <= 32)).astype(int) * 30 +
        (daily["avg_humidity"] < 70).astype(int) * 20 +
        (daily["max_wind"] < 30).astype(int) * 10
    )
    best_outdoor = daily.loc[daily["outdoor_score"].idxmax(), "date"]
    most_rain    = daily.loc[daily["total_rain"].idxmax(), "date"]
    windiest     = daily.loc[daily["max_wind"].idxmax(), "date"]
    return (
        best_outdoor.strftime("%A, %d %b"),
        most_rain.strftime("%A, %d %b"),
        windiest.strftime("%A, %d %b"),
        round(daily.loc[daily["total_rain"].idxmax(), "total_rain"], 1),
        round(daily.loc[daily["max_wind"].idxmax(), "max_wind"], 1),
    )

def base_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(size=12, color="#38bdf8", family="Space Mono, monospace"), x=0.01),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", family="Space Mono, monospace", size=10),
        xaxis=dict(showgrid=True, gridcolor="#1e3a5f", zeroline=False, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor="#1e3a5f", zeroline=False, tickfont=dict(size=9)),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9)),
    )

# ── HEADER ──
col_title, col_refresh = st.columns([5, 1])
with col_title:
    st.markdown('<div class="atmos-title">🌦 AtmosPulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="atmos-sub">Live Weather Intelligence Dashboard</div>', unsafe_allow_html=True)
with col_refresh:
    st.markdown("<br>", unsafe_allow_html=True)
    refresh_btn = st.button("⟳ Refresh")

if not API_KEY:
    st.markdown('<div class="alert-warn">⚠️ API key not set. Add OPENWEATHER_API_KEY to Streamlit secrets.</div>', unsafe_allow_html=True)

st.markdown("---")

col_search, col_btn = st.columns([4, 1])
with col_search:
    city_input = st.text_input("City", placeholder="Enter a city name (e.g. Hyderabad, Mumbai, London)", label_visibility="collapsed")
with col_btn:
    search_btn = st.button("Search →")

city = city_input.strip() if city_input.strip() else "Hyderabad"

if "last_fetched" not in st.session_state:
    st.session_state.last_fetched = 0
    st.session_state.cached_city = ""

now_ts = time.time()
needs_refresh = refresh_btn or search_btn or st.session_state.cached_city != city or (now_ts - st.session_state.last_fetched) > 1800

if needs_refresh and API_KEY:
    st.session_state.last_fetched = now_ts
    st.session_state.cached_city = city
    with st.spinner("Fetching live data..."):
        current  = get_current_weather(city)
        forecast = get_forecast(city)
    st.session_state.current  = current
    st.session_state.forecast = forecast
else:
    current  = st.session_state.get("current")
    forecast = st.session_state.get("forecast")

if st.session_state.last_fetched:
    ts = datetime.fromtimestamp(st.session_state.last_fetched).strftime("%d %b %Y · %H:%M:%S")
    st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:0.65rem;color:#334155;margin-bottom:0.5rem;">LAST UPDATED · {ts} · AUTO-REFRESHES EVERY 30 MIN</div>', unsafe_allow_html=True)

if API_KEY and needs_refresh and not current:
    st.markdown(f'<div class="alert-danger">❌ Could not find weather data for "{city}". Check the city name.</div>', unsafe_allow_html=True)
    st.stop()

if not current:
    st.markdown('<div class="alert-warn">👆 Enter a city above and click Search — or add your API key to get started.</div>', unsafe_allow_html=True)
    st.stop()

# ── PARSE ──
temp        = round(current["main"]["temp"], 1)
feels       = round(current["main"]["feels_like"], 1)
humidity    = current["main"]["humidity"]
pressure    = current["main"]["pressure"]
vis         = round(current.get("visibility", 0) / 1000, 1)
wind_spd    = round(current["wind"]["speed"] * 3.6, 1)
wind_dir    = wind_direction(current["wind"].get("deg", 0))
desc        = current["weather"][0]["description"].title()
icon        = current["weather"][0]["icon"]
lat         = current["coord"]["lat"]
lon         = current["coord"]["lon"]
city_display = f'{current["name"]}, {current["sys"]["country"]}'
city_name   = current["name"]
sunrise     = datetime.fromtimestamp(current["sys"]["sunrise"]).strftime("%H:%M")
sunset      = datetime.fromtimestamp(current["sys"]["sunset"]).strftime("%H:%M")
clouds      = current.get("clouds", {}).get("all", 0)
rain        = current.get("rain", {}).get("1h", 0)
air_data    = get_air_quality(lat, lon) if API_KEY else None
aqi         = air_data["list"][0]["main"]["aqi"] if air_data else None
aqi_text, aqi_cls = aqi_label(aqi) if aqi else ("N/A", "ok")

# ── CITY HEADER ──
st.markdown(f"""
<div style="display:flex;align-items:center;gap:1rem;margin:1rem 0 0.5rem 0;">
  <div>
    <div style="font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;color:#f0f9ff;">{city_display}</div>
    <div style="font-family:Space Mono,monospace;font-size:0.75rem;color:#64748b;margin-top:2px;">{desc} · {lat:.2f}°N, {lon:.2f}°E</div>
  </div>
  <img src="https://openweathermap.org/img/wn/{icon}@2x.png" style="width:60px;height:60px;filter:drop-shadow(0 0 12px rgba(56,189,248,0.5));">
</div>
""", unsafe_allow_html=True)

# ── MOOD BANNER ──
emoji, mood_title, mood_desc, bg_color, border_color = get_mood(desc, temp, rain, wind_spd, vis, humidity, city_name)
st.markdown(f"""
<div class="mood-banner" style="background:{bg_color};border:1px solid {border_color}40;">
    <div class="mood-emoji">{emoji}</div>
    <div>
        <div class="mood-title" style="color:{border_color};">{mood_title}</div>
        <div class="mood-desc">{mood_desc}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SCORE CARD ──
score = calculate_weather_score(temp, humidity, wind_spd, vis, aqi, rain)
verdict_text, verdict_color = score_verdict(score)
st.markdown('<div class="section-header">TODAY\'S OUTDOOR SCORE</div>', unsafe_allow_html=True)
sc1, sc2, sc3, sc4 = st.columns([1.2, 1, 1, 1])

with sc1:
    st.markdown(f"""
    <div class="score-card">
        <div class="score-label">Outdoor Comfort Score</div>
        <div class="score-number" style="color:{verdict_color};">{score}<span style="font-size:1.5rem;color:#64748b;">/100</span></div>
        <div class="score-bar-bg"><div class="score-bar-fill" style="width:{score}%;background:linear-gradient(90deg,{verdict_color},#38bdf8);"></div></div>
        <div class="score-verdict" style="color:{verdict_color};">{verdict_text}</div>
    </div>""", unsafe_allow_html=True)

with sc2:
    feels_msg = "Uncomfortably hot" if feels > 38 else "Quite warm" if feels > 32 else "Comfortable" if feels > 20 else "Cool" if feels > 10 else "Cold"
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Feels Like</div>
        <div class="metric-value" style="font-size:2rem;">{feels}<span class="metric-unit">°C</span></div>
        <div class="metric-sub">{feels_msg}</div>
    </div>""", unsafe_allow_html=True)

with sc3:
    heat_idx = round(feels - temp, 1)
    hi_label = "Amplified heat" if heat_idx > 3 else "Similar to actual" if abs(heat_idx) <= 1 else "Cooler than actual"
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Heat Effect</div>
        <div class="metric-value" style="font-size:2rem;">{heat_idx:+.1f}<span class="metric-unit">°C</span></div>
        <div class="metric-sub">{hi_label}</div>
    </div>""", unsafe_allow_html=True)

with sc4:
    comfort = "Uncomfortable" if humidity > 75 and temp > 30 else "Sticky" if humidity > 65 else "Comfortable" if humidity < 55 else "Acceptable"
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Comfort Level</div>
        <div class="metric-value" style="font-size:1.6rem;padding-top:0.3rem;">{comfort}</div>
        <div class="metric-sub">Humidity {humidity}% · Temp {temp}°C</div>
    </div>""", unsafe_allow_html=True)

# ── LIVE CONDITIONS ──
st.markdown('<div class="section-header">LIVE CONDITIONS</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    color = "#ef4444" if temp > 35 else "#38bdf8" if temp < 15 else "#34d399"
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Temperature</div><div class="metric-value" style="color:{color};">{temp}<span class="metric-unit">°C</span></div><div class="metric-sub">Feels like {feels}°C</div></div>""", unsafe_allow_html=True)

with c2:
    h_color = "#ef4444" if humidity > 80 else "#38bdf8" if humidity < 30 else "#818cf8"
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Humidity</div><div class="metric-value" style="color:{h_color};">{humidity}<span class="metric-unit">%</span></div><div class="metric-sub">{"Very Humid" if humidity > 75 else "Comfortable" if humidity < 60 else "Moderate"}</div></div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Wind</div><div class="metric-value">{wind_spd}<span class="metric-unit">km/h</span></div><div class="metric-sub">Direction: {wind_dir}</div></div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Visibility</div><div class="metric-value">{vis}<span class="metric-unit">km</span></div><div class="metric-sub">Cloud cover {clouds}%</div></div>""", unsafe_allow_html=True)

with c5:
    aqi_colors = {"ok":"#34d399","warn":"#f59e0b","danger":"#ef4444"}
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Air Quality</div><div class="metric-value" style="color:{aqi_colors[aqi_cls]};">{aqi if aqi else "—"}</div><div class="metric-sub">AQI · {aqi_text}</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4)

with d1:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Pressure</div><div class="metric-value" style="font-size:1.8rem;">{pressure}<span class="metric-unit">hPa</span></div><div class="metric-sub">{"High" if pressure > 1013 else "Low"} pressure system</div></div>""", unsafe_allow_html=True)

with d2:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Sunrise</div><div class="metric-value" style="font-size:2rem;">🌅 {sunrise}</div><div class="metric-sub">Local time</div></div>""", unsafe_allow_html=True)

with d3:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Sunset</div><div class="metric-value" style="font-size:2rem;">🌇 {sunset}</div><div class="metric-sub">Local time</div></div>""", unsafe_allow_html=True)

with d4:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Rainfall (1h)</div><div class="metric-value" style="font-size:1.8rem;">{rain}<span class="metric-unit">mm</span></div><div class="metric-sub">{"Heavy rain" if rain > 7.5 else "Moderate" if rain > 2.5 else "Light / None"}</div></div>""", unsafe_allow_html=True)

# ── ANOMALY ALERTS ──
st.markdown('<div class="section-header">ANOMALY ALERTS</div>', unsafe_allow_html=True)
alerts = []
if temp > 40: alerts.append(("danger","🔴 Extreme Heat Warning: Temperature exceeds 40°C"))
elif temp > 35: alerts.append(("warn","🟡 Heat Advisory: Temperature above 35°C"))
if temp < 5: alerts.append(("danger","🔵 Cold Alert: Near-freezing temperatures"))
if humidity > 85: alerts.append(("warn","💧 High Humidity Alert: Risk of heat stress"))
if wind_spd > 60: alerts.append(("danger","🌪️ Strong Wind Warning: Wind speed above 60 km/h"))
if vis < 1: alerts.append(("danger","🌫️ Low Visibility Alert: Under 1km — fog likely"))
if aqi and aqi >= 4: alerts.append(("danger","☣️ Air Quality Alert: Unhealthy levels detected"))
if not alerts: alerts.append(("ok","✅ All conditions normal — no anomalies detected"))
for cls, msg in alerts:
    st.markdown(f'<div class="alert-{cls}">{msg}</div>', unsafe_allow_html=True)

# ── FORECAST ──
if forecast:
    items = forecast["list"]
    df = pd.DataFrame({
        "datetime":   [datetime.fromtimestamp(i["dt"]) for i in items],
        "temp":       [i["main"]["temp"] for i in items],
        "feels_like": [i["main"]["feels_like"] for i in items],
        "humidity":   [i["main"]["humidity"] for i in items],
        "wind_kph":   [round(i["wind"]["speed"] * 3.6, 1) for i in items],
        "rain":       [i.get("rain", {}).get("3h", 0) for i in items],
        "clouds":     [i.get("clouds", {}).get("all", 0) for i in items],
    })

    # ── BEST DAY PICKER ──
    st.markdown('<div class="section-header">🏆 BEST DAY PICKER · THIS WEEK</div>', unsafe_allow_html=True)
    best_outdoor, most_rain_day, windiest_day, max_rain_mm, max_wind_kph = get_best_days(df)
    bd1, bd2, bd3 = st.columns(3)
    with bd1:
        st.markdown(f"""<div class="best-day-card sunny"><div class="best-day-title">☀️ BEST DAY TO GO OUTSIDE</div><div class="best-day-value">{best_outdoor}</div><div class="best-day-sub">Lowest rain · comfortable temp · calm winds</div></div>""", unsafe_allow_html=True)
    with bd2:
        st.markdown(f"""<div class="best-day-card rainy"><div class="best-day-title">🌧️ MOST LIKELY RAIN DAY</div><div class="best-day-value">{most_rain_day}</div><div class="best-day-sub">Expected rainfall: {max_rain_mm} mm · carry umbrella</div></div>""", unsafe_allow_html=True)
    with bd3:
        st.markdown(f"""<div class="best-day-card windy"><div class="best-day-title">💨 WINDIEST DAY</div><div class="best-day-value">{windiest_day}</div><div class="best-day-sub">Max wind: {max_wind_kph} km/h · secure loose objects</div></div>""", unsafe_allow_html=True)

    # ── TEMPERATURE CHART ──
    st.markdown('<div class="section-header">5-DAY FORECAST · TEMPERATURE TREND</div>', unsafe_allow_html=True)
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=df["datetime"], y=df["temp"], name="Temperature", line=dict(color="#38bdf8", width=2.5), fill="tozeroy", fillcolor="rgba(56,189,248,0.07)", hovertemplate="<b>%{x|%a %d %b %H:%M}</b><br>Temp: %{y:.1f}°C<extra></extra>"))
    fig_temp.add_trace(go.Scatter(x=df["datetime"], y=df["feels_like"], name="Feels Like", line=dict(color="#818cf8", width=1.5, dash="dot"), hovertemplate="<b>%{x|%a %d %b %H:%M}</b><br>Feels Like: %{y:.1f}°C<extra></extra>"))
    layout = base_layout("TEMPERATURE (°C)"); layout["yaxis"]["title"] = "°C"; layout["height"] = 280
    fig_temp.update_layout(**layout)
    st.plotly_chart(fig_temp, use_container_width=True)

    col_h, col_w = st.columns(2)
    with col_h:
        st.markdown('<div class="section-header">HUMIDITY TREND (%)</div>', unsafe_allow_html=True)
        fig_hum = go.Figure()
        fig_hum.add_trace(go.Bar(x=df["datetime"], y=df["humidity"], marker=dict(color=df["humidity"], colorscale=[[0,"#1e3a5f"],[0.5,"#38bdf8"],[1,"#ef4444"]], line=dict(width=0)), hovertemplate="<b>%{x|%a %H:%M}</b><br>Humidity: %{y}%<extra></extra>"))
        layout_h = base_layout(); layout_h["height"] = 240; layout_h["bargap"] = 0.1
        fig_hum.update_layout(**layout_h)
        st.plotly_chart(fig_hum, use_container_width=True)

    with col_w:
        st.markdown('<div class="section-header">WIND SPEED (km/h)</div>', unsafe_allow_html=True)
        fig_wind = go.Figure()
        fig_wind.add_trace(go.Scatter(x=df["datetime"], y=df["wind_kph"], fill="tozeroy", line=dict(color="#34d399", width=2), fillcolor="rgba(52,211,153,0.08)", hovertemplate="<b>%{x|%a %H:%M}</b><br>Wind: %{y:.1f} km/h<extra></extra>"))
        layout_w = base_layout(); layout_w["height"] = 240
        fig_wind.update_layout(**layout_w)
        st.plotly_chart(fig_wind, use_container_width=True)

    if df["rain"].sum() > 0:
        st.markdown('<div class="section-header">RAINFALL FORECAST (mm per 3h)</div>', unsafe_allow_html=True)
        fig_rain = go.Figure()
        fig_rain.add_trace(go.Bar(x=df["datetime"], y=df["rain"], marker=dict(color="rgba(56,189,248,0.7)", line=dict(width=0)), hovertemplate="<b>%{x|%a %H:%M}</b><br>Rain: %{y:.1f} mm<extra></extra>"))
        layout_r = base_layout(); layout_r["height"] = 200; layout_r["bargap"] = 0.05
        fig_rain.update_layout(**layout_r)
        st.plotly_chart(fig_rain, use_container_width=True)

    st.markdown('<div class="section-header">DAILY SUMMARY TABLE</div>', unsafe_allow_html=True)
    df["date"] = df["datetime"].dt.date
    daily = df.groupby("date").agg(Max_Temp=("temp","max"), Min_Temp=("temp","min"), Avg_Humidity=("humidity","mean"), Max_Wind=("wind_kph","max"), Total_Rain=("rain","sum")).round(1).reset_index()
    daily.columns = ["Date","Max Temp (°C)","Min Temp (°C)","Avg Humidity (%)","Max Wind (km/h)","Total Rain (mm)"]
    st.dataframe(daily.style.format({"Max Temp (°C)":"{:.1f}","Min Temp (°C)":"{:.1f}","Avg Humidity (%)":"{:.0f}","Max Wind (km/h)":"{:.1f}","Total Rain (mm)":"{:.1f}"}), use_container_width=True, hide_index=True)

st.markdown('<div class="footer">ATMOSPULSE · POWERED BY OPENWEATHERMAP API · BUILT WITH STREAMLIT · AUTO-REFRESH EVERY 30 MIN</div>', unsafe_allow_html=True)