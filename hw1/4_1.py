# Huibo Zhao
# Feb.17th.2018


# This function replace infrequent words with symbol _RARE_
def replace_rare(filename,newFilename):
    word_count = {}
    text = open(filename,"r")
    for line in text:
        tokens = line.strip().split(" ")
        word = tokens[0]
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
                        line = line.replace(symbol,'_RARE_')
                    new_text.write(line)




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

# This function returns the emission parameters e(x|y)
def emission_probability(x,y,filename):
    count_y_dict = extract_countY(filename)
    count_y = count_y_dict[y]
    text = open(filename,"r")
    for line in text:
        tokens = line.strip().split(" ")
        if tokens[1] == "WORDTAG" and tokens[3] == x and tokens[2] == y:
            count_xy = int(tokens[0])
            break

    text.close()
    print(count_xy)
    print(count_xy/count_y)


#emission_probability("University","I-ORG","ner.counts")
replace_rare("ner_train.dat","ner_train_rare.dat")
