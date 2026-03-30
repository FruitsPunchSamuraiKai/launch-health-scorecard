# Data Assumptions & Metric Definitions

## Sample Scope

- **Markets:** Japan and Korea
- **Platform:** Netflix only
- **Format:** Scripted series only
- **Timeframe:** 2024-2025 releases
- **Observation window:** First 6 weeks after Top 10 entry (t0–t+5)
- **Current sample:** 14 titles (7 Japan, 7 Korea)

### Inclusion criteria
All must be true:
- Primary market is Japan or Korea
- Scripted Netflix series
- Observable in Netflix weekly Top 10
- At least 2 weeks of post-launch observation

### Exclusions
Films, reality/unscripted, insufficient observation window, ambiguous origin.

## Observation Rules

- **t0** = first week title appears in Netflix Top 10
- **Missing weeks** = below reporting threshold, NOT zero demand
- Presence-based durability metrics preferred over zero-filled cumulative

## Metric Definitions

### Launch Strength
| Metric | Definition | Tier |
|---|---|---|
| week1_views | Views at t0 | 1 |
| first2w_views | views_t0 + views_t1 | 1 |
| best_rank_2w | Best rank in first 2 weeks | 1 |
| launch_strength_score | Composite: z(week1) + z(first2w) + z(11-rank), within market | Derived |

### Staying Power
| Metric | Definition | Tier |
|---|---|---|
| weeks_in_top10_6w | Count of observed Top 10 weeks in t0:t+5 | 1 |
| week4_presence | 1 if observed at t+3, else 0 | 1 |
| peak_after_week1 | 1 if best rank occurs after t0 | 1 |
| week2_week1_ratio | views_t1 / views_t0 | 1 |
| staying_power_score | Composite z-score within market | Derived |

### Off-Platform Attention
| Metric | Definition | Tier |
|---|---|---|
| trends_peak | Max Google Trends index, t-1 to t+3 | 3 |
| trends_persistence | Mean Trends t+1:t+4 / peak | 3 |
| offplatform_score | Composite z-score within market | Derived |

## Archetype Classification (Rule-Based)

| Archetype | Launch Strength | Staying Power | Other |
|---|---|---|---|
| Durable Hit | >= P66 | >= P66 | — |
| Front-Loaded Event | >= P66 | <= P33 | — |
| Slow Burner | <= P50 | >= P66 | or peak_after_week1=1 |
| Low-Buzz Niche | <= P50 | <= P50 | offplatform <= P33 |
| Balanced / Mixed | everything else | — | — |

## Key Caveats

- Weekly Top 10 data is thresholded; non-observed weeks are not zero
- Scores are relative within market, not absolute globally
- Off-platform attention is proxy-based
- This diagnoses launch shape, not marketing causality
