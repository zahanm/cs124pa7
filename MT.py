import sys
import os
import re

def readDictFromFile(filename):
  toReturn = dict()
  dictFile = open(filename,'r')
  for i, line in enumerate(dictFile):
    lineParts = line.strip().split("\t")
    if len(lineParts) > 2:
      print "Beware! Weird formatting on line " + str(i) + "!"
    toReturn[lineParts[0]] = lineParts[1]
  dictFile.close()
  return toReturn

def readTextFromFile(filename):
  textFile = open(filename,'r')
  sentences = [line.strip() for line in textFile]
  textFile.close()
  return sentences


def translateWords(sentences,dictionary):
  newSentences = []
  for i, sentence in enumerate(sentences):
    newSentence = ""
    for word in sentence.strip().split(" "):
      if word == ',' or word == '-':
        newSentence = newSentence + word
      else:
        try:
          newSentence = newSentence + dictionary[word]
        except KeyError:
          import pdb; pdb.set_trace()
      newSentence = newSentence + " "
    newSentences.append(newSentence)
  return newSentences


def posTagSentences(sentences,path,filename='sentences'):
  outfile = open(filename,'w')
  for sentence in sentences:
    outfile.write("%s.\n" % sentence)
  outfile.close()
  
  runPosTagger(filename,path)
  return readTextFromFile(filename+"-tag")


def runPosTagger(filename,path):
  if not path[-1] == '/':
    path += '/'
  os.system("java -mx600m -classpath "+path+"stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model "+path+"models/english-bidirectional-distsim.tagger -textFile "+filename+" > " + filename + "-tag")


def transformSentence(s):
  s = cleanCaseMarkers(s)
  s = moveVerb(s)
  s = reversePostpositions(s)
  return s


def cleanCaseMarkers(s):
  s = re.sub(r" (KE|KO|KA|ME)_[A-Z]+ "," \\1_MARK ",s)
  s = re.sub(r" NE_[A-Z]+ "," NE_NE ",s)
  s = re.sub(r" KE_MARK (\w+_(?:IN|TO)) "," \\1 ",s)
  s = re.sub(r" (?:KA|KE)_MARK "," 's_POS ",s)
  return s


def reversePostpositions(s):
  words = s.split(" ")
  nounThings = set(["CD","NN","NNP","JJ","DT","FW","MARK",":"])
  toReturn = ""
  currentPhrase = ""

  for word in words:
    if POS(word) in nounThings:
      currentPhrase += word + " "
    elif POS(word) == "IN":
      toReturn += word + " "
      toReturn += currentPhrase
      currentPhrase = ""
    elif POS(word) not in nounThings:
      currentPhrase += word + " "
      toReturn += currentPhrase
      currentPhrase = ""

  return toReturn


def moveVerb(s):
  words = s.split()
  i = 0
  while i < len(words):
    while i < len(words) and isNounPhrase(words[:i+1]):
      i += 1
    if i >= len(words):
      break
    rest, nexti = suckUpVerb(words[i:])
    words = words[:i] + rest
    i += nexti
  return ' '.join(words)


def suckUpVerb(words):
  nounLabels = set(["NN","NNP"])
  i = 0
  while i < len(words):
    if re.match("VB.", POS(words[i])):
      # import pdb; pdb.set_trace()
      if i+1 < len(words) and POS(words[i+1]) in nounLabels:
        return ([words[i], words[i+1]] + words[:i] + words[i+2:], i+2)
      return ([ words[i] ] + words[:i] + words[i+1:], i+1)
    i += 1
  return (words + ['No-verb-found!'], i+2)


def isNounPhrase(words):
  nnFound = False
  onlyOKbeforeNoun = set(["DT","IN","TO","JJ","NNP"])
  nounLabels = set(["NN","NNP","FW","POS",",","CC"])
  nnFoundReversers = set([",","POS","CC"])
  for word in words:
    if nnFound and POS(word) in onlyOKbeforeNoun:
      return False
    if POS(word) in nounLabels:
      nnFound = True
    if POS(word) in nnFoundReversers:
      nnFound = False
    if POS(word) not in onlyOKbeforeNoun | nounLabels:
      return False
  return True



def POS(word):
  return word.split("_")[-1]

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print('usage: {0} <text_file> <dictionary_file> path/to/postagger/'.format(__file__))
    sys.exit(1)
  textFilename = sys.argv[1]
  dictFilename = sys.argv[2]
  posPath = sys.argv[3]

  wordDictionary = readDictFromFile(dictFilename)
  sentences = readTextFromFile(textFilename)
  
  sentences = translateWords(sentences,wordDictionary)
  sentences = posTagSentences(sentences,posPath)
  sentences = [transformSentence(s) for s in sentences]

  for sentence in sentences:
    print sentence
  
  outfile = open('output','w')
  for sentence in sentences:
    outfile.write("%s.\n" % sentence)
  outfile.close()
