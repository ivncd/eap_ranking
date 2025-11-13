# Ranking El Arte de Programar

Ranking para la asignatura "El Arte de Programar" (UPM — Ingeniería Informática).

Este script en Python obtiene las notas desde la página de la asignatura (http://138.100.11.198/notas), procesa los datos y genera el fichero `index.md` con la clasificación actualizada (zona horaria: Europe/Madrid).

## Requisitos

- Python 3.9+  
- Dependencias (si existen) en `requirements.txt`:
  ```
  pip install -r requirements.txt
  ```

## Uso

1. Clona el repositorio:
   ```
   git clone https://github.com/ivncd/eap_ranking.git
   cd eap_ranking
   ```

2. Ejecuta el script:
   ```
   python ranking.py
   ```
   Esto descargará los datos, generará el ranking y sobrescribirá `index.md`.

## Notas

- El script filtra entradas con `contest_id == 11` (Concurso que no entraba en la nota).
- El fichero resultante incluye la hora de última actualización en horario de Madrid.
