import csv
import random

# Lists for generating random data
programmes = [
    "Computer Science", "Mathematics", "Physics", "Engineering", 
    "Biology", "Chemistry", "Economics", "Psychology", 
    "English Literature", "History"
]
schools = [
    "School of Technology", "School of Science", "School of Engineering", 
    "School of Arts", "School of Social Sciences", "School of Humanities"
]
years = [2020, 2021, 2022, 2023, 2024, 2025]

# Generate 1000 records
records = []
for student_id in range(1, 1001):
    record = {
        "student_id": student_id,
        "programme": random.choice(programmes),
        "school": random.choice(schools),
        "registration_year": random.choice(years)
    }
    records.append(record)

# Write to CSV
with open("registrations.csv", "w", newline="") as csvfile:
    fieldnames = ["student_id", "programme", "school", "registration_year"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print("Generated registrations.csv with 1000 records.")
