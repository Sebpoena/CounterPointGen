#counterpoint shit
from google.colab import drive

class Scale:
  def __init__(self, base):
    self.base = base
    self.scale = [i for i in range(120) if i % 12 in self.base]


cmaj = Scale([0, 2, 4, 5, 7, 9, 11])
print(cmaj.scale)

def possibleNotes(position, bass, scale):
  bareConsonances = [0, 3, 4, 7, 8, 9]
  consonanceList = [i for i in range(60) if i%12 in bareConsonances]
  currentNote = bass[position]
  possibilities = [(currentNote + i) for i in consonanceList if (currentNote + i) in scale.scale]
  return [i for i in possibilities if i in range(55, 82)]

def isValid(position, bass, solution, note):
  if position == 0:
    return True
  parallels = [0, 7]
  if (note - bass[position]) % 12 in parallels:
    if (solution[position-1] - bass[position-1]) % 12 in parallels:
      return False
  return True

def solveCP(position, bass, solution, scale):
  if position == len(bass):
    return solution
  for note in possibleNotes(position, bass, scale):
    if isValid(position, bass, solution, note):
      solution.append(note)
      result = solveCP(position + 1, bass, solution, scale)
      if result != None:
        return result
      solution.pop()
  return "no path"

cantusFirmus = [48, 57, 55, 53, 52, 55, 53, 50, 52, 53, 55, 59, 60]
#first output = [55, 60, 55, 57, 55, 55, 57, 57, 55, 57, 55, 62, 60]
#second output = [81, 81, 76, 81, 79, 79, 81, 81, 79, 81, 79, 79, 81] 
print(solveCP(0, cantusFirmus, [], cmaj))
