import sys
import csv
import Levenshtein

name=sys.argv[1:]
name=str(name)
def find_closest(user, names):
    distances = [(name, Levenshtein.distance(user.lower(), name.lower())) for name in names]
    closest_match = min(distances, key=lambda x: x[1])[0]
    return closest_match
with open('main.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    names = [name[1] for name in reader]
closest_name = find_closest(name, names)
print(closest_name)
