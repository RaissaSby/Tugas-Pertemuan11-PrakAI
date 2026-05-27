import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Palette",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0e0e0f;
}

/* Remove Streamlit default padding */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}

/* Remove top gap Streamlit adds */
[data-testid="stAppViewBlockContainer"] {
    padding: 0 !important;
}

div[data-testid="stVerticalBlock"] > div:first-child {
    padding-top: 0 !important;
}

/* ── Header ── */
.site-header {
    padding: 2rem 3rem 1.5rem;
    border-bottom: 1px solid #252528;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 2rem;
    margin-bottom: 0;
}
.site-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: #e8e4dc;
    letter-spacing: -0.02em;
    line-height: 1;
    margin: 0;
}
.site-title em {
    font-style: italic;
    color: #c8a97e;
}
.site-desc {
    font-size: 0.75rem;
    color: #888890;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding-bottom: 0.3rem;
}

/* ── Column panels ── */
.panel-wrap {
    padding: 1.75rem 2rem 2rem;
}
.panel-wrap-right {
    padding: 1.75rem 2rem 2rem;
    border-left: 1px solid #252528;
}
.panel-label {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #666670;
    margin-bottom: 1rem;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] section {
    border: 1px dashed #2e2e34 !important;
    border-radius: 12px !important;
    background: #0a0a0c !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"] section p,
[data-testid="stFileUploader"] section span {
    color: #666670 !important;
    font-size: 0.82rem !important;
}
[data-testid="stFileUploaderDropzoneInput"] + div button {
    border-radius: 99px !important;
    background: #1a1a1e !important;
    border: 1px solid #2e2e34 !important;
    color: #a0a09a !important;
}
[data-testid="stImage"] img {
    border-radius: 10px;
    border: 1px solid #252528;
}

/* ── Spinner ── */
.stSpinner p {
    color: #888890 !important;
    font-size: 0.8rem !important;
}

/* ── Color strip ── */
.strip-wrap {
    border-radius: 10px;
    overflow: hidden;
    height: 64px;
    display: flex;
    margin-bottom: 1.25rem;
    border: 1px solid #252528;
}
.strip-seg { height: 100%; }

/* ── Swatches ── */
.swatch-row {
    display: flex;
    gap: 6px;
    margin-bottom: 1.5rem;
}
.swatch {
    flex: 1;
    border-radius: 8px;
    aspect-ratio: 1;
    border: 1px solid rgba(255,255,255,0.07);
    position: relative;
}
.swatch-hex {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    text-align: center;
    padding: 4px 0 6px;
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 0.05em;
    background: rgba(0,0,0,0.32);
    color: rgba(255,255,255,0.9);
    border-radius: 0 0 7px 7px;
    text-transform: uppercase;
}

/* ── Section divider ── */
.sect-div {
    height: 1px;
    background: #252528;
    margin: 1.25rem 0;
}

/* ── Bar chart ── */
.bars {
    display: flex;
    flex-direction: column;
    gap: 7px;
    margin-bottom: 1.5rem;
}
.bar-row {
    display: flex;
    align-items: center;
    gap: 8px;
}
.bar-dot {
    width: 10px; height: 10px;
    border-radius: 3px;
    flex-shrink: 0;
}
.bar-hex-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 10.5px;
    color: #888890;
    width: 62px;
    flex-shrink: 0;
}
.bar-track {
    flex: 1;
    height: 4px;
    background: #1e1e22;
    border-radius: 99px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 99px;
}
.bar-pct {
    font-family: 'DM Mono', monospace;
    font-size: 10.5px;
    color: #666670;
    width: 36px;
    text-align: right;
    flex-shrink: 0;
}

/* ── Detail boxes ── */
.detail-box {
    background: #121214;
    border: 1px solid #252528;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.detail-swatch {
    width: 40px; height: 40px;
    border-radius: 8px;
    flex-shrink: 0;
    border: 1px solid rgba(255,255,255,0.07);
}
.detail-right { flex: 1; min-width: 0; }
.detail-hex {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #e8e4dc;
    letter-spacing: -0.01em;
    margin-bottom: 0.4rem;
}
.chips-row {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}
.chip {
    background: #0e0e0f;
    border: 1px solid #252528;
    border-radius: 6px;
    padding: 0.3rem 0.6rem;
    display: flex;
    flex-direction: column;
    gap: 1px;
}
.chip-label {
    font-size: 8.5px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #555560;
    line-height: 1;
}
.chip-val {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #b0b0aa;
    font-weight: 400;
}

/* ── Waiting state ── */
.waiting {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: #333338;
    font-size: 0.75rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

/* ── Export button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #2e2e34 !important;
    border-radius: 99px !important;
    color: #888890 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    border-color: #888890 !important;
    color: #c8c8c2 !important;
    background: #141416 !important;
}

/* ── Image meta ── */
.img-meta {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    font-size: 0.7rem;
    color: #666670;
    font-family: 'DM Mono', monospace;
}

/* ── Footer ── */
.site-footer {
    border-top: 1px solid #252528;
    padding: 1rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}
.footer-txt {
    font-size: 0.65rem;
    color: #444448;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    l = (mx+mn)/2
    if mx == mn:
        h = s = 0
    else:
        d = mx - mn
        s = d/(2-mx-mn) if l > 0.5 else d/(mx+mn)
        if mx == r:   h = (g-b)/d + (6 if g<b else 0)
        elif mx == g: h = (b-r)/d + 2
        else:         h = (r-g)/d + 4
        h /= 6
    return round(h*360), round(s*100), round(l*100)

def brightness(rgb):
    return (rgb[0]*0.299 + rgb[1]*0.587 + rgb[2]*0.114) / 255

def extract_colors(image_array, n=6):
    pixels = image_array.reshape(-1, 3).astype(float)
    if len(pixels) > 200_000:
        idx = np.random.choice(len(pixels), 200_000, replace=False)
        pixels = pixels[idx]
    km = KMeans(n_clusters=n, random_state=42, n_init=10)
    km.fit(pixels)
    centers = km.cluster_centers_.astype(int)
    counts = np.bincount(km.labels_)
    pcts = counts / counts.sum() * 100
    order = np.argsort(pcts)[::-1]
    return centers[order], pcts[order]

def make_strip(colors, pcts):
    segs = ""
    for c, p in zip(colors, pcts):
        hex_c = rgb_to_hex(c)
        segs += f'<div class="strip-seg" style="flex:{p:.2f}; background:{hex_c};"></div>'
    return f'<div class="strip-wrap">{segs}</div>'

def make_swatches(colors):
    html = '<div class="swatch-row">'
    for c in colors:
        hex_c = rgb_to_hex(c)
        html += f'<div class="swatch" style="background:{hex_c};"><div class="swatch-hex">{hex_c}</div></div>'
    html += '</div>'
    return html

def make_bars(colors, pcts):
    html = '<div class="bars">'
    for c, p in zip(colors, pcts):
        hex_c = rgb_to_hex(c)
        html += f'''<div class="bar-row">
  <div class="bar-dot" style="background:{hex_c};"></div>
  <span class="bar-hex-lbl">{hex_c.upper()}</span>
  <div class="bar-track"><div class="bar-fill" style="width:{p:.1f}%;background:{hex_c};"></div></div>
  <span class="bar-pct">{p:.1f}%</span>
</div>'''
    html += '</div>'
    return html

def make_detail(colors, pcts):
    html = ""
    for c, p in zip(colors, pcts):
        hex_c = rgb_to_hex(c).upper()
        h, s, l = rgb_to_hsl(*c)
        br = round(brightness(c)*100)
        swatch_hex = rgb_to_hex(c)
        html += f'''<div class="detail-box">
  <div class="detail-swatch" style="background:{swatch_hex};"></div>
  <div class="detail-right">
    <div class="detail-hex">{hex_c}</div>
    <div class="chips-row">
      <div class="chip"><div class="chip-label">RGB</div><div class="chip-val">{int(c[0])}, {int(c[1])}, {int(c[2])}</div></div>
      <div class="chip"><div class="chip-label">HSL</div><div class="chip-val">{h}° {s}% {l}%</div></div>
      <div class="chip"><div class="chip-label">Coverage</div><div class="chip-val">{p:.1f}%</div></div>
      <div class="chip"><div class="chip-label">Lum</div><div class="chip-val">{br}%</div></div>
    </div>
  </div>
</div>'''
    return html

def make_export(colors, pcts, fname):
    lines = ["PALETTE EXPORT", "─"*34, f"File: {fname}", ""]
    for c, p in zip(colors, pcts):
        hex_c = rgb_to_hex(c).upper()
        h, s, l = rgb_to_hsl(*c)
        lines.append(f"{hex_c}  |  RGB({int(c[0])}, {int(c[1])}, {int(c[2])})  |  HSL({h}°, {s}%, {l}%)  |  {p:.1f}%")
    return "\n".join(lines)


# ── Header ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="site-header">
  <h1 class="site-title"><em>Palette</em></h1>
  <p class="site-desc">Dominant color extractor · K-Means clustering</p>
</div>
""", unsafe_allow_html=True)


# ── Columns ───────────────────────────────────────────────────────────────────

col_l, col_r = st.columns(2, gap="small")

with col_l:
    st.markdown('<div class="panel-wrap">', unsafe_allow_html=True)
    st.markdown('<p class="panel-label">Input</p>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "", type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, use_container_width=True)
        st.markdown(
            f'<div class="img-meta"><span>{uploaded.name}</span>'
            f'<span>{image.width} × {image.height}</span></div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="panel-wrap-right">', unsafe_allow_html=True)
    st.markdown('<p class="panel-label">Output</p>', unsafe_allow_html=True)

    if uploaded:
        img_arr = np.array(image)
        with st.spinner("extracting…"):
            colors, pcts = extract_colors(img_arr, n=6)

        st.markdown(make_strip(colors, pcts), unsafe_allow_html=True)
        st.markdown(make_swatches(colors), unsafe_allow_html=True)

        st.markdown('<div class="sect-div"></div>', unsafe_allow_html=True)
        st.markdown('<p class="panel-label">Proportion</p>', unsafe_allow_html=True)
        st.markdown(make_bars(colors, pcts), unsafe_allow_html=True)

        st.markdown('<div class="sect-div"></div>', unsafe_allow_html=True)
        st.markdown('<p class="panel-label">Color values</p>', unsafe_allow_html=True)
        st.markdown(make_detail(colors, pcts), unsafe_allow_html=True)

        st.markdown('<div class="sect-div"></div>', unsafe_allow_html=True)
        export_txt = make_export(colors, pcts, uploaded.name)
        st.download_button(
            label="↓  export palette",
            data=export_txt,
            file_name="palette.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.markdown('<div class="waiting">— upload an image to begin —</div>',
                    unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="site-footer">
  <span class="footer-txt">Palette · Color Extractor</span>
  <span class="footer-txt" style="font-family:'DM Mono',monospace;">sklearn · KMeans · k=6</span>
</div>
""", unsafe_allow_html=True)