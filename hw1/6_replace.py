#!/usr/bin/env python3

# Huibo Zhao
# Feb.18th.2018


# This function replace infrequent words with symbol _ABR_,_CAP_,_NUM_,_RARE_
def replace_rare(filename,newFilename):
    word_count = {}
    text = open(filename,"r")
    for line in text:
        tokens = line.strip().split(" ")
        if (len(tokens) > 1):  #ignore spaces
            if(tokens[0] in word_count):
                word_count[tokens[0]] += 1
            else:
                word_count[tokens[0]] = 1
    text.close()

    with open(filename) as text:
        with open(newFilename, 'w') as new_text:
            for line in text:
                tokens = line.strip().split(" ")
                if (len(tokens) > 1):
                    word = tokens[0]
                    symbol = tokens[1]
                    if (word_count[word] < 5):

                        if word.isupper() and word[len(word)-1] == '.':
                            new_word = "_ABR_" #abbreviation
                        elif word.isupper():
                            new_word = "_CAP_" #capitalized
                        elif word.isdigit():
                            new_word = "_NUM_"
                        else:
                            new_word = "_RARE_"



                        line_temp = new_word + " " + symbol + "\n"
                        new_text.write(line_temp)
                    else:
                        new_text.write(line)
                else:
                    new_text.write(line)
    return word_count



replace_rare("ner_train.dat","ner_train_rare2.dat")
