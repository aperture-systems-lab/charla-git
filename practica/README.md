# Ejercicio Práctico

Resuelve un reto de [Deep-ML](https://www.deep-ml.com/problems) y súbelo a este
repositorio con un **fork** y un **pull request**. 
>Lee cuidadosamente las instrucciones

## Intrucciones y ejemplo de entrega

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

Ahora veremos cómo se realiza adecuadamente el merge 

## El merge

Antes de hacer el PR, realiza un merge a tu rama en la rama main usando:

```bash
git merge --no-ff <tu-usuario>
```

Sin `--no-ff` git haría un *fast-forward* y la rama desaparecería del grafo, como si nunca hubiera existido. 

Te debería salir así

```
git log --oneline --graph --all

*   cd60689 (HEAD -> main) Merge branch '<tu-usuario>'
|\
| * 12e237c (<tu-usuario>) feat(retos): solucion de <tu-usuario> a <nombre-del-reto>
|/
* 3f6b057 (origin/main) commit anterior
```

**¿Se abrió un editor raro?** 

Es Vim parchate, git lo abre para que escribas el mensaje del commit de merge, y ya viene con `Merge branch '<tu-usuario>'` puesto. Solo hay que guardar y salir: pulsa `Esc`, escribe `:wq` y dale `Enter`.


## Esquema

Con lo que viste en la charla ya tienes todo para hacer el recorrido completo:

```
   Deep-ML                     
        |
        |  solución lista
        v
   el original                
        |
        |  fork
        v
   Creas la rama y añades tu solución
        |
        |  merge
        v
   tu fork
        |
        |  pull request
        v
   el original                          
```

Con esto habrías acabado el ejercicio práctico

## Condiciones para aprobar el pull request

- El reto pasa los tests en Deep-ML.
- Tu rama se llama como tu usuario de GitHub.
- Tu archivo está en `practica/retos/<tu-usuario>/`.
- El pull request va de tu rama hacia el `main` del original, no al revés.
- El pull request solo toca archivos dentro de tu carpeta.
- Los commits están realizados usando buenas prácticas

