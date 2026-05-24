import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Dataset setup ---
rng = np.random.default_rng(seed=42)
n = 200

df = pd.DataFrame({
    "student_id": range(1, n + 1),
    "name":       [f"Student_{i}" for i in range(1, n + 1)],
    "major":      rng.choice(["CS", "Math", "Physics", "Biology"], size=n),
    "year":       rng.integers(1, 5, size=n),
    "score_1":    rng.uniform(0, 10, size=n).round(2),
    "score_2":    rng.uniform(0, 10, size=n).round(2),
    "score_3":    rng.uniform(0, 10, size=n).round(2),
    "city":       rng.choice(["CDMX", "GDL", "MTY", "Unknown"], size=n, p=[0.4, 0.3, 0.2, 0.1]),
})

df["average"] = (df["score_1"] + df["score_2"] + df["score_3"]) / 3

conditions = [df["average"] >= 9.0, df["average"] >= 7.0, df["average"] >= 5.0]
df["grade"] = np.select(conditions, ["A", "B", "C"], default="D")

# Usa el dataset del bloque anterior (estudiantes con major, year,
# score_1/2/3, average, grade). Genera las siguientes visualizaciones,
# cada una en su propia Figure con título, labels y grid donde aplique:
#
# 1. Histograma de "average" con 20 bins.
#    Agrega una línea vertical en la media.
#
# 2. Subplot 1×2:
#    - Izquierda: boxplot de "average" por "major"
#    - Derecha:   boxplot de "average" por "year"
#
# 3. Scatter plot: score_1 en X, score_2 en Y.
#    Colorea los puntos según "major" usando hue de Seaborn.
#
# 4. Heatmap de correlación entre score_1, score_2, score_3 y average.
#
# 5. Countplot (sns.countplot) de "grade" mostrando cuántos
#    estudiantes obtuvieron cada calificación (A/B/C/D),
#    ordenado de A a D.
#
# Todos los plots deben guardarse como PNG con plt.savefig()
# antes de plt.show().

# Exercise 1
fig, ax = plt.subplots(figsize=(8, 5))
mean_val = df["average"].mean()
ax.hist(df["average"], bins=20, color="steelblue", edgecolor="white", alpha=0.8)
ax.axvline(mean_val, color="red", linestyle="--", label=f"mean = {mean_val:.2f}")
ax.set_title("Average Grade")
ax.set_xlabel("Grade")
ax.set_ylabel("Count")
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig("exercise_1.png", dpi=150)   # ← faltaba esto
plt.show()

# Exercise 2
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
majors = sorted(df["major"].unique())
data_by_major = [df[df["major"] == m]["average"].values for m in majors]
axes[0].boxplot(data_by_major, labels=majors, patch_artist=True)
axes[0].set_title("Average by Major")
axes[0].set_xlabel("Major")
axes[0].set_ylabel("Average")
axes[0].grid(True, axis="y", alpha=0.3)

years = sorted(df["year"].unique())
data_by_year = [df[df["year"] == y]["average"].values for y in years]
axes[1].boxplot(data_by_year, labels=years, patch_artist=True)
axes[1].set_title("Average by Year")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Average")
axes[1].grid(True, axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("exercise_2.png", dpi=150)
plt.show()

# Exercise 3
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(
    data=df,
    x="score_1",
    y="score_2",
    hue="major",
    palette="muted",
    alpha=0.7,
    ax=ax
)

ax.set_title("score_1 vs score_2 by Major")
ax.set_xlabel("Score 1")
ax.set_ylabel("Score 2")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("exercise_3.png", dpi=150)
plt.show()

# Exercise 4
fig, ax = plt.subplots(figsize=(7, 6))
corr_matrix = df[["score_1", "score_2", "score_3", "average"]].corr()
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1, vmax=1,
    square=True,
    linewidths=0.5,
    ax=ax
)

ax.set_title("Feature Correlation Matrix")
plt.tight_layout()
plt.savefig("exercise_4.png", dpi=150)
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))

sns.countplot(
    data=df,
    x="grade",
    order=["A", "B", "C", "D"],
    palette="muted",
    ax=ax
)

for bar in ax.patches:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        int(bar.get_height()),
        ha="center",
        va="bottom",
        fontsize=11
    )

ax.set_title("Students per Grade")
ax.set_xlabel("Grade")
ax.set_ylabel("Count")
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("exercise_5.png", dpi=150)
plt.show()