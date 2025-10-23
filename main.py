import random
import math

# Return records group by tutorial group
def read_and_parse_file_content(filepath):
  records = {}
  with open(filepath, "r") as file:
    content = file.read()
    lines = content.split("\n")

    # First line is the header
    for line in lines[1:]:
      # Skip empty lines
      if not line:
        continue

      record = line.split(",")

      tutorial_group = record[0]
      student_id     = record[1]
      school        = record[2]
      name          = record[3]
      gender        = record[4]
      cgpa          = record[5]

      # Initialize empty list if not yet
      if not tutorial_group in records:
        records[tutorial_group] = []

      records[tutorial_group].append({
        'tutorial_group': tutorial_group,
        'student_id': student_id,
        'school': school,
        'name': name,
        'gender': gender,
        'cgpa': cgpa
      })

  return records

# This will categorise GPA based on the logic
# 
def categorise_gpa(gpa):
  return round(float(gpa) / 0.2, 2)

def get_max_count(items):
  max_count = 0
  uniq_items = set(items)

  for i in uniq_items:
    current_count = 0
    for j in items:
      if i == j:
        current_count += 1

    if current_count > max_count:
      max_count = current_count
  
  return max_count

def validate_team_constraints(team):
  school_count = get_max_count([s['school'] for s in team])
  # gender_count = get_max_count([s['gender'] for s in team])
  gpa_cat_count = get_max_count([categorise_gpa(s['cgpa']) for s in team])

  # print("School count: ", school_count, "Gender count: ", gender_count, "GPA count: ", gpa_cat_count)
  # print(school_count <= 2 and gender_count <= 2 and gpa_cat_count <= 2)
  return (school_count <= 2)

def calculate_diversity_score(team):
  schools = set([s['school'] for s in team ])
  cgpa    = set([categorise_gpa(s['cgpa']) for s in team])

  return len(schools) + len(cgpa)


def find_best_match_student(students, team):
  # Default to a random employee if no best match found
  best_match = random.sample(students, 1)[0]
  best_score = -1

  for student in students:
    temp_team = team.copy()
    temp_team.append(student)

    if not validate_team_constraints(temp_team):
      continue

    diversity_score = calculate_diversity_score(temp_team)

    if diversity_score > best_score:
      best_match = student

  return best_match


def split_project_teams(students, team_offset=1, team_size=5):
  students_count = len(students)

  num_teams = math.ceil(students_count / team_size)
  teams = {}

  males = []
  females = []

  for student in students:
    if student['gender'] == 'Male':
      males.append(student)
    else:
      females.append(student)

  available_students = [
    males.copy(),
    females.copy()
  ]

  for i in range(num_teams):
    group_number = i + team_offset

    teams[group_number] = []

    # If one gender is more than the other
    # We start with the one with the most students
    starting_index = 0 if (len(available_students[0]) > len(available_students[1])) else 1

    for i in range(team_size):
      gender_selection = (i + starting_index) % 2 # 0, 1 (mod2)

      selected_students = available_students[gender_selection]

      if not selected_students:
        gender_selection = (i + starting_index + 1) % 2
        selected_students = available_students[gender_selection]

      student = find_best_match_student(selected_students, teams[group_number])
      teams[group_number].append(student)
      selected_students.remove(student)

      if not available_students[0] and not available_students[1]:
        break

  return teams, group_number

def print_and_get_diversity_info(team, group_number):
  avergae_gpa = sum([float(s['cgpa']) for s in team]) / len(team)
  number_of_students = len(team)
  number_of_males = len([s for s in team if s['gender'] == 'Male'])
  number_of_females = len([s for s in team if s['gender'] == 'Female'])
  diversity_score   = calculate_diversity_score(team)
  schools = [s['school'] for s in team ]

  print("Group ", group_number, end=" | ")
  print("Tutorial Group", team[0]['tutorial_group'], end=" | ")
  print("Number of students: ", number_of_students, end=" | ")
  print("Schools max count: ", get_max_count(schools), end=" | ")
  print("Male: ", number_of_males, end=" | ")
  print("Female: ", number_of_females, end=" | ")
  print("Average GPA: ", avergae_gpa, end=" | ")
  print("Diversity Score: ", diversity_score)

  # if group_number >= 1073:
  #   for i in team:
  #     print(i['cgpa'])

  return diversity_score

if __name__ == "__main__":
  filepath = "records.csv"
  records = read_and_parse_file_content(filepath)

  teams = {}

  current_group_number = 1
  
  for tutorial_group in records:
    students = records[tutorial_group]
    current_teams, current_group_number = split_project_teams(students, current_group_number)

    teams = teams | current_teams

  total_count = 0
  total_diversity_score = 0

  for group_number in teams:
    team = teams[group_number]
    diversity_score = print_and_get_diversity_info(team, group_number)

    total_count += 1
    total_diversity_score += diversity_score

  # print(f"Average diversity score: %.2f", total_diversity_score / total_count)

  min_gpa = 5
  max_gpa = 0
  for tutorial_group in records:
    students = records[tutorial_group]
    for student in students:
      gpa = float(student['cgpa'])
      if gpa < min_gpa:
        min_gpa = gpa
      if gpa > max_gpa:
        max_gpa = gpa

  print("Min GPA: ", min_gpa)
  print("Max GPA: ", max_gpa)

    



