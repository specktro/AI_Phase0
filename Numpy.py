import numpy as np

# Dado el siguiente dataset simulado de 100 estudiantes con
# 4 features cada uno (notas en 4 materias, escala 0-10):
#
# rng = np.random.default_rng(seed=42)
# notas = rng.uniform(0, 10, size=(100, 4)).astype(np.float32)
#
# 1. Calcula la nota promedio de cada estudiante (axis correcto)
#    y agrega el resultado como columna al array original.
#
# 2. Encuentra los índices de los 5 estudiantes con mayor promedio.
#    Hint: np.argsort
#
# 3. Normaliza las notas al rango [0, 1] usando min-max scaling:
#    x_norm = (x - x_min) / (x_max - x_min)
#    Hazlo en una sola línea usando broadcasting, sin loops.
#
# 4. Crea una máscara booleana que identifique a los estudiantes
#    con promedio >= 7.0, y úsala para extraer sus notas.
#
# 5. Calcula la matriz de covarianza de las 4 materias.
#    Hint: np.cov — lee su documentación, el parámetro rowvar importa.

rng = np.random.default_rng(seed=42)
notes = rng.uniform(0, 10, size=(100, 4)).astype(np.float32)

# Exercise 1
averages = notes.mean(axis=1)
notes_ext = np.column_stack([notes, averages])

# Exercise 2
top5_index = np.argsort(averages)[-5:]
print("Top 5:\n", notes[top5_index])

# Exercise 3
x_min = notes.min(axis=0)
x_max = notes.max(axis=0)
x_norm = (notes - x_min) / (x_max - x_min)

print("Min by topic:", x_norm.min(axis=0))
print("Max by topic:", x_norm.max(axis=0))

## Exercise 4
mask = averages >= 7.0
approved = notes[mask]
print(f"\nApproved students: {approved.shape[0]}")

# Exercise 5
C = np.cov(notes, rowvar=False)
print("\nCovarianza shape:", C.shape)
print("Varianzas (diagonal):", np.diag(C))
print("Es simétrica:", np.allclose(C, C.T))
print(f"cov(Mat1, Mat2) = {C[0, 1]:.4f}")
print(f"var(Mat1)       = {C[0, 0]:.4f}")