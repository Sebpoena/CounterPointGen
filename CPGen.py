#counterpoint shit
from google.colab import drive
import random

class Scale:
  def __init__(self, base):
    self.base = base
    self.scale = [i for i in range(120) if i % 12 in self.base]


cmaj = Scale([0, 2, 4, 5, 7, 9, 11])

#possibility generation functions
def possibleNotes(position, bass, scale):
  bareConsonances = [0, 3, 4, 7, 8, 9]
  consonanceList = [i for i in range(60) if i%12 in bareConsonances]
  currentNote = bass[position]
  possibilities = [(currentNote + i) for i in consonanceList if (currentNote + i) in scale.scale]
  return [i for i in possibilities if i in range(55, 82)]

def possibleNotes_2(position, bass, scale):
  bareConsonances = [0, 3, 4, 7, 8, 9]
  consonanceList = [i for i in range(60) if i%12 in bareConsonances]
  currentNote = bass[position]
  possibilities = [(currentNote + i) for i in consonanceList if (currentNote + i) in scale.scale]
  returnList = [i for i in possibilities if i in range(55, 82)]
  random.shuffle(returnList)
  return returnList

#validity functions
def isValid(position, bass, solution, note):
  if position == 0:
    return True
  parallels = [0, 7]
  if (note - bass[position]) % 12 in parallels:
    if (solution[position-1] - bass[position-1]) % 12 in parallels:
      return False
  return True

def isValid_2(position, bass, solution, note):
  if position == 0:
    return True
  parallels = [0, 7]
  if (note - bass[position]) % 12 in parallels:
    if (solution[position-1] - bass[position-1]) % 12 in parallels:
      return False
  if note == solution[position - 1]:
    return False
  return True

def isValid_3(position, bass, solution, note):
  if position == 0:
    return True
  parallels = [0, 7]
  if (note - bass[position]) % 12 in parallels:
    if (solution[position-1] - bass[position-1]) % 12 in parallels:
      return False
  if note == solution[position - 1] or abs(note - solution[position - 1]) >= 8:
    return False
  return True

def isValid_4(position, bass, solution, note):
  if position == 0:
    return True
  parallels = [0, 7]
  if (note - bass[position]) % 12 in parallels:
    if (solution[position-1] - bass[position-1]) % 12 in parallels:
      return False
  if note == solution[position - 1] or abs(note - solution[position - 1]) >= 7 or abs(note - solution[position - 1]) == 6:
    return False
  return True

#solver functions
def solveCP(position, bass, solution, scale):
  if position == len(bass):
    return solution
  for note in possibleNotes_2(position, bass, scale)[::-1]:
    if isValid_4(position, bass, solution, note):
      solution.append(note)
      result = solveCP(position + 1, bass, solution, scale)
      if result != None:
        return result
      solution.pop()
  return "no path"

cantusFirmus = [48, 57, 55, 53, 52, 55, 53, 50, 52, 53, 55, 59, 60]
print(solveCP(0, cantusFirmus, [], cmaj))

#results
"""
is valid_1 attempts:
with possible_1
first = [55, 60, 55, 57, 55, 55, 57, 57, 55, 57, 55, 62, 60]
second = [81, 81, 76, 81, 79, 79, 81, 81, 79, 81, 79, 79, 81]
with possible_2
[72, 60, 64, 69, 79, 76, 62, 57, 79, 72, 71, 79, 64]

is valid_2 attempts:
with possible_1
first = [55, 60, 55, 57, 55, 59, 57, 59, 55, 57, 55, 62, 60]
second = [81, 77, 79, 81, 79, 76, 81, 77, 79, 81, 79, 74, 81]
with possible_2
[69, 65, 59, 72, 67, 76, 60, 71, 59, 62, 67, 62, 64]

is valid_3 + possible_2:
[69, 76, 71, 65, 67, 71, 65, 71, 72, 65, 64, 71, 69]

is valid_4 + possible_2
[72, 77, 79, 81, 79, 74, 69, 71, 72, 74, 79, 74, 79]
"""
