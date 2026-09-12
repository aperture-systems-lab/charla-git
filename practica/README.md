# La práctica

Resuelve un reto de [Deep-ML](https://www.deep-ml.com/problems) y súbelo a este
repositorio con un **fork** y un **pull request**.

## Qué entregas

Un solo archivo, dentro de una carpeta con tu nombre de usuario:

```
practica/retos/<tu-usuario>/<nombre-del-reto>.py
```

- `<tu-usuario>`: tu usuario de GitHub (`github.com/JeroHoyos` → `JeroHoyos`).
- `<nombre-del-reto>`: el título del reto en minúsculas y con guiones
  (*Matrix-Vector Dot Product* → `matrix-vector-dot-product`).

Ejemplo: `practica/retos/JeroHoyos/matrix-vector-dot-product.py`

Dentro del archivo: el enlace al reto arriba y tu solución debajo.

```python
# Link del reto: https://www.deep-ml.com/problems/1

def matrix_dot_vector(a, b):
    ...
```

La rama se llama igual que tu carpeta: tu usuario de GitHub, tal cual.

```
JeroHoyos
```

Y los commits siguen [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/),
como se vio en la charla.

```
feat(retos): solucion de JeroHoyos a matrix-vector-dot-product
```

## Cómo se hace

Con lo que viste en la charla ya tienes todo para hacer el recorrido completo:

```
   Deep-ML                     resuelves el reto y pasan los tests
        |
        |  solución lista
        v
   el original                 aperture-systems-lab/charla-git
        |
        |  fork
        v
   tu fork                     tu-usuario/charla-git
        |
        |  clone
        v
   tu computador               rama -> archivo con tu solución -> commit
        |
        |  push
        v
   tu fork
        |
        |  pull request
        v
   el original                 tu solución queda propuesta
```

Ahí termina el ejercicio práctico: tu código ya está propuesto al repositorio
original y solo falta que se revise.

## Condiciones para aprobar el pull request

- El reto pasa los tests en Deep-ML.
- Tu rama se llama como tu usuario de GitHub.
- Tu archivo está en `practica/retos/<tu-usuario>/`.
- El pull request va de tu rama hacia el `main` del original, no al revés.
- El pull request solo toca archivos dentro de tu carpeta.
- Los commits están realizados usando buenas prácticas