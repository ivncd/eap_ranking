import requests
import json

from collections import defaultdict
from bs4 import BeautifulSoup

from typing import Dict

from datetime import datetime
from zoneinfo import ZoneInfo

spain_tz = ZoneInfo("Europe/Madrid")
now_spain = datetime.now(spain_tz).strftime("%d/%m/%Y %H:%M")

URL = "http://138.100.11.198/notas"
SAVE_FILE = "frontend/src/lib/data.json"
# SAVE_FILE = "data.json"


def obtain_text():
    r = requests.get(URL)
    return r.text


def obtain_data(text: str):
    result = defaultdict(list)
    problems = defaultdict(dict)
    soup = BeautifulSoup(text, "lxml")
    tr = soup.find_all("tr")

    for row in tr[1:]:
        mat, user, problem_id, contest_id, level, grade = [
            col.getText().strip() for col in row.children if col.getText().strip() != ""
        ]
        contest_id = int(contest_id)
        problem_id = int(problem_id)
        grade = round(float(grade), 2)

        if contest_id == 11:
            continue

        if problem_id not in problems:
            problems[problem_id] = {
                "contest_id": contest_id,
                "level": level,
                "user_data": [],
            }

        # Handle duplicate problem IDs from different contests
        elif problems[problem_id]["contest_id"] != contest_id:
            exists = False
            while problem_id in problems:
                if problems[problem_id]["contest_id"] == contest_id:
                    exists = True
                    break

                problem_id += 0.1  # We assume there is no more than ten 10 instances of the same problem ID

            if not exists:
                problems[problem_id] = {
                    "contest_id": contest_id,
                    "level": level,
                    "user_data": [],
                }

        problems[problem_id]["user_data"].append({"user": user, "grade": grade})

        result[user].append(
            {
                "id": mat,
                "user": user,
                "pid": problem_id,
                "cid": contest_id,
                "level": level,
                "grade": grade,
            }
        )

    return result, problems


def obtain_grades(result):
    grades = {}
    for user, values in result.items():
        total = defaultdict(int)
        for value in values:
            value = list(value.values())
            level, grade = value[4], value[5]
            total[level] += grade

        max_a = round(min(5, total["A"]), 2)
        max_b = round(min(7, max_a + total["B"]), 2)
        max_c = round(min(9, max_b + total["C"]), 2)
        max_d = round(min(10, max_c + total["D"]), 2)

        grades[user] = (max_a, max_b, max_c, max_d)

    return grades


def get_user_ranks(grades_list):
    ranks = {}
    prev_grade = None
    rank, display_rank = 0, 0
    for _, (user, grades) in enumerate(grades_list):
        total = grades[-1]

        rank += 1
        if total != prev_grade:
            display_rank = rank
            prev_grade = total

        ranks[user] = display_rank

    return ranks


def get_problem_data(problems):
    problem_data = {}
    for problem_id in problems.keys():
        ordered = sorted(problems[problem_id]["user_data"], key=lambda x: -x["grade"])
        problem_data[problem_id] = {
            "contest_id": problems[problem_id]["contest_id"],
            "level": problems[problem_id]["level"],
            "ranking": {},
        }

        prev_grade = None
        rank, display_rank = 0, 0
        for user_data in ordered:
            grade = user_data["grade"]
            user = user_data["user"]

            rank += 1
            if grade != prev_grade:
                display_rank = rank
                prev_grade = grade

            problem_data[problem_id]["ranking"][user] = display_rank

    return problem_data


def create_database(result, grades, user_ranks, problem_data):
    final: Dict = {
        "last_updated": now_spain,
        "user_data": {},
        "problems_data": problem_data,
    }
    for user, user_grades in sorted(grades, key=lambda x: x[0]):
        problem_grades = {r["pid"]: r["grade"] for r in result[user]}

        final["user_data"][user] = {
            "ranking": user_ranks[user],
            "problems": problem_grades,
            "grades": {
                "A": user_grades[0],
                "AB": user_grades[1],
                "ABC": user_grades[2],
                "ABCD": user_grades[3],
            },
        }

    return final


def start():
    text = obtain_text()

    result, problems = obtain_data(text)
    grades = sorted(obtain_grades(result).items(), key=lambda x: -x[1][-1])
    user_ranks = get_user_ranks(grades)
    problem_data = get_problem_data(problems)

    data = create_database(result, grades, user_ranks, problem_data)
    with open(SAVE_FILE, "w+", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    start()
