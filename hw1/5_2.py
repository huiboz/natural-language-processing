#!/usr/bin/env python3

# Huibo Zhao
# Feb.18th.2018

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




def prob_emission(x,y):
    if x in frequent_word:
        word = x
    else:
        word = "_RARE_"


    if (word,y) in dictionary_emission:
        return dictionary_emission[(word,y)]
    else:
        return 0

#print(prob_emission("south","I-PER"))



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

def prob_trigrams(w,u,v):
    if (w,u,v) in trigram_dict:
        numerator = trigram_dict[(w,u,v)]
    else:
        return 0

    if (w,u) in bigram_dict:
        denominator = bigram_dict[(w,u)]
    else:
        return 0

    return (float) (numerator/denominator)



tag_list = []
for key in count_y_dict:
    tag_list.append(key)

tag_list_star = ["*"]

#print(tag_list)

def viterbi(word_list):
    pi = {}
    bp = {}
    pi[(0,'*','*')] = 1
    return_prob_list = []

    for k in range(1,len(word_list)+1):
        if k == 1:
            for v in tag_list:
                pi[(1,'*',v)] = prob_trigrams("*","*",v) * prob_emission(word_list[k-1],v)
                bp[(1,'*',v)] = '*'
        elif k == 2:
            for v in tag_list:
                for u in tag_list:
                    pi[(2,u,v)] = pi[(k-1,'*',u)] * prob_trigrams("*",u,v) * prob_emission(word_list[k-1],v)
                    bp[(2,u,v)] = '*'
        else:
            for v in tag_list:
                for u in tag_list:
                    max_prob = 0
                    max_tag = tag_list[0]
                    for w in tag_list:
                        temp_prob = pi[(k-1,w,u)] * prob_trigrams(w,u,v) * prob_emission(word_list[k-1],v)
                        if temp_prob > max_prob:
                            max_prob = temp_prob
                            max_tag = w
                    pi[(k,u,v)] = max_prob
                    bp[(k,u,v)] = max_tag

    length = len(word_list)
    y_tag_list = []
    ##### get yn-1 and yn #####
    if (length > 1):
        max_prob = 0
        yn_1 = tag_list[0]
        yn   = tag_list[0]
        for u in tag_list:
            for v in tag_list:
                temp_prob = pi[(length,u,v)] * prob_trigrams(u,v,'STOP')
                if temp_prob > max_prob:
                    max_prob = temp_prob
                    yn_1 = u
                    yn = v
        y_tag_list.insert(0,yn)
        y_tag_list.insert(0,yn_1)
    else: # sentence with only one word
        max_prob = 0
        yn_1 = '*'
        yn   = tag_list[0]
        max_prob = 0
        for v in tag_list:
            temp_prob = pi[(length,'*',v)] * prob_trigrams('*',v,'STOP')
            if temp_prob > max_prob:
                max_prob = temp_prob
                yn = v
        y_tag_list.insert(0,yn)
    #############################

    ###### get each yk #######
    for k in range(length-2,0,-1):
        yk = bp[(k+2,y_tag_list[0],y_tag_list[1])]
        y_tag_list.insert(0,yk)
    #############################

    ##### get prob ############

    prob_list = []
    for i in range(1,length+1,1):
        if i == 1:
            prob_list.append(math.log(pi[(i,'*',y_tag_list[i-1])]))
        else:
            prob_list.append(math.log(pi[(i,y_tag_list[i-2],y_tag_list[i-1])]))
    ###########################
    return prob_list,y_tag_list




def output(filename,outputFile):
    output_tag = []
    output_prob = []
    count = 0
    with open(filename) as text:
        word_list = []
        for line in text:
            tokens = line.strip().split(" ")
            if tokens[0] == '': #emply line
                #print(word_list)
                prob_list, tag_list = viterbi(word_list)
                output_tag += tag_list
                output_prob += prob_list
                #break
                word_list = []
            else:
                word_list.append(tokens[0])
                count += 1
                print(count)
    print(count)
    print(len(output_tag))
    print(len(output_prob))

    with open(filename) as text:
        with open(outputFile, 'w') as new_text:
            index = 0
            for line in text:
                tokens = line.strip().split(" ")
                if tokens[0] == '': # emply line
                    new_text.write(line)
                else:
                    word = tokens[0]
                    new_line = word + " " + output_tag[index] + " " + str(output_prob[index]) + "\n"
                    new_text.write(new_line)
                    index += 1
                    print(index)


output("ner_dev.dat","5_2.txt")
