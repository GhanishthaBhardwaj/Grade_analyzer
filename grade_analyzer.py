import csv

print("Welcome! This is a program that analyses student grades.")

def avg_score(data):
    if not data:
        return 0
    return sum(data.values()) / len(data)

def median_score(data):
    if not data:
        return 0
    vals = sorted(data.values())
    n = len(vals)
    mid = n // 2
    if n % 2 != 0:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2

def max_score(data):
    if not data:
        return 0
    return max(data.values())

def min_score(data):
    if not data:
        return 0
    return min(data.values())

def save_to_csv(data, filename="grades.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for name, marks in data.items():
            writer.writerow([name, marks])

def read_from_csv(filename="grades.csv"):
    data = {}
    skipped = 0
    try:
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            for lineno, row in enumerate(reader, start=1):
                # skip empty rows quickly
                if not row or all(cell.strip() == "" for cell in row):
                    skipped += 1
                    continue
                # if row has >=2 columns use first two
                if len(row) >= 2:
                    name = row[0].strip()
                    val = row[1].strip()
                else:
                    # maybe the file used space separator like "Dev 85"
                    parts = row[0].strip().split()
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        val = parts[1].strip()
                    else:
                        skipped += 1
                        continue
                # try to convert marks to int, skip if invalid
                try:
                    marks = int(val)
                except ValueError:
                    skipped += 1
                    continue
                if name == "":
                    skipped += 1
                    continue
                data[name] = marks
    except FileNotFoundError:
        raise
    return data, skipped

def print_analysis(marks_data):
    print("\n--- Analysis Result ---")
    print(f"Average:\t{avg_score(marks_data)}")
    print(f"Median:\t\t{median_score(marks_data)}")
    print(f"Max Score:\t{max_score(marks_data)}")
    print(f"Min Score:\t{min_score(marks_data)}")

    grades = {}
    a = b = c = d = f = 0
    for name, m in marks_data.items():
        if m >= 90:
            grades[name] = "A"; a += 1
        elif m >= 80:
            grades[name] = "B"; b += 1
        elif m >= 70:
            grades[name] = "C"; c += 1
        elif m >= 60:
            grades[name] = "D"; d += 1
        else:
            grades[name] = "F"; f += 1

    print("\nGrades\t\tTotal Students")
    print(f"A\t\t{a}\nB\t\t{b}\nC\t\t{c}\nD\t\t{d}\nF\t\t{f}")

    passed = [name for name in marks_data if marks_data[name] >= 40]
    failed = [name for name in marks_data if marks_data[name] < 40]

    print("-" * 40)
    print(f"Total Passed Students: {len(passed)}")
    print(f"Names: {', '.join(passed) if passed else 'None'}")
    print(f"Total Failed Students: {len(failed)}")
    print(f"Names: {', '.join(failed) if failed else 'None'}")

    print("\nName\t\tMarks\t\tGrade")
    print("-" * 35)
    for name, marks in marks_data.items():
        print(f"{name}\t\t{marks}\t\t{grades[name]}")

def main():
    while True:
        print("\n=== Grade Menu ===")
        print("1. Manual Input (Save to CSV)")
        print("2. CSV Input (Read grades.csv)")
        print("3. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Please enter a number (1, 2 or 3).")
            continue

        if choice == 3:
            print("Exiting program.")
            break

        if choice == 1:
            try:
                n = int(input("Enter number of students: "))
                marks_data = {}
                for i in range(n):
                    name = input(f"Enter name of student {i+1}: ").strip()
                    marks = int(input(f"Enter marks of {name}: ").strip())
                    marks_data[name] = marks
                save_to_csv(marks_data)
                print("Data saved to grades.csv successfully!")
                print_analysis(marks_data)

            except ValueError:
                print("Invalid input: marks must be integers. Try again.")
                continue

        elif choice == 2:
            try:
                marks_data, skipped = read_from_csv()
            except FileNotFoundError:
                print("grades.csv file not found. Use option 1 to create it first.")
                continue

            if not marks_data:
                print("No valid records found in grades.csv.")
                if skipped:
                    print(f"Skipped {skipped} bad/empty lines.")
                continue

            if skipped:
                print(f"Note: skipped {skipped} bad/empty lines while reading CSV.")
            print_analysis(marks_data)

        else:
            print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()


