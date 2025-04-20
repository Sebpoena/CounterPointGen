#counterpoint shit
from google.colab import drive
import random

class Scale:
  def __init__(self, base):
    self.base = base
    self.scale = [i for i in range(120) if i % 12 in self.base]


cmaj = Scale([0, 2, 4, 5, 7, 9, 11])

#possibility generation functions
def possibleNotes(position, bass, solution, scale):
  bareConsonances = [0, 3, 4, 7, 8, 9]
  consonanceList = [i for i in range(60) if i%12 in bareConsonances]
  currentNote = bass[position]
  possibilities = [(currentNote + i) for i in consonanceList if (currentNote + i) in scale.scale]
  return [i for i in possibilities if i in range(55, 82)]

def possibleNotes_2(position, bass, solution, scale):
  bareConsonances = [0, 3, 4, 7, 8, 9]
  consonanceList = [i for i in range(60) if i%12 in bareConsonances]
  currentNote = bass[position]
  possibilities = [(currentNote + i) for i in consonanceList if (currentNote + i) in scale.scale]
  returnList = [i for i in possibilities if i in range(55, 82)]
  random.shuffle(returnList)
  return returnList

def possibleNotes_similar(position, bass, solution, scale):
  bareConsonances = [0, 3, 4, 7, 8, 9]
  consonanceList = [i for i in range(60) if i%12 in bareConsonances]
  currentNote = bass[position]
  possibilities = [(currentNote + i) for i in consonanceList if (currentNote + i) in scale.scale and (currentNote + i) in range(55, 82)]
  if position > 0:
    if bass[position] - bass[position - 1] > 0:
      returnList = [i for i in possibilities if i > solution[position - 1]]
    else:
      returnList = [i for i in possibilities if i < solution[position - 1]]
  else:
    returnList = possibilities
  random.shuffle(returnList)
  return returnList

def possibleNotes_contrary(position, bass, solution, scale):
  bareConsonances = [0, 3, 4, 7, 8, 9]
  consonanceList = [i for i in range(60) if i%12 in bareConsonances]
  currentNote = bass[position]
  possibilities = [(currentNote + i) for i in consonanceList if (currentNote + i) in scale.scale and (currentNote + i) in range(55, 82)]
  if position > 0:
    if bass[position] - bass[position - 1] > 0:
      returnList = [i for i in possibilities if i < solution[position - 1]]
    else:
      returnList = [i for i in possibilities if i > solution[position - 1]]
  else:
    returnList = possibilities
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

def isValid_5(position, bass, solution, note):
  if position == 0 and note % 12 in [0, 4, 7]:
    return True
  elif position == 0:
    return False
  parallels = [0, 7]
  prev = position - 1
  if (note - bass[position]) % 12 in parallels:
    if (solution[prev] - bass[prev]) % 12 in parallels:
      return False
  if note == solution[prev] or abs(note - solution[prev]) > 9 or abs(note - solution[prev]) == 6:
    return False
  return True

#solver functions
def solveCP(position, bass, solution, scale):
  if position == len(bass):
    return solution
  for note in possibleNotes_similar(position, bass, solution, scale):
    if isValid_5(position, bass, solution, note):
      solution.append(note)
      result = solveCP(position + 1, bass, solution, scale)
      if result != None:
        return result
      solution.pop()
  return None

cantusFirmus = [48, 57, 55, 53, 52, 55, 53, 50, 52, 53, 55, 59, 60]
for i in range(5):
  print(solveCP(0, cantusFirmus, [], cmaj))
