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

# Calculate dynamic CGPA categories based on percentiles
def calculate_cgpa_categories(students, team_size=5):
  # Extract all CGPAs and sort them
  cgpas = sorted([float(s['cgpa']) for s in students])
  
  if not cgpas:
    return {}
  
  # Create percentile-based categories
  cgpa_to_category = {}
  num_categories = team_size
  students_per_category = len(cgpas) / num_categories
  
  for i, cgpa in enumerate(cgpas):
    category = min(int(i / students_per_category), num_categories - 1)
    cgpa_to_category[cgpa] = category
  
  return cgpa_to_category

# This will categorise GPA based on the logic
def categorise_gpa(gpa, cgpa_mapping=None):
  if cgpa_mapping is not None:
    return cgpa_mapping.get(float(gpa), 0)

# Helper method to get maximum count for the similar items
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

def calculate_diversity_score(team, cgpa_mapping=None):
  schools = set([s['school'] for s in team ])
  genders = set([s['gender'] for s in team])
  cgpa    = set([categorise_gpa(s['cgpa'], cgpa_mapping) for s in team])

  return len(schools) + len(cgpa) + len(genders)


def find_best_match_student(students, team, cgpa_mapping=None):
  # Default to a random employee if no best match found
  best_match = random.sample(students, 1)[0]
  best_score = -1

  for student in students:
    temp_team = team.copy()
    temp_team.append(student)

    diversity_score = calculate_diversity_score(temp_team, cgpa_mapping)

    if diversity_score > best_score:
      best_match = student
      best_score = diversity_score

  return best_match


def split_project_teams(students, team_offset=1, team_size=5):
  students_count = len(students)

  num_teams = math.ceil(students_count / team_size)
  teams = {}
  
  # Calculate CGPA categories based on team size
  cgpa_mapping = calculate_cgpa_categories(students, team_size)

  males = []
  females = []

  for student in students:
    if student['gender'] == 'Male':
      males.append(student)
    else:
      females.append(student)
      
  for i in range(num_teams):
    group_number = i + team_offset

    teams[group_number] = []

    # We assign students based on the gender proportion so that it's evenly distributed
    proportions = distribute_students_proportions([males, females], 'gender', team_size)

    for gender, size in proportions.items():
      selected_students = males if gender == 'Male' else females

      for _ in range(size):
        student = find_best_match_student(selected_students, teams[group_number], cgpa_mapping)
        teams[group_number].append(student)
        selected_students.remove(student)

      if not males and not females:
        break

  return teams, group_number

def distribute_students_proportions(student_by_categories, category, size):
  total_count = sum([len(cat) for cat in student_by_categories])

  result = {}

  remaining_allocation = size

  for index, students in enumerate(student_by_categories):
    
    if not students:
      continue

    cat = students[0][category]

    if index == len(student_by_categories) - 1:
      result[cat] = remaining_allocation
      break
    
    proportion = (len(students) / total_count) * size
    proportion = round(proportion)
    remaining_allocation -= proportion
    result[cat] = proportion
  
  return result

def print_and_get_diversity_info(teams):

  total_count = 0
  total_diversity_score = 0

  for group_number in teams:
    team = teams[group_number]

    avergae_gpa = sum([float(s['cgpa']) for s in team]) / len(team)
    number_of_students = len(team)
    number_of_males = len([s for s in team if s['gender'] == 'Male'])
    number_of_females = len([s for s in team if s['gender'] == 'Female'])
    diversity_score   = calculate_diversity_score(team)
    schools = [s['school'] for s in team ]

    total_count += 1
    total_diversity_score += diversity_score

    print("Group ", group_number, end=" | ")
    print("Tutorial Group", team[0]['tutorial_group'], end=" | ")
    print("Number of students: ", number_of_students, end=" | ")
    print("Schools max count: ", get_max_count(schools), end=" | ")
    print("Male: ", number_of_males, end=" | ")
    print("Female: ", number_of_females, end=" | ")
    print("Average GPA: ", avergae_gpa, end=" | ")
    print("Diversity Score: ", diversity_score)

def print_min_max_gpa(records):
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

def output_to_csv(teams):
  filepath = "diversified_teams.csv"
  with open(filepath, "w") as file:

    headers = "Group Number,Tutorial Group,Student ID,School,Name,Gender,CGPA"

    # Write headers of csv file
    file.write(headers)

    # iterate through teams and write them to the csv file
    for group_number in teams:
      team = teams[group_number]
      for student in team:
        row_output = f"{group_number},{student['tutorial_group']},{student['student_id']},{student['school']},{student['name']},{student['gender']},{student['cgpa']}\n"
        file.write(row_output)

if __name__ == "__main__":
  filepath = "records.csv"
  records = read_and_parse_file_content(filepath)

  teams = {}

  current_group_number = 1
  
  for tutorial_group in records:
    students = records[tutorial_group]
    current_teams, current_group_number = split_project_teams(students, current_group_number)

    teams = teams | current_teams

  output_to_csv(teams)
  # print_and_get_diversity_info(teams)
  # print_min_max_gpa(records)