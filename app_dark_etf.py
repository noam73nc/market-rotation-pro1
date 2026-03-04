import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

try:
    from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
    AGGRID_AVAILABLE = True
except ImportError:
    AGGRID_AVAILABLE = False

st.set_page_config(
    page_title="MarketRotation Pro",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Theme palettes
THEMES = {
    "dark": {
        "bg": "#0b0f1a", "bg2": "#111827", "bg3": "#1a2236",
        "border": "#1f2d42", "border2": "#263347",
        "text": "#e2e8f5", "muted": "#8899b0",
        "title": "#f1f5f9", "date_color": "#94a3b8",
        "price_color": "#f1f5f9", "sec_hdr": "#f1f5f9",
        "ticker_color": "#e2e8f0", "name_color": "#94a3b8",
        "th_color": "#94b8d8", "td_color": "#eef2f8",
        "row_hover": "#0f1929", "row_even": "#0c1520",
        "link_color": "#7dd3fc", "link_hover": "#fff",
        "stocks_color": "#a0b4c8", "stocks_hover": "#60a5fa",
        "pill_pos_bg": "rgba(34,197,94,0.15)", "pill_pos_fg": "#4ade80",
        "pill_neg_bg": "rgba(239,68,68,0.15)",  "pill_neg_fg": "#f87171",
        "pill_neu_bg": "rgba(100,116,139,0.12)", "pill_neu_fg": "#94a3b8",
        "pos": "#4ade80", "neg": "#f87171", "neu": "#8899aa",
        "btn_bg": "#1a2236", "btn_fg": "#3b82f6", "btn_border": "#263347",
        "ag_root": "#0b0f1a", "ag_header": "#111827",
        "ag_border": "#1f2d42", "ag_hdr_color": "#94b8d8",
        "ag_row": "#0b0f1a", "ag_row_even": "#0c1520",
        "ag_hover": "#0f1929", "ag_cell": "#eef2f8", "ag_icon": "#4a6080",
        "ag_tkr": "#7dd3fc",  "ag_name": "#c8d8e8", "ag_stocks": "#a0b4c8",
        "ag_pos": "#4ade80", "ag_neg": "#f87171", "ag_neu": "#64748b",
        "scatter_bg": "#0b0f1a", "scatter_grid": "#1e2d42",
        "scatter_zero": "#334155", "scatter_tick": "#64748b",
        "scatter_title": "#94b8d8", "scatter_font": "#c8d8e8",
        "scatter_hover_bg": "#0f172a", "scatter_hover_border": "#334155",
        "scatter_legend": "#94b8d8",
        "vix_low": "#22c55e", "vix_normal": "#f1f5f9",
        "vix_elev": "#f59e0b", "vix_high": "#ef4444",
        "chg_pos": "#4ade80", "chg_neg": "#f87171",
        "sub_hdr": "#94b8d8", "update_txt": "#334155",
        "footer": "#1e293b",
    },
    "light": {
        "bg": "#f8fafc", "bg2": "#ffffff", "bg3": "#f1f5f9",
        "border": "#e2e8f0", "border2": "#cbd5e1",
        "text": "#0f172a", "muted": "#64748b",
        "title": "#0f172a", "date_color": "#475569",
        "price_color": "#0f172a", "sec_hdr": "#0f172a",
        "ticker_color": "#0f172a", "name_color": "#334155",
        "th_color": "#334155", "td_color": "#1e293b",
        "row_hover": "#f1f5f9", "row_even": "#f8fafc",
        "link_color": "#2563eb", "link_hover": "#1d4ed8",
        "stocks_color": "#475569", "stocks_hover": "#2563eb",
        "pill_pos_bg": "rgba(22,163,74,0.12)", "pill_pos_fg": "#15803d",
        "pill_neg_bg": "rgba(220,38,38,0.10)",  "pill_neg_fg": "#b91c1c",
        "pill_neu_bg": "rgba(100,116,139,0.10)", "pill_neu_fg": "#64748b",
        "pos": "#16a34a", "neg": "#dc2626", "neu": "#94a3b8",
        "btn_bg": "#ffffff", "btn_fg": "#2563eb", "btn_border": "#bfdbfe",
        "ag_root": "#ffffff", "ag_header": "#f8fafc",
        "ag_border": "#e2e8f0", "ag_hdr_color": "#334155",
        "ag_row": "#ffffff", "ag_row_even": "#f8fafc",
        "ag_hover": "#f1f5f9", "ag_cell": "#1e293b", "ag_icon": "#94a3b8",
        "ag_tkr": "#2563eb", "ag_name": "#334155", "ag_stocks": "#475569",
        "ag_pos": "#16a34a", "ag_neg": "#dc2626", "ag_neu": "#94a3b8",
        "scatter_bg": "#ffffff", "scatter_grid": "#f1f5f9",
        "scatter_zero": "#cbd5e1", "scatter_tick": "#64748b",
        "scatter_title": "#334155", "scatter_font": "#334155",
        "scatter_hover_bg": "#0f172a", "scatter_hover_border": "#334155",
        "scatter_legend": "#64748b",
        "vix_low": "#16a34a", "vix_normal": "#0f172a",
        "vix_elev": "#d97706", "vix_high": "#dc2626",
        "chg_pos": "#16a34a", "chg_neg": "#dc2626",
        "sub_hdr": "#64748b", "update_txt": "#64748b",
        "footer": "#94a3b8",
    }
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --bg:      #0b0f1a;
  --bg2:     #111827;
  --bg3:     #1a2236;
  --border:  #1f2d42;
  --border2: #263347;
  --text:    #e2e8f5;
  --muted:   #8899b0;
  --accent:  #3b82f6;
  --pos:     #22c55e;
  --neg:     #ef4444;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'JetBrains Mono', monospace;
}
[data-testid="stSidebar"] { background: var(--bg2) !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"], .stDeployButton { display: none; }
[data-testid="stMainBlockContainer"] { padding: 0 2rem 2rem !important; max-width: 100% !important; }

.stButton > button {
  background: var(--bg3) !important;
  color: var(--accent) !important;
  border: 1px solid var(--border2) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 11px !important;
  border-radius: 6px !important;
  padding: 5px 14px !important;
}
.stButton > button:hover {
  background: var(--accent) !important;
  color: #fff !important;
}

/* PAGE HEADER */
.page-header {
  padding: 28px 0 18px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 22px;
}
.page-title {
  font-family: 'Syne', sans-serif;
  font-size: 30px;
  font-weight: 800;
  color: #f1f5f9;
  letter-spacing: -0.5px;
}
.page-sub {
  font-size: 11px;
  color: var(--muted);
  margin-top: 5px;
}
.page-date {
  font-family: 'Syne', sans-serif;
  font-size: 17px;
  font-weight: 700;
  color: #94a3b8;
  margin-top: 14px;
}

/* MARKET CARDS */
.cards-row {
  display: flex;
  gap: 10px;
  margin-bottom: 26px;
  flex-wrap: wrap;
}
.mkt-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 16px;
  flex: 1;
  min-width: 130px;
}
.mkt-card-label {
  font-size: 10px;
  color: var(--muted);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.mkt-card-label a { color: inherit; text-decoration: none; }
.mkt-card-price {
  font-family: 'Syne', sans-serif;
  font-size: 21px;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 10px;
}
.mkt-pills { display: flex; gap: 6px; flex-wrap: wrap; }
.pill {
  display: inline-flex; align-items: center; gap: 3px;
  padding: 3px 9px; border-radius: 20px;
  font-size: 11px; font-weight: 500;
}
.pill-pos { background: rgba(34,197,94,0.15); color: #4ade80; }
.pill-neg { background: rgba(239,68,68,0.15); color: #f87171; }
.pill-neu { background: rgba(100,116,139,0.12); color: #94a3b8; }
.pill-lbl { font-size: 9px; opacity: .65; margin-right: 1px; }

/* VIX CARD */
.vix-price-low    { color: #22c55e; }
.vix-price-normal { color: #f1f5f9; }
.vix-price-elev   { color: #f59e0b; }
.vix-price-high   { color: #ef4444; }
.vix-bar-track {
  height: 5px; border-radius: 3px; position: relative;
  background: linear-gradient(to right, #22c55e 0 25%, #3b82f6 25% 50%, #f59e0b 50% 75%, #ef4444 75%);
  margin: 10px 0 4px;
}
.vix-dot {
  position: absolute; top: -4px;
  width: 12px; height: 12px; border-radius: 50%;
  background: #fff; border: 2px solid #0b0f1a;
  transform: translateX(-50%);
}
.vix-labels {
  display: flex; justify-content: space-between;
  font-size: 9px; color: var(--muted);
}
.vix-status {
  font-size: 10px; font-weight: 600; letter-spacing: 1px;
  text-transform: uppercase; margin-top: 5px;
}
.vs-low    { color: #22c55e; }
.vs-normal { color: #94a3b8; }
.vs-elev   { color: #f59e0b; }
.vs-high   { color: #ef4444; }

/* SECTION HEADERS */
.sec-hdr {
  font-family: 'Syne', sans-serif;
  font-size: 15px; font-weight: 700;
  color: #f1f5f9;
  margin: 26px 0 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}

/* GAINER CARDS */
.sub-hdr {
  font-size: 9px; color: var(--muted);
  letter-spacing: 1.5px; text-transform: uppercase;
  margin: 14px 0 7px;
}
.gc {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 8px; padding: 9px 11px;
  margin-bottom: 5px; display: flex; align-items: center; gap: 9px;
}
.gc-badge {
  min-width: 34px; height: 20px; border-radius: 4px;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 600;
}
.gc-info { flex: 1; }
.gc-ticker { font-size: 12px; font-weight: 600; color: #e2e8f0; }
.gc-name   { font-size: 10px; color: var(--muted); margin-top: 1px; }
.gc-right  { text-align: right; }
.gc-price  { font-size: 11px; color: #c9d1e0; }
.gc-chg    { font-size: 11px; font-weight: 500; }

/* RS BADGE COLORS */
.b100,.b95  { background:#064e3b; color:#34d399; }
.b90,.b85   { background:#065f46; color:#6ee7b7; }
.b80,.b75   { background:#14532d; color:#86efac; }
.b70,.b65   { background:#1a3a0f; color:#a3e635; }
.b60,.b55   { background:#431407; color:#fb923c; }
.b50,.b45,.b40,.b35,.b30,.b25,.b20,.b15,.b10,.b5 { background:#450a0a; color:#f87171; }

/* TABLE */
.pos { color:#4ade80; font-weight:500; }
.neg { color:#f87171; font-weight:500; }
.neu { color:#8899aa; }
.blue a { color:#7dd3fc; text-decoration:none; font-weight:700; }
.blue a:hover { color:#fff; }
.gray { color:#c8d8e8; }
.stocks a { color:#a0b4c8; text-decoration:none; margin-right:8px; }
.stocks a:hover { color:#60a5fa; }
.tbl-wrap { overflow-x:auto; border:1px solid var(--border); border-radius:8px; }
.dtbl { width:100%; border-collapse:collapse; font-size:11.5px; }
.dtbl th {
  background:var(--bg2); color:#94b8d8; font-size:9.5px; font-weight:700;
  letter-spacing:1px; text-transform:uppercase; padding:8px 10px;
  text-align:right; border-bottom:2px solid var(--border); white-space:nowrap;
}
.dtbl th.l { text-align:left; }
.dtbl td {
  padding:7px 10px; border-bottom:1px solid #111827;
  text-align:right; color:#eef2f8; font-size:12px; white-space:nowrap;
}
.dtbl td.l { text-align:left; }
.dtbl td.c { text-align:center; }
.dtbl tr:hover td { background:#0f1929; }
.dtbl tr:nth-child(even) td { background:#0c1520; }
.dtbl tr:nth-child(even):hover td { background:#0f1929; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════
INDUSTRY_LEADERS = [
    ("SMH",  "Semiconductor",        ["NVDA","TSM","AVGO"]),
    ("SOXX", "Semiconductor(iShares)",["NVDA","AVGO","AMD"]),
    ("IGV",  "Software",             ["MSFT","ORCL","CRM"]),
    ("FDN",  "Internet",             ["META","AMZN","GOOGL"]),
    ("CIBR", "Cybersecurity",        ["PANW","CRWD","FTNT"]),
    ("BOTZ", "Robotics & AI",        ["ISRG","ABB","FANUY"]),
    ("AIQ",  "AI & Tech",            ["NVDA","MSFT","GOOGL"]),
    ("ROBO", "Robotics",             ["IRBT","ISRG","BRKS"]),
    ("QTUM", "Quantum Tech",         ["IBM","IONQ","RGTI"]),
    ("FFTY", "IBD50",                ["MU","PACS","ANAB"]),
    ("ARKK", "ARK Innovation",       ["TSLA","COIN","ROKU"]),
    ("ARKQ", "ARK Autonomous",       ["TSLA","UUUU","KTOS"]),
    ("ARKX", "ARK Space",            ["AJRD","KTOS","RKLB"]),
    ("ARKG", "ARK Genomics",         ["RXRX","TDOC","VCYT"]),
    ("IBIT", "Bitcoin ETF",          ["MSTR","COIN","CLSK"]),
    ("BITO", "Bitcoin Futures",      ["MSTR","RIOT","MARA"]),
    ("BLOK", "Blockchain",           ["MSTR","COIN","SQ"]),
    ("WGMI", "Crypto Miners",        ["MARA","RIOT","CLSK"]),
    ("XOP",  "Oil & Gas Exp.",       ["VG","TPL","XOM"]),
    ("USO",  "Oil Fund",             ["XOM","CVX","COP"]),
    ("TAN",  "Solar",                ["NXT","ENPH","FSLR"]),
    ("FAN",  "Wind Energy",          ["ENLT","VWS","EDPR"]),
    ("ICLN", "Clean Energy",         ["BE","NXT","FSLR"]),
    ("URA",  "Uranium",              ["CCJ","OKLO","UEC"]),
    ("IBB",  "Biotechnology",        ["GILD","AMGN","VRTX"]),
    ("XBI",  "Biotech (SPDR)",       ["MRNA","BNTX","REGN"]),
    ("IHI",  "Med. Devices",         ["ABT","ISRG","BSX"]),
    ("IHF",  "Health Facilities",    ["UNH","CI","CVS"]),
    ("KRE",  "Regional Bank",        ["BPOP","MTB","CFG"]),
    ("KIE",  "Insurance",            ["AIG","MET","PRU"]),
    ("IAI",  "Broker-Dealers",       ["GS","MS","SCHW"]),
    ("ITA",  "Aerospace",            ["GE","RTX","BA"]),
    ("XAR",  "Aerospace (SPDR)",     ["HEI","TDG","AXON"]),
    ("IYT",  "Transportation",       ["UPS","UNP","FDX"]),
    ("JETS", "Global Jets",          ["DAL","UAL","LUV"]),
    ("BOAT", "Marine Shipping",      ["FRO","MATX","STNG"]),
    ("POWR", "Power-Grid",           ["GEV","PWR","NEE"]),
    ("COPX", "Copper Miners",        ["FCX","SCCO","TECK"]),
    ("GDX",  "Gold Miners",          ["AEM","NEM","AU"]),
    ("SIL",  "Silver Miners",        ["WPM","PAAS","CDE"]),
    ("GLD",  "Gold",                 ["NEM","AEM","WPM"]),
    ("SLV",  "Silver",               ["WPM","PAAS","CDE"]),
    ("PALL", "Palladium",            ["SBSW","SIL","IMPUY"]),
    ("DBA",  "Agriculture",          ["ADM","BG","INGR"]),
    ("DBB",  "Base Metals",          ["FCX","AA","NUE"]),
    ("SLX",  "Steel",                ["RIO","BHP","VALE"]),
    ("MOO",  "Agribusiness",         ["DE","ZTS","CTVA"]),
    ("WOOD", "Timber",               ["WY","SW","IP"]),
    ("PEJ",  "Leisure",              ["WBD","LYV","UAL"]),
    ("XRT",  "Retail",               ["CASY","VVV","PSMT"]),
    ("KARS", "Electric Cars",        ["BMW","TSLA","RIVN"]),
    ("ITB",  "Home Construct.",      ["DHI","LEN","PHM"]),
    ("XHB",  "Homebuilders",         ["DHI","LEN","NVR"]),
    ("EEM",  "Emerging Markets",     ["TSM","BABA","VALE"]),
    ("FXI",  "China",                ["BABA","JD","BIDU"]),
    ("EWZ",  "Brazil",               ["VALE","ITUB","PBR"]),
    ("INDA", "India",                ["INFY","HDB","WIT"]),
    ("IEV",  "Europe",               ["ASML","SAP","LVMUY"]),
    ("KWEB", "China Internet",       ["BABA","JD","BIDU"]),
    ("ISRA", "Israel",               ["NICE","CHKP","TEVA"]),
    ("LIT",  "Lithium & Battery",    ["ALB","SQM","LTHM"]),
    ("UFO",  "Space",                ["MAXR","IRDM","RKLB"]),
    ("IPO",  "IPO ETF",              ["ABNB","COIN","RBLX"]),
    ("GRNY", "Green Energy",         ["ENPH","FSLR","RUN"]),
]

SECTOR_LEADERS = [
    ("RSPG","Energy"), ("RSPN","Industrials"), ("RSPU","Utilities"),
    ("RSPR","Real Estate"), ("RSPC","Comm Svcs"), ("RSPM","Materials"),
    ("RSPS","Cons Stpl"), ("RSPH","Health Care"), ("RSPD","Cons Disc"),
    ("RSPT","Technology"), ("RSPF","Financials"),
]

BENCHMARK = "SPY"

# (yahoo_ticker, display_label, card_name, kind)
MARKET_CARDS = [
    ("SPY",     "SPY",  "S&P 500",       "index"),
    ("QQQ",     "QQQ",  "Nasdaq 100",    "index"),
    ("IWM",     "IWM",  "Russell 2000",  "index"),
    ("^DJI",    "DJI",  "Dow Jones",     "index"),
    ("BTC-USD", "BTC",  "Bitcoin",       "crypto"),
    ("ETH-USD", "ETH",  "Ethereum",      "crypto"),
    ("^VIX",    "VIX",  "Volatility",    "vix"),
]

# ═══════════════════════════════════════
# DATA FETCHING
# ═══════════════════════════════════════
@st.cache_data(ttl=300)
def fetch_prices(tickers):
    end   = datetime.today()
    start = end - timedelta(days=300)
    syms  = list(set(tickers + [BENCHMARK]))
    try:
        raw    = yf.download(syms, start=start, end=end, auto_adjust=True, progress=False, threads=True)
        prices = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw
        return prices.dropna(how="all")
    except Exception as e:
        st.error(f"Fetch error: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=120)
def fetch_market_cards():
    end = datetime.today()
    start = end - timedelta(days=40)
    out = {}
    for yahoo_tkr, display, name, kind in MARKET_CARDS:
        try:
            raw   = yf.download(yahoo_tkr, start=start, end=end, auto_adjust=True, progress=False)
            close = raw["Close"].dropna()
            if len(close) < 2:
                continue
            price   = float(close.iloc[-1])
            day_pct = float((close.iloc[-1] / close.iloc[-2] - 1) * 100)
            wk_pct  = float((close.iloc[-1] / close.iloc[-6]  - 1) * 100) if len(close) >= 6  else None
            mth_pct = float((close.iloc[-1] / close.iloc[-22] - 1) * 100) if len(close) >= 22 else None
            out[display] = {
                "name": name, "kind": kind, "price": price,
                "day_pct": day_pct, "wk_pct": wk_pct, "mth_pct": mth_pct,
            }
        except Exception:
            continue
    return out

@st.cache_data(ttl=300)
def fetch_scatter_data(tickers):
    """Fetch data for scatter: price $ chg from open + volume run rate vs 20d avg"""
    end   = datetime.today()
    start = end - timedelta(days=60)
    out   = {}
    for tkr in tickers:
        try:
            raw = yf.download(tkr, start=start, end=end,
                              auto_adjust=True, progress=False)
            if raw.empty or len(raw) < 22:
                continue
            close  = raw["Close"].dropna()
            volume = raw["Volume"].dropna() if "Volume" in raw.columns else None
            # Price $ change from open proxy: today close minus yesterday close
            if len(close) >= 2:
                price_chg = float(close.iloc[-1] - close.iloc[-2])
            else:
                continue
            price = float(close.iloc[-1])
            # Run Rate 20 Day = today's volume / avg volume of last 20 days * 100
            # e.g. 200 = today volume is 2x the 20-day average
            if volume is not None and len(volume) >= 21:
                today_vol = float(volume.iloc[-1])
                avg_vol   = float(volume.iloc[-21:-1].mean())  # 20 days excluding today
                run_rate  = round((today_vol / avg_vol) * 100, 1) if avg_vol > 0 else None
            else:
                run_rate = None
            out[tkr] = {
                "price_chg_open": round(price_chg, 2),
                "run_rate_20d":   run_rate,
                "price":          price,
            }
        except Exception:
            continue
    return out

# ═══════════════════════════════════════
# RS CALCULATION
# ═══════════════════════════════════════
def percentrank_series(series, window):
    def _pr(arr):
        if len(arr) < window:
            return np.nan
        return float(np.sum(arr[:-1] < arr[-1])) / (window - 1) * 100.0
    return series.rolling(window).apply(_pr, raw=True)

def compute_all(prices):
    results = {}
    if BENCHMARK not in prices.columns:
        return results
    spy = prices[BENCHMARK].dropna()
    for tkr in prices.columns:
        if tkr == BENCHMARK:
            continue
        close = prices[tkr].dropna()
        if len(close) < 30:
            continue
        idx   = close.index.intersection(spy.index)
        c, s  = close.loc[idx], spy.loc[idx]
        ratio = c / s
        pr21  = percentrank_series(ratio, 21)
        clean = pr21.dropna()
        if clean.empty:
            continue
        latest_rs = clean.iloc[-1]
        score = max(5, min(100, int(round(latest_rs / 5) * 5)))

        def chg(ser, lb):
            cl = ser.dropna()
            return (cl.iloc[-1] / cl.iloc[-1 - lb] - 1) * 100 if len(cl) > lb else np.nan

        def rs_chg(r, lb):
            cl = r.dropna()
            return (cl.iloc[-1] / cl.iloc[-1 - lb] - 1) * 100 if len(cl) > lb else np.nan

        results[tkr] = {
            "score": score, "raw_rs": latest_rs,
            "price": float(c.iloc[-1]),
            "day_pct":  chg(c, 1),      "wk_pct":  chg(c, 5),      "mth_pct":  chg(c, 21),
            "rs_day":   rs_chg(ratio,1), "rs_wk":   rs_chg(ratio,5), "rs_mth":   rs_chg(ratio,21),
            "pct_52w":  (c.iloc[-1] / c.rolling(252, min_periods=len(c)).max().iloc[-1] - 1) * 100,
        }
    return results

# ═══════════════════════════════════════
# HTML HELPERS
# ═══════════════════════════════════════
def badge(score):
    s = max(5, min(100, int(round(score / 5) * 5)))
    return f'<span class="gc-badge b{s}">{s}</span>'

def pct_html(val, d=2):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '<span class="neu">–</span>'
    cls = "pos" if val > 0.005 else ("neg" if val < -0.005 else "neu")
    pfx = "+" if val > 0.005 else ""
    return f'<span class="{cls}">{pfx}{val:.{d}f}%</span>'

def pfmt(val, crypto=False):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "–"
    if crypto and val > 1000:
        return f"${val:,.0f}"
    return f"${val:,.2f}"

def pill_html(val, label):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return ""
    cls = "pill-pos" if val > 0.005 else ("pill-neg" if val < -0.005 else "pill-neu")
    arrow = "▲" if val > 0.005 else ("▼" if val < -0.005 else "")
    pfx   = "+" if val > 0.005 else ""
    return f'<span class="pill {cls}"><span class="pill-lbl">{label}</span>{arrow}{pfx}{val:.2f}%</span>'

def tv(sym):
    return f"https://www.tradingview.com/chart/?symbol={sym}"

# ═══════════════════════════════════════
# RENDER: MARKET CARDS
# ═══════════════════════════════════════
def render_market_cards(card_data):
    parts = []
    for _, display, name, kind in MARKET_CARDS:
        d = card_data.get(display)
        if not d:
            parts.append(f'<div class="mkt-card"><div class="mkt-card-label">{display}</div><div class="mkt-card-price">–</div></div>')
            continue

        price   = d["price"]
        day_pct = d.get("day_pct")
        wk_pct  = d.get("wk_pct")
        is_crypto = (kind == "crypto")

        if kind == "vix":
            if   price < 15: vcls, vstatus = "vix-price-low",    "LOW"
            elif price < 20: vcls, vstatus = "vix-price-normal", "NORMAL"
            elif price < 30: vcls, vstatus = "vix-price-elev",   "ELEVATED"
            else:            vcls, vstatus = "vix-price-high",   "HIGH"
            pct_raw  = min(98, max(2, int(price / 40 * 100)))
            scls = "vs-" + vstatus.lower().replace("elevated", "elev")
            parts.append(
                f'<div class="mkt-card">'
                f'  <div class="mkt-card-label">VIX · Volatility</div>'
                f'  <div class="mkt-card-price {vcls}">{price:.2f}</div>'
                f'  <div class="vix-bar-track"><div class="vix-dot" style="left:{pct_raw}%"></div></div>'
                f'  <div class="vix-labels"><span>Low</span><span>Mod</span><span>Elev</span><span>High</span></div>'
                f'  <div class="vix-status {scls}">{vstatus}</div>'
                f'</div>'
            )
        else:
            price_str = pfmt(price, crypto=is_crypto)
            parts.append(
                f'<div class="mkt-card">'
                f'  <div class="mkt-card-label"><a href="{tv(display)}" target="_blank">{display} · {name}</a></div>'
                f'  <div class="mkt-card-price">{price_str}</div>'
                f'  <div class="mkt-pills">{pill_html(day_pct,"Day")}{pill_html(wk_pct,"Wk")}</div>'
                f'</div>'
            )

    st.markdown('<div class="cards-row">' + "".join(parts) + '</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════
# RENDER: GAINER CARD
# ═══════════════════════════════════════
def gainer_card(tkr, d, key):
    v = d.get(key, np.nan)
    if v is None or (isinstance(v, float) and np.isnan(v)):
        s, col = "–", "#64748b"
    else:
        s   = f"+{v:.2f}%" if v >= 0 else f"{v:.2f}%"
        col = "#4ade80"     if v >= 0 else "#f87171"
    return (
        f'<div class="gc">{badge(d["score"])}'
        f'<div class="gc-info">'
        f'  <div class="gc-ticker">{tkr}</div>'
        f'  <div class="gc-name">{d.get("name","")}</div>'
        f'</div>'
        f'<div class="gc-right">'
        f'  <div class="gc-price">{pfmt(d.get("price", np.nan))}</div>'
        f'  <div class="gc-chg" style="color:{col}">{s}</div>'
        f'</div></div>'
    )

# ═══════════════════════════════════════
# RENDER: TABLE
# ═══════════════════════════════════════
def render_table_html(rows, extra=False):
    hdr = '<th class="l">MAJOR STOCKS</th>' if extra else ""
    out = (
        f'<div class="tbl-wrap"><table class="dtbl"><thead><tr>'
        f'<th class="c">RS</th><th class="l">TICKER</th><th class="l">NAME</th>'
        f'<th>DAY %</th><th>WK %</th><th>MTH %</th>'
        f'<th>RS DAY</th><th>RS WK</th><th>RS MTH</th><th>52W HIGH</th>'
        f'{hdr}</tr></thead><tbody>'
    )
    for row in rows:
        tkr, name, d, *rest = row
        stocks = rest[0] if rest else []
        s_links = "".join(
            f'<a href="{tv(s)}" target="_blank">{s}</a>' for s in stocks
        )
        sx  = f'<td class="l stocks">{s_links}</td>' if extra else ""
        out += (
            f'<tr>'
            f'<td class="c">{badge(d["score"])}</td>'
            f'<td class="l blue"><a href="{tv(tkr)}" target="_blank">{tkr}</a></td>'
            f'<td class="l gray">{name}</td>'
            f'<td>{pct_html(d.get("day_pct"))}</td>'
            f'<td>{pct_html(d.get("wk_pct"))}</td>'
            f'<td>{pct_html(d.get("mth_pct"))}</td>'
            f'<td>{pct_html(d.get("rs_day"),1)}</td>'
            f'<td>{pct_html(d.get("rs_wk"),1)}</td>'
            f'<td>{pct_html(d.get("rs_mth"),1)}</td>'
            f'<td>{pct_html(d.get("pct_52w"))}</td>'
            f'{sx}</tr>'
        )
    out += "</tbody></table></div>"
    return out

def rows_to_df(rows, extra=False):
    records = []
    for row in rows:
        tkr, name, d, *rest = row
        stocks = rest[0] if rest else []
        rec = {
            "RS":       d.get("score", 0),
            "Ticker":   tkr,
            "Name":     name,
            "DAY %":    round(d.get("day_pct") or 0, 2),
            "WK %":     round(d.get("wk_pct")  or 0, 2),
            "MTH %":    round(d.get("mth_pct") or 0, 2),
            "RS DAY":   round(d.get("rs_day")  or 0, 2),
            "RS WK":    round(d.get("rs_wk")   or 0, 2),
            "RS MTH":   round(d.get("rs_mth")  or 0, 2),
            "52W HIGH": round(d.get("pct_52w") or 0, 2),
        }
        if extra:
            rec["Stocks"] = "  ".join(stocks)
        records.append(rec)
    return pd.DataFrame(records)

def render_table(rows, extra=False, height=400, t=None):
    if t is None: t = THEMES['dark']
    df = rows_to_df(rows, extra)
    if not AGGRID_AVAILABLE:
        st.markdown(render_table_html(rows, extra), unsafe_allow_html=True)
        return

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, sortable=True, filter=True,
                                wrapText=False, autoHeight=False, minWidth=60)

    rs_style = JsCode("""function(p){
        var v=p.value;
        if(v>=90)return{backgroundColor:'#064e3b',color:'#34d399',fontWeight:'600',textAlign:'center'};
        if(v>=75)return{backgroundColor:'#14532d',color:'#86efac',fontWeight:'600',textAlign:'center'};
        if(v>=60)return{backgroundColor:'#1a3a0f',color:'#a3e635',fontWeight:'600',textAlign:'center'};
        if(v>=50)return{backgroundColor:'#431407',color:'#fb923c',fontWeight:'600',textAlign:'center'};
        return{backgroundColor:'#450a0a',color:'#f87171',fontWeight:'600',textAlign:'center'};
    }""")

    pct_style = JsCode("""function(p){
        var v=p.value;
        if(v>0.005) return{color:'#4ade80',fontWeight:'500',textAlign:'right'};
        if(v<-0.005)return{color:'#f87171',fontWeight:'500',textAlign:'right'};
        return{color:'#64748b',textAlign:'right'};
    }""")

    tkr_rdr = JsCode("""class TkrR {
        init(p){
            this.gui=document.createElement('a');
            this.gui.innerText=p.value;
            this.gui.href='https://www.tradingview.com/chart/?symbol='+p.value;
            this.gui.target='_blank';
            this.gui.style.cssText='color:#7dd3fc;text-decoration:none;font-weight:700;cursor:pointer';
        }
        getGui(){return this.gui;}
        refresh(){return false;}
    }""")

    _sc = t["ag_stocks"]
    stk_rdr = JsCode("class StkR{init(p){this.gui=document.createElement('span');if(!p.value)return;var sc='"+_sc+"';p.value.split('  ').forEach(function(s){s=s.trim();if(!s)return;var a=document.createElement('a');a.innerText=s;a.href='https://www.tradingview.com/chart/?symbol='+s;a.target='_blank';a.style.cssText='color:'+sc+';text-decoration:none;margin-right:10px;cursor:pointer';this.gui.appendChild(a);},this);}getGui(){return this.gui;}refresh(){return false;}}")

    gb.configure_column("RS",       width=65,  pinned="left", cellStyle=rs_style)
    gb.configure_column("Ticker",   width=90,  pinned="left", cellRenderer=tkr_rdr)
    gb.configure_column("Name",     width=170, cellStyle={"color": "#c8d8e8"})
    gb.configure_column("DAY %",    width=90,  type=["numericColumn"], cellStyle=pct_style)
    gb.configure_column("WK %",     width=90,  type=["numericColumn"], cellStyle=pct_style)
    gb.configure_column("MTH %",    width=95,  type=["numericColumn"], cellStyle=pct_style)
    gb.configure_column("RS DAY",   width=95,  type=["numericColumn"], cellStyle=pct_style)
    gb.configure_column("RS WK",    width=90,  type=["numericColumn"], cellStyle=pct_style)
    gb.configure_column("RS MTH",   width=95,  type=["numericColumn"], cellStyle=pct_style)
    gb.configure_column("52W HIGH", width=105, type=["numericColumn"], cellStyle=pct_style)
    if extra:
        gb.configure_column("Stocks", width=180, cellRenderer=stk_rdr)

    gb.configure_grid_options(rowHeight=32, headerHeight=36,
                              suppressMovableColumns=False, domLayout="normal")

    AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=GridUpdateMode.NO_UPDATE,
        allow_unsafe_jscode=True,
        height=height,
        theme="alpine",
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=False,
        custom_css={
            ".ag-root-wrapper":      {"background-color": "#0b0f1a", "border": "1px solid #1f2d42", "border-radius": "8px"},
            ".ag-header":            {"background-color": "#111827", "border-bottom": "2px solid #1f2d42"},
            ".ag-header-cell-label": {"color": "#94b8d8", "font-size": "10px", "font-weight": "700",
                                      "letter-spacing": "1px", "text-transform": "uppercase",
                                      "font-family": "JetBrains Mono, monospace"},
            ".ag-row":               {"background-color": "#0b0f1a", "border-bottom": "1px solid #111827",
                                      "font-family": "JetBrains Mono, monospace", "font-size": "12px"},
            ".ag-row-even":          {"background-color": "#0c1520"},
            ".ag-row:hover":         {"background-color": "#0f1929 !important"},
            ".ag-cell":              {"color": "#eef2f8"},
            ".ag-icon":              {"color": "#4a6080"},
        },
    )

# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════
def render_scatter(rs_all, scatter_data, tickers, t=None):
    if t is None: t = THEMES['dark']
    import plotly.graph_objects as go

    x_vals, y_vals, labels, colors, hover = [], [], [], [], []

    for tkr in tickers:
        sd = scatter_data.get(tkr)
        rd = rs_all.get(tkr)
        if not sd or not rd:
            continue
        xv = sd.get("price_chg_open")
        yv = sd.get("run_rate_20d")
        if xv is None or yv is None:
            continue
        x_vals.append(xv)
        y_vals.append(yv)
        labels.append(tkr)
        score = rd.get("score", 50)
        # Color by RS score: green=high, red=low, like reference image
        if score >= 80:   col = "#2563eb"   # strong blue
        elif score >= 60: col = "#7c9dbf"   # medium blue
        elif score >= 50: col = "#c084fc"   # purple/pink
        else:             col = "#f472b6"   # pink/red (lagging)
        colors.append(col)
        hover.append(
            f"<b>{tkr}</b><br>"
            f"Name: {rd.get('name','')}<br>"
            f"RS Score: {score}<br>"
            f"$ Chg from Open: {'+' if xv>=0 else ''}{xv:.2f}<br>"
            f"Run Rate 20D: ${yv:.0f}M<br>"
            f"Price: ${sd.get('price',0):.2f}"
        )

    if not x_vals:
        st.warning("No scatter data available.")
        return

    fig = go.Figure()

    # Zero lines
    fig.add_hline(y=0, line_color=t["scatter_zero"], line_width=1)
    fig.add_vline(x=0, line_color=t["scatter_zero"], line_width=1)

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals,
        mode="markers+text",
        text=labels,
        textposition="top right",
        textfont=dict(size=11, color=colors, family="JetBrains Mono"),
        marker=dict(
            size=8,
            color=colors,
            opacity=0.85,
            line=dict(width=0),
        ),
        hovertemplate="%{customdata}<extra></extra>",
        customdata=hover,
    ))

    fig.update_layout(
        plot_bgcolor=t["scatter_bg"],
        paper_bgcolor=t["scatter_bg"],
        font=dict(family="JetBrains Mono", size=11, color=t["scatter_font"]),
        xaxis=dict(
            title=dict(text="Price $ Change from Open", font=dict(color=t["scatter_title"], size=12)),
            gridcolor=t["scatter_grid"],
            zerolinecolor=t["scatter_zero"],
            zerolinewidth=2,
            tickfont=dict(color=t["scatter_tick"]),
        ),
        yaxis=dict(
            title=dict(text="Run Rate – 20 Day (% of avg volume, 100=normal)", font=dict(color=t["scatter_title"], size=12)),
            gridcolor=t["scatter_grid"],
            zerolinecolor=t["scatter_zero"],
            zerolinewidth=2,
            tickfont=dict(color=t["scatter_tick"]),
        ),
        margin=dict(l=60, r=30, t=30, b=60),
        height=620,
        hoverlabel=dict(
            bgcolor=t["scatter_hover_bg"],
            bordercolor=t["scatter_hover_border"],
            font=dict(color="#f1f5f9", size=12, family="JetBrains Mono"),
        ),
        showlegend=False,
    )

    # Color legend annotation
    fig.add_annotation(
        x=1, y=1.02, xref="paper", yref="paper",
        text="🔵 RS≥80 &nbsp;&nbsp; 🩵 RS 60-79 &nbsp;&nbsp; 🟣 RS 50-59 &nbsp;&nbsp; 🩷 RS<50",
        showarrow=False, font=dict(size=10, color=t["scatter_legend"]),
        align="right",
    )

    st.plotly_chart(fig, use_container_width=True)

def main():
    now      = datetime.now()
    now_str  = now.strftime("%H:%M:%S")
    date_str = now.strftime("%A, %B %d, %Y").replace(" 0", " ")

    # Header
    st.markdown(
        f'<div class="page-header">'
        f'  <div class="page-title">MarketRotation Pro</div>'
        f'  <div class="page-sub">Sector &amp; Theme Rotation Tracker &middot; Built with Python &amp; Claude AI By Noam73nc</div>'
        f'  <div class="page-date">{date_str}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # ── Theme toggle ──
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    c1, c2, c3 = st.columns([1, 1, 8])
    with c1:
        if st.button("⟳  Refresh"):
            st.cache_data.clear()
            st.rerun()
    with c2:
        label = "☀️  Light" if st.session_state.theme == "dark" else "🌙  Dark"
        if st.button(label):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()
    with c3:
        st.markdown(
            f'<div style="font-size:10px;color:#334155;padding-top:8px">Last update: {now_str} · cache 5min</div>',
            unsafe_allow_html=True
        )

    t = THEMES[st.session_state.theme]

    # ── Inject dynamic theme CSS ──
    st.markdown(f"""<style>
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stMainBlockContainer"]{{
    background:{t['bg']}!important;color:{t['text']}!important;
}}
.page-title{{color:{t['title']}}}
.page-date{{color:{t['date_color']}}}
.mkt-card{{background:{t['bg2']};border-color:{t['border']}}}
.mkt-card-price{{color:{t['price_color']}}}
.sec-hdr{{color:{t['sec_hdr']};border-color:{t['border']}}}
.gc{{background:{t['bg2']};border-color:{t['border']}}}
.gc-ticker{{color:{t['ticker_color']}}}
.gc-price{{color:{t['name_color']}}}
.sub-hdr{{color:{t['sub_hdr']}}}
.pos{{color:{t['pos']}}}
.neg{{color:{t['neg']}}}
.neu{{color:{t['neu']}}}
.blue a{{color:{t['link_color']}}}
.blue a:hover{{color:{t['link_hover']}}}
.gray{{color:{t['name_color']}}}
.stocks a{{color:{t['stocks_color']}}}
.stocks a:hover{{color:{t['stocks_hover']}}}
.pill-pos{{background:{t['pill_pos_bg']};color:{t['pill_pos_fg']}}}
.pill-neg{{background:{t['pill_neg_bg']};color:{t['pill_neg_fg']}}}
.pill-neu{{background:{t['pill_neu_bg']};color:{t['pill_neu_fg']}}}
.dtbl th{{background:{t['bg2']};color:{t['th_color']};border-bottom:2px solid {t['border']}}}
.dtbl td{{color:{t['td_color']};border-bottom:1px solid {t['border']}}}
.dtbl tr:hover td{{background:{t['row_hover']}}}
.dtbl tr:nth-child(even) td{{background:{t['row_even']}}}
.dtbl tr:nth-child(even):hover td{{background:{t['row_hover']}}}
.tbl-wrap{{border-color:{t['border']}}}
.stButton>button{{background:{t['btn_bg']}!important;color:{t['btn_fg']}!important;border-color:{t['btn_border']}!important}}
</style>""", unsafe_allow_html=True)

    # Market cards (SPY QQQ IWM DJI BTC ETH VIX)
    with st.spinner(""):
        card_data = fetch_market_cards()
    render_market_cards(card_data)

    # Fetch ETF prices & compute RS
    all_t = list({t[0] for t in INDUSTRY_LEADERS} | {t[0] for t in SECTOR_LEADERS})
    with st.spinner("Fetching ETF data..."):
        prices = fetch_prices(all_t)
    if prices.empty:
        st.error("Could not load data. Try refreshing.")
        return

    with st.spinner("Computing Relative Strength..."):
        rs_all = compute_all(prices)

    name_map = {t[0]: t[1] for t in INDUSTRY_LEADERS}
    name_map.update({t[0]: t[1] for t in SECTOR_LEADERS})
    for tkr, d in rs_all.items():
        d["name"] = name_map.get(tkr, tkr)

    # ── TABS ──
    tab1, tab2 = st.tabs(["📊  Tables", "🔵  Scatter — Price vs Volume"])

    with tab1:
      st.markdown('<div class="sec-hdr">Sector Leaders</div>', unsafe_allow_html=True)
      cl, cr = st.columns([1, 3], gap="medium")

      with cl:
        av = dict(rs_all)
        dg = sorted(av.items(), key=lambda x: x[1].get("rs_day") or -999, reverse=True)[:3]
        wg = sorted(av.items(), key=lambda x: x[1].get("rs_wk")  or -999, reverse=True)[:3]
        html  = '<div class="sub-hdr">Top 3 RS Gainers · Daily</div>'
        for tkr, d in dg:
            html += gainer_card(tkr, d, "day_pct")
        html += '<div class="sub-hdr">Top 3 RS Gainers · Weekly</div>'
        for tkr, d in wg:
            html += gainer_card(tkr, d, "wk_pct")
        st.markdown(html, unsafe_allow_html=True)

      with cr:
        sr = [(tkr, name, rs_all[tkr]) for tkr, name in SECTOR_LEADERS if tkr in rs_all]
        sr.sort(key=lambda x: x[2].get("raw_rs", 0), reverse=True)
        render_table(sr, extra=False, height=385, t=t)

      # Industry Leaders
      st.markdown('<div class="sec-hdr">Industry Leaders</div>', unsafe_allow_html=True)
      ir = [(tkr, name, rs_all[tkr], stks) for tkr, name, stks in INDUSTRY_LEADERS if tkr in rs_all]
      ir.sort(key=lambda x: x[2].get("raw_rs", 0), reverse=True)
      render_table(ir, extra=True, height=650, t=t)

      st.markdown(
          f'<div style="font-size:9px;color:#1e293b;text-align:right;margin-top:12px">Yahoo Finance · {now_str}</div>',
          unsafe_allow_html=True
      )

    with tab2:
      st.markdown('<div class="sec-hdr">ETF Scatter — Price Change vs Run Rate</div>', unsafe_allow_html=True)
      st.markdown('<div style="font-size:11px;color:#64748b;margin-bottom:14px">X-axis: price $ change from yesterday close &nbsp;|&nbsp; Y-axis: today volume ÷ 20-day avg volume × 100 &nbsp;|&nbsp; 100 = normal volume &nbsp;|&nbsp; Color = RS score</div>', unsafe_allow_html=True)
      all_tickers = list({t[0] for t in INDUSTRY_LEADERS} | {t[0] for t in SECTOR_LEADERS})
      with st.spinner("Loading scatter data..."):
          scatter_data = fetch_scatter_data(all_tickers)
      render_scatter(rs_all, scatter_data, all_tickers)

    st.markdown(
        '<div style="margin-top:32px;padding:14px 18px;border-radius:8px;'
        'background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.18);'
        'font-size:11px;color:#94a3b8;line-height:1.7">'
        '⚠️ <b style="color:#f87171">Disclaimer:</b> '
        'MarketRotation Pro is intended for educational and informational purposes only. '
        'Nothing displayed in this application constitutes financial advice, investment recommendations, '
        'or an offer to buy or sell any security. Past performance is not indicative of future results. '
        'Always consult a licensed financial advisor before making any investment decisions. Use at your own risk.'
        '</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
