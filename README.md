# Ranking El Arte de Programar

Ranking para la asignatura "El Arte de Programar" de la UPM.

Este proyecto obtiene las notas públicas desde la página oficial, calcula los rankings por usuario y por problema y lo guarda en un archivo JSON que funcionará como base de datos para la página web.

## Qué hace
- Extrae datos de la página de notas oficial de la asignatura `http://138.100.11.198/notas`.
- Agrupa los datos por usuario y por problema.
- Calcula una puntuación acumulada por el nivel de los problemas (A, B, C, D) con topes parciales y un total final.
- Genera rankings globales de usuarios y rankings por problema.
- Guarda el resultado en `frontend/src/lib/data.json` (ruta configurada en `update.py`).

## Archivo de python
`update.py` — script en Python que:
- Hace la petición HTTP y parsea la tabla HTML (usa requests + BeautifulSoup).
- Suma calificaciones por nivel y aplica topes:
  ```python
  - max_a = min(5, total["A"])
  - max_b = min(7, max_a + total["B"])
  - max_c = min(9, max_b + total["C"])
  - max_d = min(10, max_c + total["D"])
  ```
- Calcula el ranking, los que tengan la misma nota, tendrán el mismo puesto en el ranking.
- Escribe JSON con la estructura principal:
  - `last_updated` (hora en Europe/Madrid)
  - `user_data` (por usuario: ranking, problems, grades -> A, AB, ABC, ABCD)
  - `problems_data` (por problema: contest_id, level, ranking por usuario)

Ruta de salida por defecto en el script:
```py
SAVE_FILE = "frontend/src/lib/data.json"
```

### Requisitos
- Python 3.8+
- Dependencias listadas en `requirements.txt`

### Cómo ejecutar (rápido)
1. Clona el repo:
```bash
git clone https://github.com/ivncd/eap_ranking.git
cd eap_ranking
```

2. Crea y activa un entorno virtual:
```bash
python3 -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta el script para actualizar los datos:
```bash
python update.py
```
Al finalizar se habrá creado/actualizado `frontend/src/lib/data.json` con los datos obtenidos.

## Frontend
La interfaz está en la carpeta `frontend` (Svelte + TypeScript + TailwindCSS + Shadcn-svelte).

Para ejecutarla localmente:
```bash
cd frontend
npm install
npm run dev # npm run build
```
El frontend utiliza los datos obtenidos por el script de python (`frontend/src/lib/data.json`) para mostrar el ranking.

## Workflow
Este proyecto contiene un `workflow` que se ejecuta todos los jueves a las 18:20 UTC, cuando termina el concurso de ese día:
- Automaticamente ejecutará el script de python actualizando los datos.
- Compilará el `frontend` y ejecuta `npm run build`
- Generá un commit y lo subirá a la rama  `gh-pages`, actualizando la página de Github Pages.  

## Estructura de interés
- `update.py` — Script de extracción y generación de JSON.
- `frontend/` — Aplicación Svelte que muestra los datos.

## Notas
- Se excluyen registros con `contest_id == 11` ya que no se tienen en cuenta para la nota.
- La hora en el JSON está en zona `Europe/Madrid`.
