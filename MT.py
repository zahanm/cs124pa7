# -*- coding: utf-8 -*-

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
  sentences = readTextFromFile(filename+"-tag")
  return correctPosTags(sentences)


def runPosTagger(filename,path):
  if not path[-1] == '/':
    path += '/'
  os.system("java -mx600m -classpath "+path+"stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model "+path+"models/english-bidirectional-distsim.tagger -textFile "+filename+" > " + filename + "-tag")

hindi_names = frozenset(['Kabir', 'Kashi', 'Rāmānaṁda'])
prepositions = frozenset(['in_opposition_to'])

def correctPosTags(sentences):
  for i, s in enumerate(sentences):
    words = s.split()
    for j, w in enumerate(words):
      if POSless_word(w) in hindi_names:
        words[j] = POSless_word(w) + '_NNP'
      elif POSless_word(w) in prepositions:
        words[j] = POSless_word(w) + '_IN'
    sentences[i] = ' '.join(words)
  return sentences


def transformSentence(s):
  s = cleanCaseMarkers(s)
  s = moveVerb(s)
  s = reversePostpositions(s)
  s = supplementalCaseStuff(s)
  return s

def supplementalCaseStuff(s):
  words = s.split()
  if 'NE_IN' in words and 'did_VBD' in words[-2:]:
    did_pos = -2 + words[-2:].index('did_VBD')
    del words[did_pos] # remove did
    del words[words.index('NE_IN')]
  s = ' '.join(words)
  s = re.sub(r" KO_MARK "," ",s)
  return s

def cleanCaseMarkers(s):
  s = re.sub(r" (KE|KO|KA|ME)_[A-Z]+ "," \\1_MARK ",s)
  s = re.sub(r" NE_[A-Z]+ "," NE_IN ",s)
  s = re.sub(r" KE_MARK (\w+_(?:IN|TO)) "," \\1 ",s)
  s = re.sub(r" KA_MARK (\w+_(?:VB.?)) "," to_IN \\1 ",s)
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
    nounPhraseFound = False
    while i < len(words):
      if isNounPhrase(words[:i+1]):
        nounPhraseFound = True
      elif nounPhraseFound:
        break
      i += 1
    if i >= len(words):
      break
    rest, nexti = suckUpVerb(words[i:])
    words = words[:i] + rest
    i += nexti
  return ' '.join(words)


def suckUpVerb(words):
  followers = set(["NN","NNP","VBN","VBD"])
  i = 0
  while i < len(words):
    if re.match("VB.", POS(words[i])):
      # import pdb; pdb.set_trace()
      if i+1 < len(words) and POS(words[i+1]) in followers:
        return ([words[i], words[i+1]] + words[:i] + words[i+2:], i+2)
      return ([ words[i] ] + words[:i] + words[i+1:], i+1)
    i += 1
  # no verb found
  return (words, i+1)


def isNounPhrase(words):
  nnFound = False
  onlyOKbeforeNoun = set(["DT","JJ","NNP"])
  nounLabels = set(["NN","NNP","FW","POS",",","CC","IN","TO"])
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

def POSless_word(word):
  return '_'.join(word.split('_')[:-1])

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
  
  outfile = open('outputSoFar','w')
  for sentence in sentences:
    outfile.write("%s.\n" % sentence)
  outfile.close()

