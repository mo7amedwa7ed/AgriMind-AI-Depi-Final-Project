"""AgriMind AI design system — "Dark Technology + Neon Green".

Palette, typography and the full CSS theme live here.  ``build_css(lang)`` returns a
<style> block; it is injected once per run by ``agrimind_ui.apply_theme``.
"""
from __future__ import annotations

# ---- palette (from the design brief) -------------------------------------- #
BG = "#07130F"
BG2 = "#0D1F18"
CARD = "#122820"
GREEN = "#16A34A"
LIME = "#A3E635"
TEXT = "#F1F5F2"
MUTED = "#9CA3AF"
BORDER = "#244234"

# Semantic accents used only for the irrigation levels (Low / Medium / High)
AMBER = "#FBBF24"
WATER = "#38BDF8"

FONT_EN = "Inter, Figtree, 'Segoe UI', sans-serif"
FONT_AR = "Cairo, 'IBM Plex Sans Arabic', 'Segoe UI', Tahoma, sans-serif"

_FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800"
    "&family=Cairo:wght@400;500;600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;500;600"
    "&display=swap');"
)

_CSS = """
__IMPORT__
:root{
  --bg:__BG__; --bg2:__BG2__; --card:__CARD__; --green:__GREEN__; --lime:__LIME__;
  --text:__TEXT__; --muted:__MUTED__; --border:__BORDER__; --font:__FONT__;
  --radius:18px; --shadow:0 18px 40px -18px rgba(0,0,0,.65);
}
html,body,.stApp{color-scheme:dark;}
.stApp{
  background:
    radial-gradient(900px 480px at 85% -10%, rgba(163,230,53,.10), transparent 60%),
    radial-gradient(700px 420px at -5% 15%, rgba(22,163,74,.16), transparent 55%),
    var(--bg) !important;
  color:var(--text); font-family:var(--font); direction:__DIR__;
}
.stApp p,.stApp li,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6,
.stApp [data-testid="stMarkdownContainer"],.stApp [data-baseweb],.stApp input,.stApp textarea,
.stApp button,.stApp table{font-family:var(--font) !important;}
.stApp p,.stApp li{color:var(--text);}
h1,h2,h3,h4{color:var(--text) !important; letter-spacing:-.01em;}

/* ---- chrome cleanup ---- */
#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"]{display:none !important;}
[data-testid="stHeader"]{background:transparent !important;}
.block-container,[data-testid="stMainBlockContainer"]{
  max-width:1180px; padding:2.2rem 2rem 4rem !important;}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:10px}
::-webkit-scrollbar-track{background:transparent}

/* ---- sidebar ---- */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,var(--bg2),var(--bg)) !important;
  border-inline-end:1px solid var(--border);}
[data-testid="stSidebar"] > div:first-child{padding-top:.4rem;}
.ag-brand{display:flex;align-items:center;gap:.8rem;padding:.4rem .2rem 1.1rem;}
.ag-logo{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;font-size:1.4rem;
  background:linear-gradient(135deg,var(--green),var(--lime));box-shadow:0 0 24px rgba(163,230,53,.35);}
.ag-brand-name{font-weight:800;font-size:1.2rem;line-height:1.1;color:var(--text);}
.ag-brand-tag{font-size:.72rem;color:var(--muted);margin-top:.15rem;line-height:1.3;}
.ag-side-label{font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
  margin:1.1rem .3rem .5rem;font-weight:600;}
[data-testid="stPageLink-NavLink"]{
  border:1px solid transparent;border-radius:12px;padding:.55rem .75rem;transition:all .18s ease;
  background:transparent;}
[data-testid="stPageLink-NavLink"] p{color:var(--text) !important;font-weight:500;font-size:.93rem;}
[data-testid="stPageLink-NavLink"]:hover{background:rgba(163,230,53,.07);border-color:var(--border);
  transform:translateX(calc(var(--dx,1) * 2px));}
[data-testid="stPageLink-NavLink"][aria-current="page"]{
  background:linear-gradient(90deg,rgba(22,163,74,.28),rgba(163,230,53,.08));
  border-color:rgba(163,230,53,.45);}
[data-testid="stPageLink-NavLink"][aria-current="page"] p{color:var(--lime) !important;font-weight:700;}
.ag-status{display:flex;align-items:center;justify-content:space-between;gap:.6rem;
  padding:.45rem .2rem;font-size:.8rem;color:var(--muted);}
.ag-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-inline-end:.45rem;
  background:var(--lime);box-shadow:0 0 10px var(--lime);}
.ag-dot.off{background:#ef4444;box-shadow:0 0 10px #ef4444;}
.ag-ok{color:var(--lime);font-weight:600}.ag-bad{color:#f87171;font-weight:600}

/* language switch (radio -> segmented pills) */
[data-testid="stSidebar"] div[role="radiogroup"]{
  background:var(--card);border:1px solid var(--border);border-radius:12px;padding:4px;gap:4px;
  display:flex;width:100%;}
[data-testid="stSidebar"] div[role="radiogroup"] label{
  flex:1;justify-content:center;border-radius:9px;padding:.35rem .6rem;margin:0;cursor:pointer;
  transition:all .15s ease;}
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child{display:none;}
[data-testid="stSidebar"] div[role="radiogroup"] label p{font-weight:600;font-size:.85rem;color:var(--muted) !important;}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){
  background:linear-gradient(135deg,var(--green),#22c55e);}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{color:#fff !important;}

/* ---- hero ---- */
.ag-hero{position:relative;overflow:hidden;border:1px solid var(--border);border-radius:26px;
  padding:2.6rem 2.4rem;background:
   radial-gradient(520px 260px at 90% 0%,rgba(163,230,53,.18),transparent 65%),
   linear-gradient(145deg,var(--card),var(--bg2));box-shadow:var(--shadow);animation:agUp .6s ease both;}
.ag-badge{display:inline-flex;align-items:center;gap:.45rem;padding:.35rem .8rem;border-radius:999px;
  border:1px solid rgba(163,230,53,.4);background:rgba(163,230,53,.08);color:var(--lime);
  font-size:.78rem;font-weight:600;margin-bottom:1rem;}
.ag-hero-title{font-size:clamp(1.7rem,3.4vw,2.7rem);font-weight:800;line-height:1.2;margin:0 0 .9rem;color:var(--text);}
.ag-hero-title b{color:var(--lime);}
.ag-hero-text{color:var(--muted);font-size:1.02rem;line-height:1.75;max-width:760px;margin:0;}
.ag-panel{border:1px solid var(--border);border-radius:20px;padding:1.3rem 1.4rem;
  background:rgba(7,19,15,.55);backdrop-filter:blur(6px);animation:agUp .7s ease both;}
.ag-panel h4{margin:0 0 .6rem;font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted) !important;}

/* ---- sections ---- */
.ag-section{margin:2.6rem 0 1.1rem;}
.ag-section h2{font-size:1.5rem;font-weight:800;margin:0;}
.ag-section p{color:var(--muted);margin:.3rem 0 0;font-size:.95rem;}
.ag-section .bar{width:44px;height:4px;border-radius:4px;margin-top:.7rem;
  background:linear-gradient(90deg,var(--lime),var(--green));}

/* ---- cards ---- */
.ag-fcard{border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem 1.4rem 1.2rem;
  background:linear-gradient(160deg,var(--card),var(--bg2));min-height:250px;
  transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease;animation:agUp .6s ease both;}
.ag-fcard:hover{transform:translateY(-4px);border-color:rgba(163,230,53,.55);
  box-shadow:0 22px 44px -22px rgba(163,230,53,.28);}
.ag-ficon{width:54px;height:54px;border-radius:16px;display:grid;place-items:center;font-size:1.65rem;
  background:rgba(163,230,53,.1);border:1px solid rgba(163,230,53,.3);margin-bottom:1rem;}
.ag-ftitle{font-size:1.15rem;font-weight:700;margin:0 0 .45rem;color:var(--text);}
.ag-fdesc{color:var(--muted);font-size:.92rem;line-height:1.65;margin:0 0 .9rem;}
.ag-tags{display:flex;flex-wrap:wrap;gap:.4rem;}
.ag-tag{font-size:.74rem;padding:.22rem .6rem;border-radius:999px;border:1px solid var(--border);
  color:var(--muted);background:rgba(255,255,255,.02);}
.ag-pillar,.ag-benefit{border:1px solid var(--border);border-radius:var(--radius);padding:1.3rem;
  background:var(--card);height:100%;transition:border-color .2s ease;}
.ag-pillar:hover,.ag-benefit:hover{border-color:rgba(163,230,53,.45);}
.ag-pillar h3,.ag-benefit h3{font-size:1rem;margin:0 0 .4rem;font-weight:700;}
.ag-pillar p,.ag-benefit p{color:var(--muted);font-size:.9rem;line-height:1.6;margin:0;}
.ag-step{display:flex;gap:1rem;align-items:flex-start;border:1px solid var(--border);border-radius:var(--radius);
  padding:1.3rem;background:linear-gradient(160deg,var(--card),var(--bg2));height:100%;}
.ag-step-num{flex:0 0 40px;height:40px;border-radius:12px;display:grid;place-items:center;font-weight:800;
  color:#06210f;background:linear-gradient(135deg,var(--lime),#84cc16);}
.ag-step h3{margin:0 0 .3rem;font-size:1rem;font-weight:700;}
.ag-step p{margin:0;color:var(--muted);font-size:.88rem;line-height:1.6;}

/* ---- page header ---- */
.ag-page-header{display:flex;align-items:center;gap:1rem;margin-bottom:1.4rem;animation:agUp .5s ease both;}
.ag-page-icon{width:58px;height:58px;border-radius:18px;display:grid;place-items:center;font-size:1.8rem;
  background:linear-gradient(135deg,rgba(22,163,74,.35),rgba(163,230,53,.15));border:1px solid rgba(163,230,53,.4);}
.ag-page-header h1{font-size:1.85rem;font-weight:800;margin:0;line-height:1.2;}
.ag-page-header p{margin:.25rem 0 0;color:var(--muted);font-size:.95rem;}

/* ---- keyed containers used as cards ---- */
div[class*="st-key-agcard"]{border:1px solid var(--border);border-radius:var(--radius);padding:1.2rem 1.3rem 1rem;
  background:linear-gradient(160deg,var(--card),var(--bg2));margin-bottom:1rem;box-shadow:var(--shadow);}
.ag-card-title{display:flex;align-items:center;gap:.55rem;font-weight:700;font-size:.98rem;margin:0 0 .6rem;color:var(--text);}
.ag-card-title:before{content:"";width:8px;height:8px;border-radius:50%;background:var(--lime);box-shadow:0 0 10px var(--lime);}

/* hero call-to-action (page link styled as primary button) */
div[class*="st-key-agcta"]{margin-top:1rem;}
div[class*="st-key-agcta"] [data-testid="stPageLink-NavLink"]{
  display:inline-flex;width:auto;padding:.75rem 1.4rem;border-radius:14px;
  background:linear-gradient(135deg,var(--green),#22c55e);border:none;
  box-shadow:0 12px 30px -12px rgba(34,197,94,.75);}
div[class*="st-key-agcta"] [data-testid="stPageLink-NavLink"] p{color:#fff !important;font-weight:700;}
div[class*="st-key-agcta"] [data-testid="stPageLink-NavLink"]:hover{filter:brightness(1.1);transform:translateY(-1px);}
/* feature-card page links */
.ag-fcard + div [data-testid="stPageLink-NavLink"],
div[data-testid="stElementContainer"]:has(.ag-fcard) + div [data-testid="stPageLink-NavLink"]{
  border:1px solid var(--border);margin-top:.6rem;background:var(--card);}
div[data-testid="stElementContainer"]:has(.ag-fcard) + div [data-testid="stPageLink-NavLink"]:hover{
  border-color:var(--lime);}

/* ---- results ---- */
.ag-result-hero{border-radius:22px;padding:1.8rem 1.6rem;border:1px solid rgba(163,230,53,.45);
  background:radial-gradient(420px 200px at 100% 0%,rgba(163,230,53,.18),transparent 70%),
   linear-gradient(150deg,#15332a,var(--bg2));box-shadow:0 0 0 1px rgba(163,230,53,.05),0 24px 50px -24px rgba(163,230,53,.35);
  animation:agPop .45s ease both;margin-bottom:1rem;}
.ag-kicker{font-size:.76rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:600;}
.ag-value{font-size:clamp(2.1rem,4.6vw,3.3rem);font-weight:800;line-height:1.1;margin:.35rem 0;color:var(--accent,var(--lime));
  text-shadow:0 0 28px rgba(163,230,53,.25);}
.ag-value small{font-size:.38em;font-weight:600;color:var(--muted);margin-inline-start:.4rem;text-shadow:none;}
.ag-sub{color:var(--muted);font-size:.93rem;line-height:1.6;}
.ag-tile{border:1px solid var(--border);border-radius:16px;padding:1rem 1.1rem;background:var(--card);margin-bottom:1rem;}
.ag-tile-label{font-size:.76rem;color:var(--muted);font-weight:600;letter-spacing:.04em;}
.ag-tile-value{font-size:1.5rem;font-weight:700;color:var(--text);margin-top:.2rem;}
.ag-tile-value small{font-size:.55em;color:var(--muted);font-weight:500;margin-inline-start:.3rem;}
.ag-callout{border-radius:14px;padding:.85rem 1rem;font-size:.88rem;line-height:1.65;margin:.2rem 0 1rem;
  border:1px solid var(--border);background:rgba(22,163,74,.08);color:var(--text);}
.ag-callout.warn{background:rgba(251,191,36,.08);border-color:rgba(251,191,36,.4);}
.ag-callout.error{background:rgba(239,68,68,.09);border-color:rgba(239,68,68,.45);}
.ag-empty{text-align:center;padding:3rem 1.4rem;border:1.5px dashed var(--border);border-radius:22px;color:var(--muted);
  background:rgba(13,31,24,.55);}
.ag-empty .ic{font-size:2.4rem;margin-bottom:.6rem;opacity:.9;}
.ag-empty h3{margin:0 0 .3rem;font-size:1.05rem;color:var(--text) !important;}
.ag-empty p{margin:0;font-size:.9rem;}
.ag-footer{margin-top:2.6rem;padding-top:1.1rem;border-top:1px solid var(--border);color:var(--muted);font-size:.8rem;line-height:1.6;}

/* ---- inputs ---- */
[data-testid="stWidgetLabel"] p,label[data-testid="stWidgetLabel"]{color:var(--muted) !important;font-size:.85rem !important;font-weight:500;}
[data-baseweb="input"],[data-baseweb="base-input"],[data-baseweb="select"] > div{
  background:var(--bg) !important;border-color:var(--border) !important;border-radius:12px !important;transition:border-color .15s ease, box-shadow .15s ease;}
[data-baseweb="input"]:focus-within,[data-baseweb="select"] > div:focus-within{
  border-color:var(--lime) !important;box-shadow:0 0 0 3px rgba(163,230,53,.15) !important;}
.stApp input,.stApp [data-baseweb="select"] *{color:var(--text) !important;}
[data-testid="stNumberInput"] button{background:var(--bg2) !important;border-color:var(--border) !important;color:var(--text) !important;}
[data-testid="stNumberInput"] button:hover{color:var(--lime) !important;}
input[type="number"]{direction:ltr;text-align:__NUMALIGN__;}
[data-baseweb="popover"] ul,[data-baseweb="popover"] [role="listbox"],[data-baseweb="menu"]{
  background:var(--card) !important;border:1px solid var(--border);border-radius:12px;}
[data-baseweb="popover"] li{color:var(--text) !important;} [data-baseweb="popover"] li:hover{background:rgba(163,230,53,.1) !important;}
[data-testid="stTooltipContent"],[data-baseweb="tooltip"] *{background:var(--card) !important;color:var(--text) !important;}

/* ---- buttons ---- */
.stButton > button{border-radius:12px !important;font-weight:600 !important;
  padding:.62rem 1.2rem !important;transition:all .18s ease !important;border:1px solid var(--border) !important;
  background:var(--card) !important;color:var(--text) !important;}
.stButton > button:hover{border-color:var(--lime) !important;color:var(--lime) !important;transform:translateY(-1px);}
.stButton > button[kind="primary"],[data-testid="stBaseButton-primary"]{
  background:linear-gradient(135deg,var(--green),#22c55e) !important;border-color:transparent !important;color:#fff !important;
  box-shadow:0 10px 26px -10px rgba(34,197,94,.7);}
.stButton > button[kind="primary"]:hover,[data-testid="stBaseButton-primary"]:hover{
  box-shadow:0 14px 32px -10px rgba(163,230,53,.55);color:#fff !important;filter:brightness(1.08);}
.stButton > button:active{transform:scale(.98);}
.stButton > button:focus-visible{outline:2px solid var(--lime) !important;outline-offset:2px;}

/* ---- expander / alerts / tables ---- */
[data-testid="stExpander"]{border:1px solid var(--border) !important;border-radius:14px !important;background:var(--card);}
[data-testid="stExpander"] summary p{color:var(--text) !important;font-weight:600;}
[data-testid="stAlert"]{border-radius:14px;border:1px solid var(--border);}
[data-testid="stDataFrame"],[data-testid="stTable"]{border:1px solid var(--border);border-radius:12px;overflow:hidden;}
.ag-table{width:100%;border-collapse:collapse;font-size:.88rem;}
.ag-table td{padding:.5rem .3rem;border-bottom:1px solid var(--border);}
.ag-table tr:last-child td{border-bottom:none;}
.ag-table td:first-child{color:var(--muted);}
.ag-table td:last-child{text-align:end;color:var(--text);font-weight:600;direction:ltr;}
.js-plotly-plot,.plotly{direction:ltr;}

/* ---- motion ---- */
@keyframes agUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes agPop{from{opacity:0;transform:scale(.97)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){*{animation:none !important;transition:none !important;}}

/* ---- responsive ---- */
@media (max-width:900px){
  .block-container,[data-testid="stMainBlockContainer"]{padding:1.2rem 1rem 3rem !important;}
  .ag-hero{padding:1.6rem 1.2rem;border-radius:20px;}
  .ag-fcard{min-height:0;}
  .ag-page-icon{width:48px;height:48px;font-size:1.5rem;}
  .ag-page-header h1{font-size:1.45rem;}
}
"""


def build_css(lang: str = "en") -> str:
    rtl = lang == "ar"
    tokens = {
        "__IMPORT__": _FONT_IMPORT,
        "__BG__": BG, "__BG2__": BG2, "__CARD__": CARD, "__GREEN__": GREEN, "__LIME__": LIME,
        "__TEXT__": TEXT, "__MUTED__": MUTED, "__BORDER__": BORDER,
        "__FONT__": FONT_AR if rtl else FONT_EN,
        "__DIR__": "rtl" if rtl else "ltr",
        "__NUMALIGN__": "right",
    }
    css = _CSS
    for key, value in tokens.items():
        css = css.replace(key, value)
    if rtl:
        css += "\n.stApp{text-align:right;}\n[data-testid=\"stPageLink-NavLink\"]:hover{--dx:-1;}\n"
    return f"<style>{css}</style>"


def plotly_layout(lang: str = "en", height: int = 320, title: str | None = None) -> dict:
    """Shared Plotly layout (transparent background, brand fonts and colors)."""
    font = FONT_AR if lang == "ar" else FONT_EN
    layout: dict = dict(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=font, color=TEXT, size=13),
        margin=dict(l=12, r=12, t=48 if title else 12, b=12),
        hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER, font=dict(family=font, color=TEXT)),
        showlegend=False,
    )
    if title:
        layout["title"] = dict(text=title, x=0.02, xanchor="left", font=dict(size=15, color=TEXT))
    return layout
