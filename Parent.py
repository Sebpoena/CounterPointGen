#updated 3 voice counterpoint with recursion from sop to alt
from google.colab import drive

class Scale:
  def __init__(self, base, additive, triad = []):
    self.base = base
    self.additive = additive
    self.triad = triad
    if len(self.triad) == 0:
      self.triad = [(i + self.additive)%12 for i in [0, 4, 7]]
    self.scale = [i for i in range(120) if i % 12 in self.base]


cmaj = Scale([0, 2, 4, 5, 7, 9, 11], 0)
asmaj = Scale([0, 1, 3, 5, 7, 8, 10], 8)
fmin = Scale([0, 1, 3, 5, 7, 8, 10], 8, [0, 5, 8])

#soprano functions
def isValidSop(position, bass, alt, solution, scale, note):
  triad = [(i + scale.additive)%12 for i in [0, 4, 7]]
  if position == 0 and note % 12 in scale.triad:
    return True
  elif position == 0:
    #print('failed first validity')
    return False
  parallels = [0, 7]
  prev = solution[-1]
  if note == prev:
    return False
  if abs(note - prev) > 5:
    return False
  if (note - bass[position]) % 12 in parallels:
    if (solution[position-1] - bass[position-1]) % 12 in parallels:
      return False
  if (note - alt[position]) % 12 in parallels:
    if (solution[position-1] - alt[position-1]) % 12 in parallels:
      return False
  return True

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
  possibilities = sopScored(position, bass, alt, solution, scale)
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
  possibilities = sopScored(position, bass, alt, solution, scale)
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

def solveVoices(position, bass, solution, scale, pFunction):
  if position == len(bass):
    soprano = solveSop(0, [bass, solution], [], scale, pFunction)
    if soprano == None:
      return None
    else:
      return[bass, solution, soprano]
  for note in possibleAlt(position, bass, solution, scale):
    if isValidAlt(position, bass, solution, note):
      solution.append(note)
      result = solveVoices(position + 1, bass, solution, scale, pFunction)
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

#f minor, a flat major
arm1 = [48, 53, 52, 53]
arm2 = [53, 53, 55, 56]
arm3 = [55, 58, 56, 55, 53, 55, 52, 53]
arm4 = [56, 60, 58, 55, 58, 56]
arm5 = [56, 55, 53, 48, 56, 55, 53]

armPhrase = [arm1, arm2, arm3, arm4, arm5]

for i in armPhrase:
  print('---new--- reg')
  print(solveVoices(0, i, [], fmin, sopScored))

for i in armPhrase:
  print('---new--- cont')
  print(solveVoices(0, i, [], fmin, contScored))

for i in armPhrase:
  print('---new--- sim')
  print(solveVoices(0, i, [], fmin, simScored))

"""
for i in armPhrase:
  fullCP(i, asmaj)
print('normal')

for i in armPhrase:
  fullCP(i, asmaj, pFunction = "similar")
print('similar')

for i in armPhrase:
  fullCP(i, asmaj, pFunction = "contrary")
print('contrary')

---

fullCP(cf1, cmaj)
fullCP(cf1, cmaj, pFunction = "similar")
fullCP(cf1, cmaj, pFunction = "contrary")
fullCP(cf2, cmaj)
fullCP(cf2, cmaj, pFunction = "similar")
fullCP(cf2, cmaj, pFunction = "contrary")

---
interesting result
[[48, 53, 52, 53], [55, 56, 55, 56], [63, 61, 60, 61]]
---

results arm song: (major biased settings)

---new--- reg
[[48, 53, 52, 53], [55, 56, 55, 56], [63, 61, 60, 61]]
---new--- reg
[[53, 53, 55, 56], [56, 56, 58, 60], [60, 61, 63, 65]]
---new--- reg
[[55, 58, 56, 55, 53, 55, 52, 53], [55, 61, 60, 58, 56, 58, 55, 56], [60, 65, 60, 63, 61, 63, 60, 61]]
---new--- reg
[[56, 60, 58, 55, 58, 56], [56, 63, 61, 58, 61, 60], [60, 63, 65, 63, 65, 60]]
---new--- reg
[[56, 55, 53, 48, 56, 55, 53], [56, 58, 56, 55, 60, 58, 56], [60, 63, 61, 63, 65, 63, 61]]
---new--- cont
[[48, 53, 52, 53], [55, 56, 55, 56], [72, 68, 72, 68]]
---new--- cont
[[53, 53, 55, 56], [56, 56, 58, 60], [72, 73, 70, 65]]
---new--- cont
[[55, 58, 56, 55, 53, 55, 52, 53], [55, 61, 60, 58, 56, 58, 55, 56], [63, 61, 65, 67, 68, 63, 67, 65]]
---new--- cont
[[56, 60, 58, 55, 58, 56], [56, 63, 61, 58, 61, 60], [72, 68, 70, 75, 73, 75]]
---new--- cont
[[56, 55, 53, 48, 56, 55, 53], [56, 58, 56, 56, 60, 58, 56], [60, 63, 65, 68, 65, 67, 68]]
---new--- sim
[[48, 53, 52, 53], [55, 56, 55, 56], [63, 65, 60, 61]]
---new--- sim
[[53, 53, 55, 56], [56, 56, 58, 60], [68, 65, 70, 75]]
---new--- sim
[[55, 58, 56, 55, 53, 55, 52, 53], [55, 61, 60, 58, 56, 58, 55, 56], [72, 73, 68, 63, 61, 63, 60, 61]]
---new--- sim
[[56, 60, 58, 55, 58, 56], [56, 63, 61, 58, 61, 60], [63, 68, 65, 63, 65, 60]]
---new--- sim
[[56, 55, 53, 48, 56, 55, 53], [56, 58, 56, 55, 60, 58, 56], [72, 70, 65, 63, 65, 63, 61]]

--- updated logic in scale building for base triad
---new--- reg
[[48, 53, 52, 53], [55, 56, 55, 56], [60, 61, 60, 61]]
---new--- reg
[[53, 53, 55, 56], [56, 56, 58, 60], [60, 61, 63, 65]]
---new--- reg
[[55, 58, 56, 55, 53, 55, 52, 53], [55, 61, 60, 58, 56, 58, 55, 56], [60, 65, 60, 63, 61, 63, 60, 61]]
---new--- reg
[[56, 60, 58, 55, 58, 56], [56, 63, 61, 58, 61, 60], [60, 63, 65, 63, 65, 60]]
---new--- reg
[[56, 55, 53, 48, 56, 55, 53], [56, 58, 56, 55, 60, 58, 56], [60, 63, 61, 63, 65, 63, 61]]
---new--- cont
[[48, 53, 52, 53], [55, 56, 55, 56], [72, 68, 72, 68]]
---new--- cont
[[53, 53, 55, 56], [56, 56, 58, 60], [72, 73, 70, 65]]
---new--- cont
[[55, 58, 56, 55, 53, 55, 52, 53], [55, 61, 60, 58, 56, 58, 55, 56], [72, 70, 72, 75, 77, 75, 79, 77]]
---new--- cont
[[56, 60, 58, 55, 58, 56], [56, 63, 61, 58, 61, 60], [65, 60, 61, 63, 61, 63]]
---new--- cont
[[56, 55, 53, 48, 56, 55, 53], [56, 58, 56, 55, 60, 58, 56], [65, 70, 72, 75, 72, 75, 77]]
---new--- sim
[[48, 53, 52, 53], [55, 56, 55, 56], [60, 61, 60, 61]]
---new--- sim
[[53, 53, 55, 56], [56, 56, 58, 60], [65, 61, 63, 65]]
---new--- sim
[[55, 58, 56, 55, 53, 55, 52, 53], [55, 61, 60, 58, 56, 58, 55, 56], [72, 73, 68, 63, 61, 63, 60, 61]]
---new--- sim
[[56, 60, 58, 55, 58, 56], [56, 63, 61, 58, 61, 60], [65, 68, 65, 63, 65, 60]]
---new--- sim
[[56, 55, 53, 48, 56, 55, 53], [56, 58, 56, 55, 60, 58, 56], [65, 63, 61, 60, 65, 63, 61]]
"""
