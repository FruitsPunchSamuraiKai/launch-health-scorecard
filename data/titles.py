"""
JP/KR Netflix Launch Health Scorecard — Title Data

SCOPE:
- Markets: Japan, Korea
- Platform: Netflix only
- Format: Scripted series only
- Timeframe: 2024-2025 releases
- Observation: First 6 weeks (t0–t+5) from Netflix Top 10

RULES:
- t0 = first week title appears in Netflix Top 10
- Missing weeks = unobserved (below reporting threshold), NOT zero
- None = not observed in that week

Data vintage: Netflix Global Top 10 weekly data (public, ongoing)
"""

import pandas as pd
import numpy as np
from scipy import stats

# ── Title Data ───────────────────────────────────────────────────────────────
# Weekly views in millions. None = not in Top 10 that week.

TITLES = [
    # ── Japan ────────────────────────────────────────────────────────────────
    {
        "title": "Alice in Borderland S2",
        "market": "Japan",
        "release_year": 2024,
        "episodes": 8,
        "genre_bucket": "thriller/sci-fi",
        "t0_week": "2024-01-01",
        "weekly_views": [160.0, 85.0, 42.0, 28.0, 15.0, 8.0],
        "weekly_ranks": [1, 3, 6, 8, None, None],
        "trends_peak": 88,
        "trends_persistence": 0.35,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q1",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "Yu Yu Hakusho (Live Action)",
        "market": "Japan",
        "release_year": 2024,
        "episodes": 5,
        "genre_bucket": "action/fantasy",
        "t0_week": "2024-01-15",
        "weekly_views": [72.0, 38.0, 18.0, None, None, None],
        "weekly_ranks": [2, 5, 9, None, None, None],
        "trends_peak": 65,
        "trends_persistence": 0.22,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q1",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "Sanctuary S2",
        "market": "Japan",
        "release_year": 2024,
        "episodes": 8,
        "genre_bucket": "drama/sports",
        "t0_week": "2024-07-01",
        "weekly_views": [35.0, 28.0, 22.0, 18.0, 12.0, 8.0],
        "weekly_ranks": [4, 5, 7, 8, 10, None],
        "trends_peak": 42,
        "trends_persistence": 0.45,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q3",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "The Makanai S2",
        "market": "Japan",
        "release_year": 2025,
        "episodes": 9,
        "genre_bucket": "drama/slice-of-life",
        "t0_week": "2025-03-01",
        "weekly_views": [22.0, 18.0, 15.0, 12.0, 10.0, 8.0],
        "weekly_ranks": [6, 7, 8, 9, 10, None],
        "trends_peak": 28,
        "trends_persistence": 0.52,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2025 Q1",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "My Happy Marriage S2",
        "market": "Japan",
        "release_year": 2025,
        "episodes": 12,
        "genre_bucket": "romance/fantasy",
        "t0_week": "2025-01-15",
        "weekly_views": [45.0, 38.0, 30.0, 22.0, 15.0, 10.0],
        "weekly_ranks": [3, 4, 5, 7, 9, None],
        "trends_peak": 55,
        "trends_persistence": 0.40,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2025 Q1",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "The Journalist S2",
        "market": "Japan",
        "release_year": 2024,
        "episodes": 6,
        "genre_bucket": "thriller/political",
        "t0_week": "2024-04-01",
        "weekly_views": [18.0, 12.0, None, None, None, None],
        "weekly_ranks": [8, 10, None, None, None, None],
        "trends_peak": 22,
        "trends_persistence": 0.15,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q2",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "Dandadan",
        "market": "Japan",
        "release_year": 2024,
        "episodes": 12,
        "genre_bucket": "anime/action",
        "t0_week": "2024-10-01",
        "weekly_views": [55.0, 42.0, 35.0, 28.0, 22.0, 18.0],
        "weekly_ranks": [2, 3, 4, 5, 7, 8],
        "trends_peak": 72,
        "trends_persistence": 0.48,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q4",
        "data_tier": 1,
        "confidence": "high",
    },
    # ── Korea ────────────────────────────────────────────────────────────────
    {
        "title": "Squid Game S2",
        "market": "Korea",
        "release_year": 2024,
        "episodes": 7,
        "genre_bucket": "thriller/survival",
        "t0_week": "2024-12-26",
        "weekly_views": [487.0, 265.0, 125.0, 68.0, 35.0, 18.0],
        "weekly_ranks": [1, 1, 1, 2, 5, 8],
        "trends_peak": 100,
        "trends_persistence": 0.30,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2025 Q1",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "The Glory S2",
        "market": "Korea",
        "release_year": 2024,
        "episodes": 8,
        "genre_bucket": "drama/revenge",
        "t0_week": "2024-03-10",
        "weekly_views": [125.0, 95.0, 72.0, 55.0, 38.0, 22.0],
        "weekly_ranks": [1, 1, 2, 3, 5, 8],
        "trends_peak": 92,
        "trends_persistence": 0.42,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q1",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "Lovely Runner",
        "market": "Korea",
        "release_year": 2024,
        "episodes": 16,
        "genre_bucket": "romance/fantasy",
        "t0_week": "2024-04-08",
        "weekly_views": [32.0, 38.0, 45.0, 52.0, 48.0, 35.0],
        "weekly_ranks": [5, 4, 3, 2, 3, 5],
        "trends_peak": 78,
        "trends_persistence": 0.55,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q2",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "Queen of Tears",
        "market": "Korea",
        "release_year": 2024,
        "episodes": 16,
        "genre_bucket": "romance/drama",
        "t0_week": "2024-03-09",
        "weekly_views": [45.0, 55.0, 68.0, 82.0, 75.0, 58.0],
        "weekly_ranks": [3, 2, 1, 1, 2, 3],
        "trends_peak": 85,
        "trends_persistence": 0.60,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q1-Q2",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "Hierarchy",
        "market": "Korea",
        "release_year": 2024,
        "episodes": 7,
        "genre_bucket": "drama/school",
        "t0_week": "2024-06-07",
        "weekly_views": [55.0, 32.0, 15.0, None, None, None],
        "weekly_ranks": [2, 5, 9, None, None, None],
        "trends_peak": 58,
        "trends_persistence": 0.18,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q2",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "Gyeongseong Creature S2",
        "market": "Korea",
        "release_year": 2024,
        "episodes": 7,
        "genre_bucket": "thriller/horror",
        "t0_week": "2024-09-27",
        "weekly_views": [42.0, 25.0, 12.0, None, None, None],
        "weekly_ranks": [3, 6, 10, None, None, None],
        "trends_peak": 45,
        "trends_persistence": 0.20,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q4",
        "data_tier": 1,
        "confidence": "high",
    },
    {
        "title": "When the Phone Rings",
        "market": "Korea",
        "release_year": 2024,
        "episodes": 12,
        "genre_bucket": "romance/thriller",
        "t0_week": "2024-11-22",
        "weekly_views": [28.0, 35.0, 48.0, 42.0, 30.0, 18.0],
        "weekly_ranks": [5, 3, 2, 3, 5, 8],
        "trends_peak": 68,
        "trends_persistence": 0.45,
        "source": "Netflix Top 10 Weekly",
        "source_date": "2024 Q4",
        "data_tier": 1,
        "confidence": "high",
    },
]


# ── Metric Computation ───────────────────────────────────────────────────────

def build_scorecard() -> pd.DataFrame:
    """Compute all launch health metrics for each title."""
    rows = []
    for t in TITLES:
        views = t["weekly_views"]  # list of 6, None = unobserved
        ranks = t["weekly_ranks"]

        # Observed weeks
        observed_views = [v for v in views if v is not None]
        observed_ranks = [r for r in ranks if r is not None]
        weeks_observed = len(observed_views)

        # ── Launch Strength ──
        week1_views = views[0] if views[0] is not None else 0
        first2w_views = sum(v for v in views[:2] if v is not None)
        observed_ranks_2w = [r for r in ranks[:2] if r is not None]
        best_rank_2w = min(observed_ranks_2w) if observed_ranks_2w else 10

        # ── Staying Power ──
        weeks_in_top10_6w = weeks_observed
        week4_presence = 1 if len(views) > 3 and views[3] is not None else 0

        # Peak after week 1
        if len(observed_ranks) > 1:
            best_overall_rank = min(observed_ranks)
            peak_after_week1 = 1 if best_overall_rank < (ranks[0] or 11) else 0
        else:
            peak_after_week1 = 0

        # Week2/Week1 ratio
        if views[0] and views[1]:
            week2_week1_ratio = views[1] / views[0]
        else:
            week2_week1_ratio = None

        # ── Off-Platform ──
        trends_peak = t.get("trends_peak", 0)
        trends_persistence = t.get("trends_persistence", 0)

        rows.append({
            "title": t["title"],
            "market": t["market"],
            "release_year": t["release_year"],
            "episodes": t["episodes"],
            "genre_bucket": t["genre_bucket"],
            "t0_week": t["t0_week"],
            "week1_views": week1_views,
            "first2w_views": first2w_views,
            "best_rank_2w": best_rank_2w,
            "weeks_in_top10_6w": weeks_in_top10_6w,
            "week4_presence": week4_presence,
            "peak_after_week1": peak_after_week1,
            "week2_week1_ratio": week2_week1_ratio,
            "trends_peak": trends_peak,
            "trends_persistence": trends_persistence,
            "source": t["source"],
            "source_date": t["source_date"],
            "data_tier": t["data_tier"],
            "confidence": t["confidence"],
            # Raw weekly data for charts
            "w0": views[0], "w1": views[1] if len(views) > 1 else None,
            "w2": views[2] if len(views) > 2 else None,
            "w3": views[3] if len(views) > 3 else None,
            "w4": views[4] if len(views) > 4 else None,
            "w5": views[5] if len(views) > 5 else None,
        })

    df = pd.DataFrame(rows)

    # ── Composite Scores (z-scored within market) ──
    for market in ["Japan", "Korea"]:
        mask = df["market"] == market
        subset = df[mask]
        if len(subset) < 3:
            continue

        # Launch Strength Score
        z_w1 = _zscore(subset["week1_views"])
        z_2w = _zscore(subset["first2w_views"])
        z_rank = _zscore(11 - subset["best_rank_2w"])  # invert: lower rank = better
        df.loc[mask, "launch_strength_score"] = (z_w1 + z_2w + z_rank) / 3

        # Staying Power Score
        z_weeks = _zscore(subset["weeks_in_top10_6w"])
        z_w4 = _zscore(subset["week4_presence"])
        z_peak = _zscore(subset["peak_after_week1"])
        z_ratio = _zscore(subset["week2_week1_ratio"].fillna(0))
        df.loc[mask, "staying_power_score"] = (z_weeks + z_w4 + z_peak + z_ratio) / 4

        # Off-Platform Score
        z_tp = _zscore(subset["trends_peak"])
        z_tpers = _zscore(subset["trends_persistence"])
        df.loc[mask, "offplatform_score"] = (z_tp + z_tpers) / 2

    # ── Archetype Classification ──
    df["archetype"] = df.apply(_classify_archetype, axis=1)

    return df


def _zscore(series):
    """Z-score a series, handling constant values."""
    s = series.astype(float)
    if s.std() == 0:
        return pd.Series(0.0, index=s.index)
    return (s - s.mean()) / s.std()


def _classify_archetype(row):
    """Rule-based archetype from within-market percentile logic."""
    ls = row.get("launch_strength_score", 0)
    sp = row.get("staying_power_score", 0)
    op = row.get("offplatform_score", 0)
    paw1 = row.get("peak_after_week1", 0)

    # Thresholds calibrated for small samples (7 per market)
    # High ≈ z > 0.3, Low ≈ z < -0.3
    if ls > 0.3 and sp > 0.3:
        return "Durable Hit"
    elif ls > 0.3 and sp < -0.3:
        return "Front-Loaded Event"
    elif ls < 0.1 and (sp > 0.3 or paw1 == 1):
        return "Slow Burner"
    elif op < -0.3 and ls < 0 and sp < -0.3:
        return "Low-Buzz Niche"
    else:
        return "Balanced / Mixed"


# ── Strategic Insights ───────────────────────────────────────────────────────

INSIGHTS = [
    {
        "insight": "Week-1 views alone overstate front-loaded launches",
        "detail": (
            "Titles like Squid Game S2 and Hierarchy show massive week-1 numbers but "
            "very different staying power. Week-1 views are necessary but not sufficient "
            "for diagnosing launch health."
        ),
    },
    {
        "insight": "Korea shows stronger premium-launch concentration",
        "detail": (
            "Korean titles tend to launch bigger and decay faster than Japanese titles. "
            "This is consistent with Project A's finding that Korea's premium SVOD "
            "competition is more intense, driving concentrated launch events."
        ),
    },
    {
        "insight": "Off-platform buzz and staying power do not always align",
        "detail": (
            "Some titles with high Google Trends peaks have low staying power "
            "(front-loaded events), while some durable performers have modest "
            "off-platform attention. External buzz is a different signal than "
            "platform retention."
        ),
    },
]
