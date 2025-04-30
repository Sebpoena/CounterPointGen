#scored and organised CPgeneration
from google.colab import drive

class Scale:
  def __init__(self, base):
    self.base = base
    self.scale = [i for i in range(120) if i % 12 in self.base]


cmaj = Scale([0, 2, 4, 5, 7, 9, 11])

#alto functions - requires less complexity than sop
def possibleAlt(position, bass, solution, scale):
  bareConsonances = [0, 3, 4, 7, 8, 9]
  consonanceList = [i for i in range(60) if i%12 in bareConsonances]
  currentNote = bass[position]
  possibilities = [(currentNote + i) for i in consonanceList if (currentNote + i) in scale.scale]
  return [i for i in possibilities if i in range(55, 72)]

def isValidAlt(position, bass, solution, note):
  if position == 0:
    return True
  parallels = [0, 7]
  if note == bass[position]:
    return False
  if (note - bass[position]) % 12 in parallels:
    if (solution[position-1] - bass[position-1]) % 12 in parallels:
      return False
  return True

def solveAlt(position, bass, solution, scale):
  if position == len(bass):
    return solution
  for note in possibleAlt(position, bass, solution, scale):
    if isValidAlt(position, bass, solution, note):
      solution.append(note)
      result = solveAlt(position + 1, bass, solution, scale)
      if result != None:
        return result
      solution.pop()
  return None

#soprano functions
def score(position, bass, alt, solution, possibilities):
  """returns a list sorted by how well it abides by the priorities set out"""
  """the priorities are: note not already in chord, stepwise movement"""
  scoredNotes = []
  for note in possibilities:
    score = 0
    context = [(bass[position]%12), 
              (alt[position]%12)]
    if note % 12 in context:
      score -= 10
    else:
      score += 5
    if position != 0:
      prev = solution[position - 1]
      prevInterval = abs(note - prev)
      if prevInterval in (1, 2):
        score += 3
      elif prevInterval >= 7:
        score -=2
    scoredNotes.append((score, note))
  scoredNotes.sort(key=lambda x: x[0], reverse=True)
  return [note for score, note in scoredNotes]

def sopScored(position, bass, alt, solution, scale):
  """classic counterpoint, with no specific directional instructions"""
  bareConsonances = [0, 3, 4, 5, 7, 8, 9]
  consonanceList = [i for i in range(60) if i%12 in bareConsonances]
  currentBass = bass[position]
  currentAlt = alt[position]
  possibilities = [i for i in scale.scale if abs(i - currentAlt) in consonanceList and abs(i - currentBass) in consonanceList and i in range(60,82)]
  scored = score(position, bass, alt, solution, possibilities)
  return scored

def contScored(position, bass, alt, solution, scale):
  """specifically prioritises contrary motion"""
  possibilities = possibleSop(position, bass, alt, solution, scale)
  if position > 0:
    if bass[position] - bass[position - 1] > 0:
      returnList = [i for i in possibilities if i < solution[position - 1]]
    else:
      returnList = [i for i in possibilities if i > solution[position - 1]]
  else:
    returnList = possibilities
  scored = score(position, bass, alt, solution, returnList)
  return scored

def simScored(position, bass, alt, solution, scale):
  """specifically prioritises similar motion"""
  possibilities = possibleSop(position, bass, alt, solution, scale)
  if position > 0:
    if bass[position] - bass[position - 1] > 0:
      returnList = [i for i in possibilities if i > solution[position - 1]]
    else:
      returnList = [i for i in possibilities if i < solution[position - 1]]
  else:
    returnList = possibilities
  scored = score(position, bass, alt, solution, returnList)
  return scored

def solveSop(position, twoVoices, solution, scale, pFunction):
  bass = twoVoices[0]
  alt = twoVoices[1]
  if position == len(bass):
    return solution
  for note in pFunction(position, bass, alt, solution, scale):
    if isValidSop(position, bass, alt, solution, scale, note):
      solution.append(note)
      result = solveSop(position + 1, twoVoices, solution, scale, pFunction)
      if result != None:
        return result
      solution.pop()
  return None

#parent function
def fullCP(cf, scale, pFunction = "classic"):
  alto = solveAlt(0, cf, [], scale)
  voices = [cf,
            alto]
  functions = {"classic": sopScored,
               "contrary": contScored,
               "similar": simScored}
  soprano = solveSop(0, voices, [], scale, functions.get(pFunction))
  voices.append(soprano)
  for i in voices:
    print(i)
  return voices

cf1 = [48, 57, 55, 53, 52, 55, 53, 50, 52, 53, 55, 59, 60]
cf2 = [48, 50, 52, 48, 53, 50, 52, 48, 57, 62, 59, 55, 60, 55, 48]
fullCP(cf1, cmaj)
fullCP(cf1, cmaj, pFunction = "similar")
fullCP(cf1, cmaj, pFunction = "contrary")
fullCP(cf2, cmaj)
fullCP(cf2, cmaj, pFunction = "similar")
fullCP(cf2, cmaj, pFunction = "contrary")
