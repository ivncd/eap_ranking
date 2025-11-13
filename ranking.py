import requests
from collections import defaultdict
from bs4 import BeautifulSoup
from tabulate import tabulate

from datetime import datetime
from zoneinfo import ZoneInfo

spain_tz = ZoneInfo("Europe/Madrid")
now_spain = datetime.now(spain_tz)

URL = "http://138.100.11.198/notas"
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

def get_table(grades_list):
    table = []
    prev_grade = None
    rank = 0
    display_rank = 0

    for pos, (user, grades) in enumerate(grades_list):
        total = grades[-1]
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


def transform_table(table : str) -> str:
    result = "# Clasificación El Arte de Programar 2025\n\n"

    spain_tz = ZoneInfo("Europe/Madrid")
    time = datetime.now(spain_tz).strftime("%d/%m/%Y %H:%M")
    result += "\n"
    result += f"*Última actualización: {time}*\n\n"
    result += table

    return result

def start():
    text = obtain_text()
    result = obtain_data(text)
    grades = sorted(obtain_grades(result), key=lambda x: -x[1][-1])

    table = transform_table(get_table(grades))

    with open("index.md", "w+") as f:
        f.write(table)

if __name__ == "__main__":
    start()
