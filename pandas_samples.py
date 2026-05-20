import pandas as pd
import numpy as np

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
    "city":       rng.choice(["CDMX", "GDL", "MTY", None], size=n, p=[0.4, 0.3, 0.2, 0.1]),
})

# 1. Inspección inicial: muestra shape, dtypes, total de nulos por columna
#    y estadísticas descriptivas de las columnas numéricas.

# 2. Limpieza: rellena los nulos de "city" con "Unknown".

# 3. Agrega una columna "average" con el promedio de score_1, score_2 y score_3
#    para cada estudiante. Hazlo sin loops — solo operaciones de DataFrame.

# 4. Usando groupby, calcula para cada "major":
#    - promedio de "average"
#    - desviación estándar de "average"
#    - número de estudiantes
#    Muestra el resultado ordenado por promedio descendente.

# 5. Filtra los estudiantes con average >= 7.0 y year == 1.
#    ¿Cuántos hay? Muestra sus nombres y major.

# 6. Agrega una columna "grade" con las siguientes reglas:
#    average >= 9.0 → "A"
#    average >= 7.0 → "B"
#    average >= 5.0 → "C"
#    average <  5.0 → "D"
#    Hint: pd.cut o np.select — elige el que prefieras.

# Exercise 1 — initial inspection
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
print(df.describe())

# Exercise 2 — fill nulls
df["city"] = df["city"].fillna("Unknown")

# Exercise 3 — average column, no loops
df["average"] = (df["score_1"] + df["score_2"] + df["score_3"]) / 3

# Exercise 4 — groupby with agg
summary = (
    df.groupby("major")["average"]
    .agg(mean="mean", std="std", count="count")
    .sort_values("mean", ascending=False)
)
print(summary)

# Exercise 5 — filter and report
filtered = df.query("average >= 7.0 and year == 1")
print(f"Students with average >= 7.0 in year 1: {len(filtered)}")
print(filtered[["name", "major"]])

# Exercise 6 — grade column with np.select
conditions = [
    df["average"] >= 9.0,
    df["average"] >= 7.0,
    df["average"] >= 5.0,
]
choices = ["A", "B", "C"]
df["grade"] = np.select(conditions, choices, default="D")
print(df[["name", "average", "grade"]].head(10))