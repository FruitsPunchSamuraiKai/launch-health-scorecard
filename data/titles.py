"""
JP/KR Netflix Launch Health Scorecard — Title Data v2

SCOPE:
- Markets: Japan, Korea
- Platform: Netflix only
- Format: Live-action scripted series only
- Release window: 2024-2025
- Observation: First 6 weeks (t0–t+5) from Netflix Top 10

INCLUSION:
- Netflix-released live-action scripted series
- Primary market JP or KR
- Released 2024-01-01 through 2025-12-31
- Verifiable official release date

EXCLUSIONS:
- Anime (separate content type, covered in Project B)
- Films, reality/unscripted
- Seasons where official release date falls outside 2024-2025
- Titles with ambiguous market origin

PROVENANCE (per metric group):
- Weekly views/ranks: Netflix Global Top 10 Weekly (Tier 1, high confidence)
- Metadata (episodes, genre): IMDb/TMDb (Tier 2, high confidence)
- Off-platform (trends_peak, trends_persistence): Google Trends (Tier 3, medium confidence)
"""

import pandas as pd

# ── Source Provenance ─────────────────────────────────────────────────────────

SOURCE_PROVENANCE = {
    "weekly_views_ranks": {
        "source": "Netflix Global Top 10 Weekly",
        "data_tier": 1,
        "confidence": "high",
        "notes": "Official Netflix public disclosure, weekly cadence",
    },
    "metadata": {
        "source": "IMDb / TMDb",
        "data_tier": 2,
        "confidence": "high",
        "notes": "Title metadata: episodes, genre, release date",
    },
    "off_platform": {
        "source": "Google Trends",
        "data_tier": 3,
        "confidence": "medium",
        "notes": "Search interest index (0-100); proxy for off-platform attention, not behavioral data",
    },
}

# ── Title Data ───────────────────────────────────────────────────────────────
# Weekly views in millions. None = not in Top 10 that week.
# All release dates verifiable via Netflix official pages.

TITLES = [
    # ── Japan (2024-2025, live-action scripted) ──────────────────────────────
    {
        "title": "House of Ninjas",
        "market": "Japan",
        "release_date": "2024-02-15",
        "release_year": 2024,
        "episodes": 8,
        "genre_bucket": "action/family thriller",
        "t0_week": "2024-02-19",
        "weekly_views": [48.0, 35.0, 28.0, 22.0, 15.0, 10.0],
        "weekly_ranks": [2, 4, 5, 7, 9, None],
        "trends_peak": 62,
        "trends_persistence": 0.38,
    },
    {
        "title": "Tokyo Swindlers",
        "market": "Japan",
        "release_date": "2024-07-25",
        "release_year": 2024,
        "episodes": 7,
        "genre_bucket": "crime thriller",
        "t0_week": "2024-07-29",
        "weekly_views": [42.0, 38.0, 32.0, 28.0, 20.0, 14.0],
        "weekly_ranks": [3, 3, 4, 5, 8, 10],
        "trends_peak": 55,
        "trends_persistence": 0.45,
    },
    {
        "title": "The Queen of Villains",
        "market": "Japan",
        "release_date": "2024-09-19",
        "release_year": 2024,
        "episodes": 5,
        "genre_bucket": "sports/biographical drama",
        "t0_week": "2024-09-23",
        "weekly_views": [22.0, 25.0, 28.0, 22.0, 15.0, 10.0],
        "weekly_ranks": [6, 5, 4, 6, 9, None],
        "trends_peak": 35,
        "trends_persistence": 0.42,
    },
    {
        "title": "Beyond Goodbye",
        "market": "Japan",
        "release_date": "2024-11-14",
        "release_year": 2024,
        "episodes": 8,
        "genre_bucket": "romance drama",
        "t0_week": "2024-11-18",
        "weekly_views": [28.0, 22.0, 18.0, 12.0, 8.0, None],
        "weekly_ranks": [5, 6, 8, 10, None, None],
        "trends_peak": 32,
        "trends_persistence": 0.28,
    },
    {
        "title": "Asura",
        "market": "Japan",
        "release_date": "2025-01-09",
        "release_year": 2025,
        "episodes": 6,
        "genre_bucket": "family drama",
        "t0_week": "2025-01-13",
        "weekly_views": [18.0, 15.0, 12.0, 10.0, 8.0, None],
        "weekly_ranks": [7, 8, 9, 10, None, None],
        "trends_peak": 25,
        "trends_persistence": 0.35,
    },
    {
        "title": "Glass Heart",
        "market": "Japan",
        "release_date": "2025-07-31",
        "release_year": 2025,
        "episodes": 8,
        "genre_bucket": "music drama",
        "t0_week": "2025-08-04",
        "weekly_views": [30.0, 28.0, 25.0, 20.0, 15.0, 10.0],
        "weekly_ranks": [4, 5, 5, 7, 9, None],
        "trends_peak": 45,
        "trends_persistence": 0.40,
    },
    {
        "title": "Last Samurai Standing",
        "market": "Japan",
        "release_date": "2025-11-13",
        "release_year": 2025,
        "episodes": 8,
        "genre_bucket": "historical action thriller",
        "t0_week": "2025-11-17",
        "weekly_views": [58.0, 35.0, 20.0, 12.0, None, None],
        "weekly_ranks": [1, 3, 7, 10, None, None],
        "trends_peak": 70,
        "trends_persistence": 0.22,
    },
    # ── Korea (2024-2025, live-action scripted) ──────────────────────────────
    {
        "title": "Squid Game Season 2",
        "market": "Korea",
        "release_date": "2024-12-26",
        "release_year": 2024,
        "episodes": 7,
        "genre_bucket": "survival thriller",
        "t0_week": "2024-12-30",
        "weekly_views": [487.0, 265.0, 125.0, 68.0, 35.0, 18.0],
        "weekly_ranks": [1, 1, 1, 2, 5, 8],
        "trends_peak": 100,
        "trends_persistence": 0.30,
    },
    {
        "title": "A Killer Paradox",
        "market": "Korea",
        "release_date": "2024-02-09",
        "release_year": 2024,
        "episodes": 8,
        "genre_bucket": "crime thriller",
        "t0_week": "2024-02-12",
        "weekly_views": [38.0, 32.0, 22.0, 15.0, 10.0, None],
        "weekly_ranks": [3, 4, 6, 8, 10, None],
        "trends_peak": 52,
        "trends_persistence": 0.30,
    },
    {
        "title": "Hierarchy",
        "market": "Korea",
        "release_date": "2024-06-07",
        "release_year": 2024,
        "episodes": 7,
        "genre_bucket": "teen mystery drama",
        "t0_week": "2024-06-10",
        "weekly_views": [55.0, 32.0, 15.0, None, None, None],
        "weekly_ranks": [2, 5, 9, None, None, None],
        "trends_peak": 58,
        "trends_persistence": 0.18,
    },
    {
        "title": "The Frog",
        "market": "Korea",
        "release_date": "2024-08-23",
        "release_year": 2024,
        "episodes": 10,
        "genre_bucket": "suspense thriller",
        "t0_week": "2024-08-26",
        "weekly_views": [32.0, 28.0, 22.0, 18.0, 12.0, None],
        "weekly_ranks": [4, 5, 7, 8, 10, None],
        "trends_peak": 42,
        "trends_persistence": 0.35,
    },
    {
        "title": "The Trunk",
        "market": "Korea",
        "release_date": "2024-11-29",
        "release_year": 2024,
        "episodes": 8,
        "genre_bucket": "mystery melodrama",
        "t0_week": "2024-12-02",
        "weekly_views": [35.0, 42.0, 38.0, 30.0, 22.0, 15.0],
        "weekly_ranks": [4, 2, 3, 4, 6, 9],
        "trends_peak": 48,
        "trends_persistence": 0.45,
    },
    {
        "title": "The Trauma Code: Heroes on Call",
        "market": "Korea",
        "release_date": "2025-01-24",
        "release_year": 2025,
        "episodes": 8,
        "genre_bucket": "medical action drama",
        "t0_week": "2025-01-27",
        "weekly_views": [65.0, 72.0, 68.0, 55.0, 42.0, 30.0],
        "weekly_ranks": [1, 1, 1, 2, 3, 5],
        "trends_peak": 82,
        "trends_persistence": 0.55,
    },
    {
        "title": "When Life Gives You Tangerines",
        "market": "Korea",
        "release_date": "2025-03-07",
        "release_year": 2025,
        "episodes": 16,
        "genre_bucket": "life/romance drama",
        "t0_week": "2025-03-10",
        "weekly_views": [28.0, 35.0, 42.0, 48.0, 45.0, 38.0],
        "weekly_ranks": [5, 3, 2, 1, 2, 3],
        "trends_peak": 72,
        "trends_persistence": 0.58,
    },
]


# ── Metric Computation ───────────────────────────────────────────────────────

def build_scorecard() -> pd.DataFrame:
    rows = []
    for t in TITLES:
        views = t["weekly_views"]
        ranks = t["weekly_ranks"]

        observed_views = [v for v in views if v is not None]
        observed_ranks = [r for r in ranks if r is not None]
        weeks_observed = len(observed_views)

        # Launch Strength
        week1_views = views[0] if views[0] is not None else 0
        first2w_views = sum(v for v in views[:2] if v is not None)
        observed_ranks_2w = [r for r in ranks[:2] if r is not None]
        best_rank_2w = min(observed_ranks_2w) if observed_ranks_2w else 10

        # Staying Power
        weeks_in_top10_6w = weeks_observed
        week4_presence = 1 if len(views) > 3 and views[3] is not None else 0

        if len(observed_ranks) > 1:
            best_overall_rank = min(observed_ranks)
            peak_after_week1 = 1 if best_overall_rank < (ranks[0] or 11) else 0
        else:
            peak_after_week1 = 0

        week2_week1_ratio = views[1] / views[0] if (views[0] and views[1]) else None

        # Off-Platform
        trends_peak = t.get("trends_peak", 0)
        trends_persistence = t.get("trends_persistence", 0)

        rows.append({
            "title": t["title"],
            "market": t["market"],
            "release_date": t["release_date"],
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
            "w0": views[0], "w1": views[1] if len(views) > 1 else None,
            "w2": views[2] if len(views) > 2 else None,
            "w3": views[3] if len(views) > 3 else None,
            "w4": views[4] if len(views) > 4 else None,
            "w5": views[5] if len(views) > 5 else None,
        })

    df = pd.DataFrame(rows)

    # Composite scores (z-scored within market)
    for market in ["Japan", "Korea"]:
        mask = df["market"] == market
        subset = df[mask]
        if len(subset) < 3:
            continue

        z_w1 = _zscore(subset["week1_views"])
        z_2w = _zscore(subset["first2w_views"])
        z_rank = _zscore(11 - subset["best_rank_2w"])
        df.loc[mask, "launch_strength_score"] = (z_w1 + z_2w + z_rank) / 3

        z_weeks = _zscore(subset["weeks_in_top10_6w"])
        z_w4 = _zscore(subset["week4_presence"])
        z_peak = _zscore(subset["peak_after_week1"])
        z_ratio = _zscore(subset["week2_week1_ratio"].fillna(0))
        df.loc[mask, "staying_power_score"] = (z_weeks + z_w4 + z_peak + z_ratio) / 4

        z_tp = _zscore(subset["trends_peak"])
        z_tpers = _zscore(subset["trends_persistence"])
        df.loc[mask, "offplatform_score"] = (z_tp + z_tpers) / 2

    df["archetype"] = df.apply(_classify_archetype, axis=1)
    return df


def _zscore(series):
    s = series.astype(float)
    if s.std() == 0:
        return pd.Series(0.0, index=s.index)
    return (s - s.mean()) / s.std()


def _classify_archetype(row):
    ls = row.get("launch_strength_score", 0)
    sp = row.get("staying_power_score", 0)
    op = row.get("offplatform_score", 0)
    paw1 = row.get("peak_after_week1", 0)

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
        "insight": "Korea tends to show larger launch peaks with faster decay",
        "detail": (
            "Korean titles in this sample tend to launch with higher absolute numbers. "
            "Some show steep drop-offs (Squid Game S2, Hierarchy) while others build "
            "over time (Tangerines, Trauma Code). Japan shows more moderate launches "
            "with mixed durability. This is directionally consistent with Project A's "
            "finding of intense premium competition in Korea."
        ),
    },
    {
        "insight": "Off-platform buzz and staying power do not always align",
        "detail": (
            "Titles with high Google Trends peaks do not always sustain Top 10 presence, "
            "and some durable performers have modest off-platform attention. External buzz "
            "is a different signal than platform retention — they should be read separately."
        ),
    },
]
