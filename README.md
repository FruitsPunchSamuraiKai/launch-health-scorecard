# JP/KR Netflix Launch Health Scorecard

Public-data diagnostics for early signal vs. staying power in Japan and Korea.

*Part of a three-project portfolio:*
- *Project A: [APAC Streaming Competitive Intelligence](https://github.com/FruitsPunchSamuraiKai/apac-streaming-ci)*
- *Project B: [Japan Content Investment Efficiency](https://github.com/FruitsPunchSamuraiKai/japan-content-efficiency)*
- *Project C: This project — title-level launch health and trajectory*

## 1. Problem

Weekly launch performance is often summarized with a single number — week-1
views or peak rank. That can be misleading. A title with massive week-1 numbers
may decay rapidly, while a modest launch may build over time.

This project asks:
- Which public early signals distinguish front-loaded launches from durable performers?
- How should launch health be interpreted differently in Japan vs. Korea?
- Where does off-platform attention align with launch strength, and where does it not?

## 2. Scope

- **Markets:** Japan and Korea
- **Platform:** Netflix only
- **Format:** Live-action scripted series only
- **Timeframe:** 2024–2025 releases (verified official Netflix release dates)
- **Observation:** First 6 weeks after Top 10 entry (t0–t+5)
- **Sample:** 14 titles (7 Japan, 7 Korea)

### Inclusion criteria
- Netflix-released live-action scripted series
- Primary market is Japan or Korea
- Released 2024-01-01 through 2025-12-31
- Verifiable official release date
- Observable in Netflix weekly Top 10

### Exclusions
Anime (covered in Project B), films, reality/unscripted, seasons with
official release dates outside 2024-2025, ambiguous market origin.

## 3. Data Sources

| Source | What It Provides | Tier |
|---|---|---|
| Netflix Top 10 Weekly | Weekly views, ranks, weeks observed | 1 (Reported) |
| Netflix Engagement Report | Longer-window cross-check | 1 (Reported) |
| Google Trends | Off-platform search attention | 3 (Proxy) |
| IMDb / TMDb | Metadata: format, episodes, genre | 2 (Estimate) |

Every field tagged with source, source_date, data_tier, confidence.

## 4. Approach

Three diagnostic dimensions:

1. **Launch Strength** — week-1 views, first 2 weeks, best rank
2. **Staying Power** — weeks in Top 10, week-4 presence, W2/W1 ratio, peak timing
3. **Off-Platform Attention** — Google Trends peak and persistence

Composite scores z-scored **within market** (JP and KR operate at different absolute scales).

Rule-based archetype classification: Durable Hit, Front-Loaded Event, Slow Burner, Low-Buzz Niche, Balanced/Mixed.

## 5. Key Findings

- Week-1 views alone overstate some front-loaded launches
- Korea shows stronger premium-launch concentration and faster decay
- Japan shows more mixed durability patterns, consistent with attention fragmentation
- Off-platform buzz and staying power do not always move together

## 6. Limitations

- External data only — no internal marketing/retention/completion data
- Top 10 data is thresholded (below cutoff = invisible, not zero)
- Off-platform attention is proxy-based
- 14-title sample — directional, not statistically definitive
- Diagnostics framework, not causal effectiveness model

## 7. Connection to Portfolio

- **Project A** explains market structure (competitive pressure)
- **Project B** explains content investment logic (efficiency, export value)
- **Project C** explains title-level launch trajectory (early signal, staying power)

Together: **market context → investment framework → launch health diagnostics**
