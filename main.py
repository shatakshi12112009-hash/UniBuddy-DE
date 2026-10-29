
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("deadlines.json")

VOCABULARY = {
    "Klausur": "Written exam",
    "Vorlesung": "Lecture",
    "Übung": "Exercise class",
    "Abgabe": "Submission",
    "Prüfungsordnung": "Examination regulations",
    "Werkstudent": "Working student",
    "Sprechstunde": "Office hours",
}


def load_deadlines():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save_deadlines(deadlines):
    DATA_FILE.write_text(
        json.dumps(deadlines, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def add_deadline():
    title = input("Task or exam name: ").strip()
    if not title:
        print("Name cannot be empty.")
        return

    try:
        due = date.fromisoformat(input("Due date (YYYY-MM-DD): ").strip())
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    if due < date.today():
        print("That date is in the past.")
        return

    deadlines = load_deadlines()
    deadlines.append({"title": title, "date": due.isoformat()})
    deadlines.sort(key=lambda item: item["date"])
    save_deadlines(deadlines)
    print("Deadline saved!")


def show_deadlines():
    deadlines = load_deadlines()
    if not deadlines:
        print("No deadlines yet. Add your first task!")
        return

    for item in sorted(deadlines, key=lambda x: x["date"]):
        due = date.fromisoformat(item["date"])
        days = (due - date.today()).days
        print(f"{item['title']} | {due} | {days} day(s) left")


def ects_calculator():
    try:
        ects = float(input("Enter ECTS credits: "))
        if ects <= 0:
            print("Enter a number greater than zero.")
            return
        print(f"Estimated workload: {ects * 30:g} hours")
    except ValueError:
        print("Please enter a valid number.")


def vocabulary_quiz():
    score = 0
    for german, english in VOCABULARY.items():
        answer = input(f"What does '{german}' mean? ").strip()
        if answer.casefold() == english.casefold():
            print("Correct!")
            score += 1
        else:
            print(f"Answer: {english}")
    print(f"Your score: {score}/{len(VOCABULARY)}")


def main():
    while True:
        print("\n===== UNIBUDDY DE =====")
        print("1. Add a deadline")
        print("2. View deadlines")
        print("3. ECTS workload calculator")
        print("4. German vocabulary quiz")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_deadline()
        elif choice == "2":
            show_deadlines()
        elif choice == "3":
            ects_calculator()
        elif choice == "4":
            vocabulary_quiz()
        elif choice == "5":
            print("Good luck with your studies!")
            break
        else:
            print("Choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
