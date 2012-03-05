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
  for sentence in sentences:
    newSentence = ""
    for word in sentence.strip().split(" "):
      if word == ',' or word == '-':
        newSentence = newSentence + word
      else:
        newSentence = newSentence + dictionary[word]
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
  s = reversePostpositions(s)
  return s


def cleanCaseMarkers(s):
  s = re.sub(r" (KE|NE|KO|KA|ME)_[A-Z]+ "," \\1_MARK ",s)
  s = re.sub(r" KE_MARK (\w+_IN) "," \\1 ",s)
  return s


def reversePostpositions(s):
  words = s.split(" ")
  nounThings = set(["CD","NN","NNP","JJ","DT","FW"])
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

