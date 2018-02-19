#!/usr/bin/env python3

# Huibo Zhao
# Feb.18th.2018

import math

def dict_trigrams(filename):
    bigram_dict = {}
    trigram_dict = {}


    text = open(filename,"r")

    for line in text:
        tokens = line.strip().split(" ")
        if tokens[1] == "2-GRAM":
            bigram_dict[(tokens[2],tokens[3])] = int(tokens[0])



        if tokens[1] == "3-GRAM":
            trigram_dict[(tokens[2],tokens[3],tokens[4])] = int(tokens[0])

    text.close()

    return bigram_dict, trigram_dict

bigram_dict, trigram_dict = dict_trigrams("ner_rare.counts")


def compute_trigrams(filename,outputFile):


    with open(filename) as text:
        with open(outputFile, 'w') as new_text:
            for line in text:
                tokens = line.strip().split(" ")
                if (len(tokens) > 1):
                    w_i2 = tokens[0]
                    w_i1 = tokens[1]
                    w_i =  tokens[2]

                    numerator = trigram_dict[(w_i2,w_i1,w_i)]
                    denominator = bigram_dict[(w_i2,w_i1)]
                    temp = numerator / denominator
                    new_line = w_i2 + " " + w_i1 + " " + w_i + " " + str(math.log(temp)) + "\n"
                    new_text.write(new_line)


compute_trigrams("trigrams.txt","5_1.txt")
