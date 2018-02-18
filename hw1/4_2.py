import math

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

# This function returns the emission parameters e(x|y)
def emission_probability(filename):
    dict_prob = {}
    dict_tag = {}

    text = open(filename,"r")
    for line in text:
        tokens = line.strip().split(" ")
        if tokens[1] == "WORDTAG":
            label = tokens[2]
            count = int(tokens[0])
            word = tokens[3]

            if word not in dict_prob:
                dict_prob[word] = count / count_y_dict[label]
                dict_tag[word] = label
            else:
                temp_prob = dict_prob[word]
                this_prob = count / count_y_dict[label]
                if this_prob > temp_prob:
                    dict_prob[word] = this_prob
                    dict_tag[word] = label

    text.close()
    return dict_prob, dict_tag



dict_prob, dict_tag = emission_probability("ner_rare.counts")

def entity_tagger(filename,outputFile):

    taggers = ['_RARE_','O','I-PER','I-LOC','I-MISC','I-ORG','B-MISC','B-ORG','B-LOC']
    rare_prob = math.log(1/count_y_dict['_RARE_'])
    with open(filename) as text:
        with open(outputFile, 'w') as new_text:
            for line in text:
                tokens = line.strip().split(" ")
                if tokens[0] == '': # emply line
                    new_text.write(line)
                else:
                    word = tokens[0]
                    if word in dict_prob:
                        new_line = word + " " + dict_tag[word] + " " + str(math.log(dict_prob[word])) + "\n"
                    else:
                        new_line = word + " " + "_RARE_" + " " + str(rare_prob) + "\n"

                    new_text.write(new_line)

entity_tagger("ner_dev.dat","4_2.txt")
