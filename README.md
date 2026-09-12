# Git y GitHub

Charla **Una introducción a Git y GitHub** hecha en manim, con su parte práctica.

## Requisitos

- Python ≥ 3.13 (ver [.python-version](.python-version))
- [uv](https://docs.astral.sh/uv/) para gestionar el entorno y las dependencias

## Uso

```bash
# --- La presentación ---
cd presentacion
uv sync                                                        # instalar su entorno

uv run python -m manim_slides render main.py presentation      # renderizar
uv run python -m manim_slides present presentation             # presentar

# --- La parte práctica ---
cd practica
uv sync                                                        # instalar su entorno
```

## La práctica

Después de la charla viene la parte práctica: 

Resuelve un reto de [Deep-ML](https://www.deep-ml.com/problems) y aporta **a este mismo repositorio** con un fork y un pull request. El enunciado paso a paso está en [`practica/README.md`](practica/README.md).

## Bibliografía

### Artículos

- Driessen, V. (2010). *A successful Git branching model*. nvie.com. https://nvie.com/posts/a-successful-git-branching-model/ 
- Ma, E. J. *GitFlow for data science*. Essays on Data Science. https://ericmjl.github.io/essays-on-data-science/workflow/gitflow/
- *How to use Git for data science*. DagsHub. https://dagshub.com/blog/how-to-use-git-for-data-science/
- *Git flow for data science*. DagsHub. https://dagshub.com/blog/git-flow-for-data-science/
- *Linux statistics*. SQ Magazine. https://sqmagazine.co.uk/linux-statistics/ 
- *Conventional Commits 1.0.0*. conventionalcommits.org. https://www.conventionalcommits.org/es/v1.0.0/ 


### Vídeos

- Moure, B. (MoureDev). *Curso COMPLETO de GIT y GITHUB desde CERO para PRINCIPIANTES*. YouTube. https://www.youtube.com/watch?v=3GymExBkKjE
- Boot.dev. *Git and GitHub - Full Course*. YouTube. https://www.youtube.com/watch?v=rH3zE7VlIMs
- Boot.dev. *What is Git? | Course Intro by ThePrimeagen*. YouTube. https://www.youtube.com/watch?v=HQDeOxJeGfY
- Boot.dev. *You need to try git reflog*. YouTube. https://www.youtube.com/watch?v=atNg-nPhxJ8
- Boot.dev. *Git Fork vs Git Clone*. YouTube. https://www.youtube.com/watch?v=rxh6MhK6Tbs
- Boot.dev. *Common Git Log Options*. YouTube. https://www.youtube.com/watch?v=yQ73zvYlQtk
- Boot.dev. *What is git cherry pick?*. YouTube. https://www.youtube.com/watch?v=Q3Hg6PIghws
- Boot.dev. *What is Git Merge?*. YouTube. https://www.youtube.com/watch?v=BAtW9n5FgLM
- Boot.dev. *Git Revert vs Git Reset*. YouTube. https://www.youtube.com/watch?v=iIaM7j3tMuk
- Boot.dev. *How I use git stash*. YouTube. https://www.youtube.com/watch?v=_02z3tvMr4I
- Boot.dev. *What is a Merge Commit in Git?*. YouTube. https://www.youtube.com/watch?v=10PLCbsdXVI
- Boot.dev. *What is Git Rebase?*. YouTube. https://www.youtube.com/watch?v=nHcfoHOW4uA
- LearnThatStack. *Git Will Finally Make Sense After This*. YouTube. https://www.youtube.com/watch?v=Ala6PHlYjmw
- ByteByteGo. *How Git Works: Explained in 4 Minutes*. YouTube. https://www.youtube.com/watch?v=e9lnsKot_SQ
- ByteByteGo. *Git MERGE vs REBASE: Everything You Need to Know*. YouTube. https://www.youtube.com/watch?v=0chZFIZLR_0
- pildorasdeprogramacion. Git amend para arreglar tus commits de git. Youtube. https://www.youtube.com/shorts/u9SPJqK2bqM

### Datos y encuestas

- *Developer Survey 2022 — Version control*. Stack Overflow. https://survey.stackoverflow.co/2022/#technology-version-control

### Retos

- *Practice Problems*. Deep-ML. https://www.deep-ml.com/problems
