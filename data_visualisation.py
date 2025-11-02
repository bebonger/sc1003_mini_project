import matplotlib.pyplot as plt

def read_and_parse_file_content(filepath):
    records = {}
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        lines = content.split("\n")

        # First line is the header
        for line in lines[1:]:
            if not line.strip():
                continue

            record = line.split(",")

            tutorial_group = record[0]
            student_id     = record[1]
            school          = record[2]
            name            = record[3]
            gender          = record[4]
            cgpa            = record[5]
            team            = record[6]

            if tutorial_group not in records:
                records[tutorial_group] = []

            records[tutorial_group].append({
                "tutorial_group": tutorial_group,
                "student_id": student_id,
                "school": school,
                "name": name,
                "gender": gender,
                "cgpa": float(cgpa),
                "team": int(team)
            })
    return records


# load dataset
file_path = "diversified_teams.csv"
records = read_and_parse_file_content(file_path)

# flatten data
all_records = [r for group in records.values() for r in group]

# overall gpa distribution
cgpas = [r["cgpa"] for r in all_records]
plt.figure(figsize=(8,5))
plt.hist(cgpas, bins=20, edgecolor='black')
plt.title("Overall GPA Distribution")
plt.xlabel("GPA")
plt.ylabel("Number of Students")
plt.show()

# overall gender ratio
genders = {}
for r in all_records:
    g = r["gender"]
    genders[g] = genders.get(g, 0) + 1

plt.figure(figsize=(6,6))
plt.pie(genders.values(), labels=genders.keys(), autopct="%1.1f%%", startangle=90)
plt.title("Overall Gender Ratio")
plt.show()

# average gpa by tutorial group
avg_gpa_by_group = {}
for g, rows in records.items():
    total = sum(r["cgpa"] for r in rows)
    count = len(rows)
    avg_gpa_by_group[g] = total / count if count else 0

plt.figure(figsize=(10,5))
plt.bar(avg_gpa_by_group.keys(), avg_gpa_by_group.values(), color='skyblue', edgecolor='black')
plt.title("Average GPA by Tutorial Group")
plt.xlabel("Tutorial Group")
plt.ylabel("Average GPA")
plt.xticks(rotation=45)
plt.show()

# school diversity by tutorial group
diversity_by_group = {}
for g, rows in records.items():
    unique_schools = []
    for r in rows:
        if r["school"] not in unique_schools:
            unique_schools.append(r["school"])
    diversity_by_group[g] = len(unique_schools)

plt.figure(figsize=(10,5))
plt.bar(diversity_by_group.keys(), diversity_by_group.values(), color='lightgreen', edgecolor='black')
plt.title("School Diversity (Unique Schools) per Tutorial Group")
plt.xlabel("Tutorial Group")
plt.ylabel("Number of Unique Schools")
plt.xticks(rotation=45)
plt.show()

# gender ratios per tutorial group
groups = sorted(records.keys())
male_ratios, female_ratios = [], []

for g in groups:
    count_male = 0
    count_female = 0
    total = 0
    for r in records[g]:
        if r["gender"] == "Male":
            count_male += 1
        elif r["gender"] == "Female":
            count_female += 1
        total += 1

    male_ratio = count_male / total if total else 0
    female_ratio = count_female / total if total else 0
    male_ratios.append(male_ratio)
    female_ratios.append(female_ratio)

plt.figure(figsize=(10,6))
plt.bar(groups, male_ratios, label="Male", alpha=0.7)
plt.bar(groups, female_ratios, bottom=male_ratios, label="Female", alpha=0.7)
plt.title("Gender Ratio by Tutorial Group")
plt.xlabel("Tutorial Group")
plt.ylabel("Proportion")
plt.legend()
plt.xticks(rotation=45)
plt.show()
