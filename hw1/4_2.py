#!/usr/bin/env python3

# Huibo Zhao
# Feb.18th



import math


# This function return a list of frequent word
def frequent(filename):
    word_count = {}
    frequent_word = []
    text = open(filename,"r")
    for line in text:
        tokens = line.strip().split(" ")
        if (len(tokens) > 1):  #ignore spaces
            if(tokens[0] in word_count):
                word_count[tokens[0]] += 1
            else:
                word_count[tokens[0]] = 1
    text.close()

    for key in word_count:
        if word_count[key]>4:
            frequent_word.append(key)

    return frequent_word

frequent_word = frequent("ner_train.dat")
#print(frequent_word)


# This function returns a dictionary of count_y
def extract_countY(filename):
    count_y_dict = {}
    text = open(filename,"r")
    for line in text:
        tokens = line.strip().split(" ")
        if tokens[1] == "WORDTAG":
            label = tokens[2]
            count = int(tokens[0])
            if label in count_y_dict:
                count_y_dict[label] = count_y_dict[label] + count
            else:
                count_y_dict[label] = count

    text.close()

    return count_y_dict

count_y_dict = extract_countY("ner_rare.counts")
#print(count_y_dict)

def dict_emission(filename):
    dictionary = {}
    text = open(filename,"r")
    for line in text:
        tokens = line.strip().split(" ")
        if tokens[1] == "WORDTAG":
            label = tokens[2]
            count = int(tokens[0])
            word = tokens[3]
            dictionary[(word,label)] = count / count_y_dict[label]
    return dictionary

dictionary_emission = dict_emission("ner_rare.counts")



#dict_prob, dict_tag = emission_probability("ner_rare.counts")

def compute(word):
    taggers = ['O','I-PER','I-LOC','I-MISC','I-ORG','B-MISC','B-ORG','B-LOC']
    prob = 0
    tag_index = 0
    if word not in frequent_word:
        word = "_RARE_"

    for i in range(len(taggers)):
        if (word,taggers[i]) in dictionary_emission:
            temp_prob = dictionary_emission[(word,taggers[i])]
            prob = max(prob,temp_prob)
            if temp_prob == prob:
                tag_index = i

    return math.log(prob),taggers[tag_index]

#a,b = compute("south")
#print(a)
#print(b)



def entity_tagger(filename,outputFile):

    taggers = ['O','I-PER','I-LOC','I-MISC','I-ORG','B-MISC','B-ORG','B-LOC']

    with open(filename) as text:
        with open(outputFile, 'w') as new_text:
            for line in text:
                tokens = line.strip().split(" ")
                if tokens[0] == '': # emply line
                    new_text.write(line)
                else:
                    word = tokens[0]
                    a,b = compute(word)
                    new_line = word + " " + b + " " + str(a) + "\n"
                    new_text.write(new_line)


entity_tagger("ner_dev.dat","4_2.txt")
