import requests
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
from requests.api import get
from tabulate import tabulate

from datetime import datetime
from zoneinfo import ZoneInfo

spain_tz = ZoneInfo("Europe/Madrid")
now_spain = datetime.now(spain_tz).strftime("%d/%m/%Y %H:%M")

URL = "http://138.100.11.198/notas"
INDEX_FILE = "index.md"
FINISHED_CSV = "finished.csv"

def obtain_text():
    r = requests.get(URL)
    return r.text

def obtain_data(text : str):
    result = defaultdict(list)
    soup = BeautifulSoup(text, "lxml")
    tr = soup.find_all("tr")
    for row in tr[1:]:
        mat, user, problem_id, contest_id, level, grade = [col.getText().strip() for col in row.children if col.getText().strip() != ""]
        contest_id = int(contest_id)
        problem_id = int(problem_id)
        grade = float(grade)

        if contest_id == 11:
            continue

        result[user].append((mat, user, problem_id, contest_id, level, grade))

    return result

def obtain_grades(result):
    grades = {}
    for user, values in result.items():
        total = defaultdict(int)
        for value in values:
            level, grade = value[4], value[5]
            total[level] += grade

        max_a = min(5, total["A"])
        max_b = min(7, max_a + total["B"])
        max_c = min(9, max_b + total["C"])
        max_d = min(10, max_c + total["D"])

        grades[user] = (max_a, max_b, max_c, max_d)

    return grades.items()

def get_ranking_table(grades_list):
    table = []
    prev_grade = None
    rank = 0
    display_rank = 0

    for _, (user, grades) in enumerate(grades_list):
        total = grades[-1]

        if total == 9:
            continue

        rank += 1
        if total != prev_grade:
            display_rank = rank
            prev_grade = total
        table.append([display_rank, user, *grades])

    return tabulate(
        table,
        headers=["Ranking", "Usuario", "Nota A /5", "Nota A+B /7", "Nota A+B+C /9", "Nota A+B+C+D /10"],
        tablefmt="github"
    )

def get_csv_data():
    return pd.read_csv(FINISHED_CSV)

def save_csv(df):
    df.to_csv(FINISHED_CSV, index=False)
    
def get_finished_table(grades_list):
    df = get_csv_data()
    rank = 0
    current_date = datetime.now().strftime("%d/%m/%Y")

    if not df.empty:
        rank = df["Rank"].iloc[-1]

    rank += 1
    for _, (user, grades) in enumerate(grades_list):
        total = grades[-1]
        if total != 9 or user in df["Usuario"].values:
            continue

        df.loc[len(df)] = [rank, user, current_date]

    save_csv(df)

    return tabulate(
        df,
        headers=["Ranking", "Usuario", "Fecha fin"],
        tablefmt="github",
        showindex=False
    )


def create_index(ranking_table : str, finished_table : str) -> str:
    result = "# Clasificación El Arte de Programar 2025\n\n"

    # result += "[Ranking](#clasificación-el-arte-de-programar-2025) • [Ranking final](#clasificación-final)</center>"
    result += "<div style='display: flex; justify-content: center; gap: 1em'>"
    result += "<a href='#clasificación-el-arte-de-programar-2025'>Ranking</a>"
    result += "<p>•</p>"
    result += "<a href='#clasificación-final'>Ranking final</a>"
    result += "</div>"
    result += "\n\n"

    result += f"*Última actualización: {now_spain}*\n\n"
    result += ranking_table
    result += "\n\n"
    result += "\n\n---\n\n"
    result += "\n\n"
    result += "## Clasificación final\n\n"
    result += finished_table

    return result

def start():
    text = obtain_text()
    result = obtain_data(text)
    grades = sorted(obtain_grades(result), key=lambda x: -x[1][-1])

    ranking_table = get_ranking_table(grades)
    finished_table = get_finished_table(grades)

    index = create_index(ranking_table, finished_table)
    with open(INDEX_FILE, "w+") as f:
        f.write(index)

if __name__ == "__main__":
    start()
