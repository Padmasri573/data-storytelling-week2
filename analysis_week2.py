"""
Week 2 Task - Advanced Data Visualization and Storytelling with Python
Dataset: Gapminder (life expectancy, GDP per capita, population - 142 countries, 1952-2007)
Source: plotly.express built-in gapminder dataset (originally from gapminder.org)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 150
CHART_DIR = "charts"

df = pd.read_csv("gapminder.csv")
print("Shape:", df.shape)
print(df.dtypes)
print("Years covered:", sorted(df.year.unique()))
print("Continents:", df.continent.unique())
print("Missing values:\n", df.isnull().sum())

continent_colors = {
    "Africa": "#E07B39", "Americas": "#4C72B0", "Asia": "#C44E52",
    "Europe": "#55A868", "Oceania": "#8172B2",
}

# ---------------------------------------------------------------------------
# CHART 1 - The Global Trend: life expectancy by continent over time (line)
# ---------------------------------------------------------------------------
avg_by_cont_year = df.groupby(["continent", "year"], observed=True)["lifeExp"].mean().reset_index()

fig, ax = plt.subplots(figsize=(9, 5.5))
for cont, group in avg_by_cont_year.groupby("continent", observed=True):
    ax.plot(group["year"], group["lifeExp"], marker="o", linewidth=2.5,
            label=cont, color=continent_colors.get(cont))
ax.set_title("Life Expectancy Has Risen on Every Continent Since 1952", fontsize=14, weight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Average Life Expectancy (years)")
ax.legend(title="Continent", loc="lower right")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/01_life_expectancy_trend.png")
plt.close()

# ---------------------------------------------------------------------------
# CHART 2 - The Wealth-Health Connection: GDP vs Life Expectancy, 1952 vs 2007
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
for ax, yr in zip(axes, [1952, 2007]):
    sub = df[df.year == yr]
    sizes = (sub["pop"] / sub["pop"].max()) * 1800 + 20
    for cont in sub.continent.unique():
        c = sub[sub.continent == cont]
        s = (c["pop"] / sub["pop"].max()) * 1800 + 20
        ax.scatter(c["gdpPercap"], c["lifeExp"], s=s, alpha=0.55,
                   color=continent_colors.get(cont), label=cont, edgecolor="white", linewidth=0.5)
    ax.set_xscale("log")
    ax.set_title(f"{yr}", fontsize=13, weight="bold")
    ax.set_xlabel("GDP per Capita (log scale, USD)")
axes[0].set_ylabel("Life Expectancy (years)")
axes[1].legend(title="Continent", loc="lower right", fontsize=9)
fig.suptitle("As Nations Grow Richer, Their People Tend to Live Longer - Bubble Size = Population", fontsize=14, weight="bold")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/02_gdp_vs_lifeexp_bubble.png")
plt.close()

# ---------------------------------------------------------------------------
# CHART 3 - Who's Ahead, Who's Behind: Top 15 vs Bottom 15 countries, 2007 (Plotly)
# ---------------------------------------------------------------------------
df_2007 = df[df.year == 2007]
top15 = df_2007.nlargest(15, "lifeExp").sort_values("lifeExp")
bottom15 = df_2007.nsmallest(15, "lifeExp").sort_values("lifeExp")
ranked = pd.concat([bottom15, top15])
ranked["group"] = ["Lowest 15"] * 15 + ["Highest 15"] * 15

fig = px.bar(
    ranked, x="lifeExp", y="country", orientation="h", color="group",
    color_discrete_map={"Lowest 15": "#C44E52", "Highest 15": "#55A868"},
    labels={"lifeExp": "Life Expectancy (years)", "country": "", "group": ""},
    title="The Life Expectancy Gap: Lowest vs. Highest Countries, 2007",
    hover_data={"continent": True, "gdpPercap": ":.0f"},
)
fig.update_layout(
    title_font_size=18, title_x=0.5,
    margin=dict(l=10, r=10, t=60, b=10),
    font=dict(size=13),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
fig.write_image(f"{CHART_DIR}/03_lifeexp_top_bottom.png", width=1000, height=800, scale=2)

# ---------------------------------------------------------------------------
# CHART 4 - Population Growth by Continent (stacked area)
# ---------------------------------------------------------------------------
pop_by_cont_year = df.groupby(["year", "continent"], observed=True)["pop"].sum().reset_index()
pivot = pop_by_cont_year.pivot(index="year", columns="continent", values="pop") / 1e9  # billions

fig, ax = plt.subplots(figsize=(9, 5.5))
order = ["Oceania", "Europe", "Americas", "Africa", "Asia"]
ax.stackplot(pivot.index, [pivot[c] for c in order], labels=order,
             colors=[continent_colors[c] for c in order], alpha=0.85)
ax.set_title("Global Population Growth by Continent, 1952-2007", fontsize=14, weight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Population (billions)")
ax.legend(loc="upper left", title="Continent")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/04_population_growth_stacked.png")
plt.close()

# ---------------------------------------------------------------------------
# CHART 5 - Distribution of Life Expectancy by Continent: 1952 vs 2007 (box plot)
# ---------------------------------------------------------------------------
compare = df[df.year.isin([1952, 2007])].copy()
compare["year"] = compare["year"].astype(str)

fig, ax = plt.subplots(figsize=(9.5, 5.5))
sns.boxplot(data=compare, x="continent", y="lifeExp", hue="year", ax=ax,
            palette={"1952": "#B0B0B0", "2007": "#4C72B0"})
ax.set_title("Life Expectancy Spread by Continent: 1952 vs 2007", fontsize=14, weight="bold")
ax.set_xlabel("Continent")
ax.set_ylabel("Life Expectancy (years)")
ax.legend(title="Year")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/05_lifeexp_boxplot_comparison.png")
plt.close()

# ---------------------------------------------------------------------------
# CHART 6 - Spotlight on Outliers: GDP vs Life Expectancy, 2007 with annotations
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6.5))
for cont in df_2007.continent.unique():
    c = df_2007[df_2007.continent == cont]
    ax.scatter(c["gdpPercap"], c["lifeExp"], s=60, alpha=0.5,
               color=continent_colors.get(cont), label=cont, edgecolor="white", linewidth=0.4)
ax.set_xscale("log")
ax.set_xlabel("GDP per Capita (log scale, USD)")
ax.set_ylabel("Life Expectancy (years)")
ax.set_title("Outliers to the Wealth-Health Pattern, 2007", fontsize=14, weight="bold")
ax.legend(title="Continent", loc="lower right", fontsize=9)

highlight_countries = ["United States", "Cuba", "South Africa", "Kuwait", "Costa Rica", "Equatorial Guinea"]
for country in highlight_countries:
    row = df_2007[df_2007.country == country]
    if len(row):
        x, y = row["gdpPercap"].values[0], row["lifeExp"].values[0]
        ax.annotate(country, (x, y), textcoords="offset points", xytext=(8, 6),
                    fontsize=9, weight="bold",
                    arrowprops=dict(arrowstyle="-", color="gray", lw=0.8))
        ax.scatter([x], [y], s=110, facecolors="none", edgecolors="black", linewidth=1.3, zorder=5)

plt.tight_layout()
plt.savefig(f"{CHART_DIR}/06_outlier_spotlight.png")
plt.close()

# ---------------------------------------------------------------------------
# Supporting stats printed for the report
# ---------------------------------------------------------------------------
print("\n=== KEY STATS ===")
print("Global avg life expectancy 1952:", round(df[df.year == 1952]["lifeExp"].mean(), 1))
print("Global avg life expectancy 2007:", round(df[df.year == 2007]["lifeExp"].mean(), 1))

corr_2007 = np.corrcoef(np.log(df_2007["gdpPercap"]), df_2007["lifeExp"])[0, 1]
print("Correlation (log GDP per capita vs life expectancy), 2007:", round(corr_2007, 3))

pop_1952 = df[df.year == 1952]["pop"].sum() / 1e9
pop_2007 = df[df.year == 2007]["pop"].sum() / 1e9
print(f"World population 1952: {pop_1952:.2f}B -> 2007: {pop_2007:.2f}B")

for country in highlight_countries:
    row = df_2007[df_2007.country == country]
    if len(row):
        print(country, "GDP:", round(row['gdpPercap'].values[0]), "LifeExp:", round(row['lifeExp'].values[0], 1))

print("\nDONE - all charts saved to", CHART_DIR)
