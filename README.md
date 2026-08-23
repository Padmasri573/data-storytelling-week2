# Week 2 — Advanced Data Visualization & Storytelling with Python

Week 2 deliverable for a data science internship/course: going beyond basic charts to build a full data *narrative* — one that a non-technical reader can follow from start to finish, not just a folder of unconnected plots.

## The Story
**How the world got richer, healthier, and more crowded (1952–2007)** — told through the Gapminder dataset (142 countries, 12 years, life expectancy / GDP per capita / population).

The report follows a six-chapter arc:
1. Life expectancy rose on every continent — but the gap between them barely closed.
2. Richer nations live longer — the classic wealth-health relationship, shown 1952 vs. 2007.
3. The gap, named — the actual 15 highest and 15 lowest countries, side by side.
4. Population boomed almost 3x over — and Asia drove most of it.
5. "Continent average" hides a lot — some countries within the same region pulled far ahead of their neighbors.
6. The exceptions — Cuba and Costa Rica match US-level life expectancy at a fraction of the income; a reminder that money isn't the whole story.

## Contents
| File | Description |
|---|---|
| `Week2_Data_Storytelling_Report.docx` | Full report — introduction, methods, six annotated visual chapters, business/scientific implications, conclusion |
| `analysis_week2.py` | Python script generating all 6 visualizations (Matplotlib, Seaborn, Plotly) |
| `gapminder.csv` | Source dataset (142 countries × 12 years, no missing values) |
| `charts/` | All 6 exported visualizations |

## Why three libraries?
Different chart types call for different tools:
- **Matplotlib** — full manual control for annotated/comparison charts (trend line, bubble comparison, stacked area, outlier spotlight)
- **Seaborn** — fast, clean statistical comparison (the box-plot distribution)
- **Plotly** — polished horizontal bar chart with built-in hover metadata

## Tools
Python · Pandas · Matplotlib · Seaborn · Plotly
