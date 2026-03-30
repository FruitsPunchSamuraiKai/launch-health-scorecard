"""
JP/KR Netflix Launch Health Scorecard
Public-data diagnostics for early signal vs. staying power
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from data.titles import build_scorecard, INSIGHTS

st.set_page_config(page_title="JP/KR Launch Health Scorecard", page_icon="🚀", layout="wide")

st.title("JP/KR Netflix Launch Health Scorecard")
st.caption("Public-data diagnostics for early signal vs. staying power in Japan and Korea")

@st.cache_data
def get_data():
    return build_scorecard()

df = get_data()
df_jp = df[df["market"] == "Japan"]
df_kr = df[df["market"] == "Korea"]

tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Summary", "Title Scorecard", "JP vs KR Comparison", "Methodology & Limitations"
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: EXECUTIVE SUMMARY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.header("Executive Summary")
    st.markdown("*Which public early signals distinguish front-loaded launches from durable performers?*")

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Titles Analyzed", len(df), f"JP {len(df_jp)} / KR {len(df_kr)}")
    with c2:
        durable = len(df[df["archetype"] == "Durable Hit"])
        st.metric("Durable Hits", durable, f"of {len(df)}")
    with c3:
        front = len(df[df["archetype"] == "Front-Loaded Event"])
        st.metric("Front-Loaded", front, f"of {len(df)}")
    with c4:
        slow = len(df[df["archetype"] == "Slow Burner"])
        st.metric("Slow Burners", slow, f"of {len(df)}")

    st.divider()

    # Archetype distribution
    st.subheader("Archetype Distribution")
    arch_data = df.groupby(["market", "archetype"]).size().reset_index(name="count")

    fig_arch = go.Figure()
    colors = {"Durable Hit": "#2ca02c", "Front-Loaded Event": "#d62728",
              "Slow Burner": "#ff7f0e", "Low-Buzz Niche": "#7f7f7f", "Balanced / Mixed": "#1f77b4"}
    for arch in colors:
        subset = arch_data[arch_data["archetype"] == arch]
        fig_arch.add_trace(go.Bar(
            x=subset["market"], y=subset["count"],
            name=arch, marker_color=colors[arch],
        ))
    fig_arch.update_layout(barmode="group", height=350, legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig_arch, use_container_width=True)

    st.divider()

    # Key insights
    st.subheader("Key Insights")
    for i, ins in enumerate(INSIGHTS, 1):
        st.markdown(f"**{i}. {ins['insight']}**")
        st.caption(ins["detail"])

    st.divider()
    st.caption(
        "Weekly Top 10 data is thresholded; non-observed weeks are not zero. "
        "Scores are relative within market. Off-platform attention is proxy-based. "
        "This is a diagnostics framework, not causal attribution."
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: TITLE SCORECARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.header("Title Scorecard")

    market_filter = st.selectbox("Market", ["All", "Japan", "Korea"], key="sc_market")
    if market_filter != "All":
        df_display = df[df["market"] == market_filter]
    else:
        df_display = df

    # Scorecard table
    score_cols = ["title", "market", "archetype", "week1_views", "first2w_views",
                  "best_rank_2w", "weeks_in_top10_6w", "week4_presence",
                  "week2_week1_ratio", "trends_peak", "trends_persistence",
                  "launch_strength_score", "staying_power_score", "offplatform_score"]

    display_df = df_display[score_cols].copy()
    for col in ["launch_strength_score", "staying_power_score", "offplatform_score"]:
        display_df[col] = display_df[col].round(2)
    if "week2_week1_ratio" in display_df.columns:
        display_df["week2_week1_ratio"] = display_df["week2_week1_ratio"].round(2)

    st.dataframe(display_df.rename(columns={
        "title": "Title", "market": "Market", "archetype": "Archetype",
        "week1_views": "Wk1 Views (M)", "first2w_views": "2Wk Views (M)",
        "best_rank_2w": "Best Rank (2w)", "weeks_in_top10_6w": "Wks in Top10",
        "week4_presence": "Wk4 Present", "week2_week1_ratio": "W2/W1 Ratio",
        "trends_peak": "Trends Peak", "trends_persistence": "Trends Persist",
        "launch_strength_score": "Launch Score", "staying_power_score": "Staying Score",
        "offplatform_score": "Offplatform Score",
    }), use_container_width=True, hide_index=True)

    # Launch vs Staying scatter
    st.subheader("Launch Strength vs Staying Power")

    fig_ls = go.Figure()
    arch_colors = {"Durable Hit": "#2ca02c", "Front-Loaded Event": "#d62728",
                   "Slow Burner": "#ff7f0e", "Low-Buzz Niche": "#7f7f7f", "Balanced / Mixed": "#1f77b4"}
    for arch, color in arch_colors.items():
        subset = df_display[df_display["archetype"] == arch]
        if len(subset) == 0:
            continue
        fig_ls.add_trace(go.Scatter(
            x=subset["launch_strength_score"], y=subset["staying_power_score"],
            mode="markers+text", name=arch,
            marker=dict(color=color, size=14, line=dict(width=1, color="white")),
            text=subset["title"], textposition="top right", textfont=dict(size=9),
        ))
    fig_ls.add_hline(y=0, line_dash="dash", line_color="#ddd")
    fig_ls.add_vline(x=0, line_dash="dash", line_color="#ddd")
    fig_ls.update_layout(
        xaxis_title="Launch Strength Score (z-scored within market)",
        yaxis_title="Staying Power Score (z-scored within market)",
        height=500, legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig_ls, use_container_width=True)

    # Weekly trajectory chart
    st.subheader("Weekly View Trajectories")
    selected_titles = st.multiselect("Select titles to compare",
        df_display["title"].tolist(), default=df_display["title"].tolist()[:4])

    if selected_titles:
        fig_traj = go.Figure()
        for title in selected_titles:
            row = df_display[df_display["title"] == title].iloc[0]
            weeks = []
            views = []
            for w in range(6):
                v = row.get(f"w{w}")
                if v is not None:
                    weeks.append(f"W{w}")
                    views.append(v)
            fig_traj.add_trace(go.Scatter(
                x=weeks, y=views, mode="lines+markers", name=title,
            ))
        fig_traj.update_layout(
            xaxis_title="Week", yaxis_title="Views (M)",
            height=400, legend=dict(orientation="h", y=1.12),
        )
        st.plotly_chart(fig_traj, use_container_width=True)

    # Source provenance (per metric group)
    st.subheader("Data Provenance")
    from data.titles import SOURCE_PROVENANCE
    prov_rows = []
    for group, info in SOURCE_PROVENANCE.items():
        prov_rows.append({
            "Metric Group": group.replace("_", " ").title(),
            "Source": info["source"],
            "Tier": info["data_tier"],
            "Confidence": info["confidence"],
            "Notes": info["notes"],
        })
    st.dataframe(pd.DataFrame(prov_rows), use_container_width=True, hide_index=True)

    st.caption(
        "Source provenance is assigned per metric group, not per title. "
        "Weekly views/ranks are Tier 1 (official Netflix). Off-platform metrics are Tier 3 (proxy)."
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: JP vs KR COMPARISON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.header("JP vs KR Launch Pattern Comparison")

    # Market-level averages
    st.subheader("Market Averages")
    market_avg = df.groupby("market").agg(
        avg_week1=("week1_views", "mean"),
        avg_2w=("first2w_views", "mean"),
        avg_weeks_top10=("weeks_in_top10_6w", "mean"),
        avg_w2w1_ratio=("week2_week1_ratio", "mean"),
        avg_trends_peak=("trends_peak", "mean"),
        avg_trends_persist=("trends_persistence", "mean"),
        n_titles=("title", "count"),
    ).round(2).reset_index()

    st.dataframe(market_avg.rename(columns={
        "market": "Market", "avg_week1": "Avg Wk1 (M)", "avg_2w": "Avg 2Wk (M)",
        "avg_weeks_top10": "Avg Wks Top10", "avg_w2w1_ratio": "Avg W2/W1",
        "avg_trends_peak": "Avg Trends Peak", "avg_trends_persist": "Avg Trends Persist",
        "n_titles": "N",
    }), use_container_width=True, hide_index=True)

    # Radar comparison
    st.subheader("Launch Profile Comparison")

    metrics = ["avg_week1", "avg_weeks_top10", "avg_w2w1_ratio", "avg_trends_peak", "avg_trends_persist"]
    labels = ["Wk1 Scale", "Durability", "W2/W1 Retention", "Buzz Peak", "Buzz Persistence"]

    # Normalize to 0-1 for radar
    jp_vals = market_avg[market_avg["market"] == "Japan"][metrics].values.flatten()
    kr_vals = market_avg[market_avg["market"] == "Korea"][metrics].values.flatten()
    max_vals = [max(jp_vals[i], kr_vals[i]) for i in range(len(metrics))]
    jp_norm = [jp_vals[i] / max_vals[i] if max_vals[i] > 0 else 0 for i in range(len(metrics))]
    kr_norm = [kr_vals[i] / max_vals[i] if max_vals[i] > 0 else 0 for i in range(len(metrics))]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=jp_norm + [jp_norm[0]], theta=labels + [labels[0]],
        fill="toself", name="Japan",
        fillcolor="rgba(31,119,180,0.2)", line=dict(color="#1f77b4", width=2),
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=kr_norm + [kr_norm[0]], theta=labels + [labels[0]],
        fill="toself", name="Korea",
        fillcolor="rgba(255,127,14,0.2)", line=dict(color="#ff7f0e", width=2),
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=400, legend=dict(orientation="h", y=-0.1),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Market interpretation
    st.subheader("Market-Specific Observations")

    col_jp, col_kr = st.columns(2)
    with col_jp:
        st.markdown("**Japan**")
        st.markdown("""
- Launch peaks tend to be smaller than Korea
- Staying power appears more evenly distributed
- Several titles show slow-burn or steady patterns
- Consistent with Project A's finding: Japan's competitive pressure
  is more about attention fragmentation than launch-weekend events
""")
    with col_kr:
        st.markdown("**Korea**")
        st.markdown("""
- Launches tend to be larger in absolute scale
- Faster decay from peak appears more common
- Several titles show steep front-loading patterns
- Some titles (Queen of Tears, Lovely Runner) build over time — slow-burn is not absent
- Directionally consistent with Project A: intense premium competition
  may drive bigger launch events but also faster attention turnover
""")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4: METHODOLOGY & LIMITATIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.header("Methodology & Limitations")

    st.subheader("Business Question")
    st.info(
        "Which public early signals distinguish front-loaded launches from durable "
        "performers in Japan and Korea, and how should launch health be interpreted "
        "differently by market?"
    )

    st.subheader("Metric Framework")
    st.markdown("""
| Dimension | Metrics | Purpose |
|---|---|---|
| **Launch Strength** | Week-1 views, first 2 weeks, best rank | How strong was the initial signal? |
| **Staying Power** | Weeks in Top 10, week-4 presence, W2/W1 ratio, peak timing | Did it sustain visibility? |
| **Off-Platform** | Google Trends peak, persistence | Did it generate external attention? |
""")

    st.subheader("Archetype Classification")
    st.markdown("""
Rule-based, using within-market z-score percentiles:

| Archetype | Launch | Staying | Other |
|---|---|---|---|
| Durable Hit | High | High | — |
| Front-Loaded Event | High | Low | — |
| Slow Burner | Low-Mid | High | or peak improved after W1 |
| Low-Buzz Niche | Low | Low | + low off-platform |
| Balanced / Mixed | — | — | everything else |
""")

    st.subheader("Key Design Choices")
    st.markdown("""
- **Missing weeks ≠ zero.** If a title drops out of Top 10, it means "below threshold," not "zero demand"
- **Within-market scoring.** Composite scores are z-scored per market because JP and KR operate at different absolute scales
- **No cost or export metrics.** Those are covered in Project B. This project focuses on launch trajectory only
""")

    st.subheader("Limitations")
    st.markdown("""
- **External data only** — no internal marketing spend, retention, or completion data
- **Top 10 is thresholded** — titles below the reporting cutoff are invisible
- **Off-platform attention is proxy-based** — Google Trends ≠ actual viewership intent
- **Small sample** — 14 titles; patterns are directional, not statistically definitive
- **This is diagnostics, not causal attribution** — it describes launch shape, not why
""")

    st.subheader("Connection to Portfolio")
    st.markdown("""
- **Project A** (APAC Streaming CI) → explains the competitive environment
- **Project B** (Content Investment Efficiency) → explains content type economics
- **Project C** (this project) → explains title-level launch trajectory

Together: **market context → investment framework → launch health diagnostics**
""")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### About")
    st.markdown(
        "**JP/KR Launch Health Scorecard**\n\n"
        "Public-data diagnostics for early signal vs. staying power.\n\n"
        "14 Netflix live-action scripted series across Japan and Korea, 2024-2025.\n\n"
        "Anime excluded (covered in Project B)."
    )
    st.markdown("---")
    st.markdown("### Data")
    st.markdown(
        "- Netflix Top 10 Weekly (Tier 1)\n"
        "- Google Trends (Tier 3)\n"
        "- Within-market z-scoring\n"
        "- Rule-based archetypes"
    )
    st.markdown("---")
    st.markdown("### Caveats")
    st.markdown(
        "- External data only\n"
        "- Top 10 is thresholded\n"
        "- 14 title sample\n"
        "- Diagnostics, not attribution"
    )
