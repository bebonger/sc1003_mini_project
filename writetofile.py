def output_to_csv(teams):
  filepath = "diversified_teams.csv"
  with open(filepath, "w") as file:

    headers = "Tutorial Group,Student ID,School,Name,Gender,CGPA"

    # Write headers
    file.write(headers)