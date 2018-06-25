import re
import random
import math
import sys
from collections import defaultdict, Counter



def perplexity(probability,unique_count):
    result=0
    for i in range(len(probability)):
        if probability[i]!=0:
            probability[i] = math.log(probability[i], 2)
            result=result+probability[i]

    result=-result/unique_count
    result=result*math.pow(2,-result)

    return result

def calculate_probability_unigram_unsmoothed(sentence_array,dict_unigram,unique_count,file):
    file.write("Generate Unigram Unsmoothed:"+'\n')
    for i in range(len(sentence_array)):
        probability=1
        temp = sentence_array[i].split(" ")
        for k in range(len(temp)):
            if temp[k] in dict_unigram:
                value=dict_unigram[temp[k]]
                probability=probability*value/unique_count
        probability=math.log10(probability)

        file.write(str(sentence_array[i].encode("utf-8")) + 'Probability is:')
        file.write(str(probability))
        file.write('\n')


def calculate_probability_unigram_smoothed(sentence_array,dict_unigram,unique_count,file):
    file.write("Generate Unigram Smoothed:"+'\n')
    for i in range(len(sentence_array)):
        probability=1
        temp = sentence_array[i].split(" ")
        for k in range(len(temp)):
            if temp[k] in dict_unigram:
                value=dict_unigram[temp[k]]
                probability=probability*(value+1)/unique_count
        probability=math.log10(probability)

        file.write(str(sentence_array[i].encode("utf-8"))+'Probability is:')
        file.write(str(probability)+'\n')




def generate_email_unigram(dict_unigram):
    sentence_array=[]

    x = list(dict_unigram.items())
    for k in range(10):
        sentence = ""
        for j in range(30):
            i = 0
            count = 0
            flag = "True"
            number = random.randint(0, len(x)-1)
            while(flag!="False"):
                if number<count:
                    sentence+=" "+x[i][0]
                    flag="False"
                elif x[i][1]==" </s>" or x[i][1]=="." or x[i][1]=="!" or x[i][1]=="?" or x[i][1]=="..." :
                    sentence += " " + x[i][0]
                    flag="False"
                else:
                    count = count+x[i][1]

                i=i+1
        sentence_array.append(sentence)

    return sentence_array


def generate_email_trigram(dict_trigram,trigram_count):

    sentence_array=[]
    pro_array = []
    pro2_array = []
    x = list(dict_trigram.items())
    for k in range(10):
        temp_array = []
        previous = "<s>"
        hold = "<s>"
        for a in range(len(x)):
            if previous==x[a][0][0] and hold==x[a][0][1]:
                for t in range(x[a][1]):
                    temp_array.append(x[a][0][2])
        sentence = ""
        flag = "True"
        j=0
        probability = len(temp_array)/trigram_count
        smoothed_probability = len(temp_array)+1 / trigram_count

        while(flag!="False"):
            if len(temp_array)>0:
                number = random.randint(0, len(temp_array)-1)
                if (j>30 or temp_array[number]==" </s>" or temp_array[number]=="." or temp_array[number]=="!" or temp_array[number]=="?" or temp_array[number]=="..." ):
                    sentence += " " + temp_array[number]
                    flag="False"



                else:
                    sentence+=" " + temp_array[number]
                    hold = temp_array[number]
                    c=Counter(temp_array)
                    probability=probability*c[hold]/len(temp_array)
                    smoothed_probability = smoothed_probability * (c[hold]+1) / len(temp_array)
                    temp_array=[]
                    for a in range(len(x)):
                        if hold==x[a][0][1] and previous==x[a][0][0]:
                            for t in range(x[a][1]):
                                temp_array.append(x[a][0][2])
                    previous=hold

                j=j+1
            else:
                flag="False"

        probability=math.log10(probability)
        smoothed_probability=math.log10(smoothed_probability)
        sentence_array.append(sentence)
        pro_array.append(probability)
        pro2_array.append(smoothed_probability)

    return sentence_array,pro_array,pro2_array



def generate_email_bigram(dict_bigram,bigram_count):

    sentence_array=[]
    pro_array = []
    pro2_array = []
    x = list(dict_bigram.items())

    for k in range(10):
        temp_array = []
        for a in range(len(x)):
            if "<s>" in x[a][0]:
                for t in range(x[a][1]):
                    temp_array.append(x[a][0][1])
        sentence = ""
        flag = "True"
        j=0
        probability = len(temp_array)/bigram_count
        smoothed_probability = len(temp_array)+1 / bigram_count
        while(flag!="False"):
            if len(temp_array)>0:
                number = random.randint(0, len(temp_array)-1)
                if (j>30 or temp_array[number]==" </s>" or temp_array[number]=="." or temp_array[number]=="!" or temp_array[number]=="?" or temp_array[number]=="..." ):
                    sentence += " " + temp_array[number]
                    flag="False"



                else:
                    sentence+=" " + temp_array[number]
                    hold = temp_array[number]
                    c=Counter(temp_array)
                    probability=probability*c[hold]/len(temp_array)
                    smoothed_probability = smoothed_probability * (c[hold]+1) / len(temp_array)
                    temp_array=[]
                    for a in range(len(x)):
                        if hold in x[a][0][0]:
                            for t in range(x[a][1]):
                                temp_array.append(x[a][0][1])


                j=j+1
            else:
                flag="False"


        probability=math.log10(probability)
        smoothed_probability=math.log10(smoothed_probability)
        sentence_array.append(sentence)
        pro_array.append(probability)
        pro2_array.append(smoothed_probability)


    return sentence_array,pro_array,pro2_array



def smoothed_trigram(dict_trigram,sentence,unique_count):
    sentence = "<s> <s> " + sentence + " </s>"
    row = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', sentence)
    probability=1
    for char in row:
        temp = char.split(" ")
        for i in range(len(temp) - 2):
            trigrams = (temp[i], temp[i + 1], temp[i + 2])
            flag = trigrams in dict_trigram
            if flag == False:
                probability=(probability*1)/unique_count

            else:
                value = dict_trigram[trigrams]
                probability=probability*(value+1)/unique_count


    return probability


def smoothed_bigram(dict_bigram,sentence,unique_count):
    sentence = "<s> <s> " + sentence + " </s>"
    row = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', sentence)
    probability=1
    for char in row:
        temp = char.split(" ")
        for i in range(len(temp) - 1):
            trigrams = (temp[i], temp[i + 1])
            flag = trigrams in dict_bigram
            if flag == False:
                probability=(probability*1)/unique_count

            else:
                value = dict_bigram[trigrams]
                probability=probability*(value+1)/unique_count


    return probability





def bigram(sentence,d,bigram_count,unique_count_bigram):
    sentence ="<s> "+ sentence + " </s>"

    row = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', sentence)
    for char in row:
        temp = char.split(" ")
        for i in range(len(temp)-1):
            bigrams = (temp[i], temp[i + 1])
            flag = bigrams in d
            if flag == False:
                d[bigrams] = 1
                unique_count_bigram=unique_count_bigram+1

            else:
                value = d[bigrams]
                value = value + 1
                d[bigrams] = value

            bigram_count=bigram_count+1


    return unique_count_bigram,bigram_count,d


def unigram(sentence,d,unigram_count,unique_count):
    sentence=sentence+" </s>"
    row = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', sentence)
    for char in row:
        temp = char.split(" ")
        for i in range(len(temp)):
            flag=temp[i] in d
            if flag==False:
                d[temp[i]]=1
                unique_count=unique_count+1


            else:
                value=d[temp[i]]
                value=value+1
                d[temp[i]]=value

            unigram_count=unigram_count+1


    return unique_count,unigram_count,d



def trigram(sentence,d,trigram_count,unique_count):
    sentence = "<s> <s> " + sentence + " </s>"
    row = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', sentence)
    for char in row:
        temp = char.split(" ")
        for i in range(len(temp)-2):
                trigrams = (temp[i], temp[i + 1],temp[i+2])
                flag = trigrams in d
                if flag == False:
                    d[trigrams] = 1
                    unique_count=unique_count+1
                else:
                    value = d[trigrams]
                    value = value + 1
                    d[trigrams] = value

                trigram_count=trigram_count+1

    return unique_count,trigram_count,d



def main():
    dict_bigram = defaultdict(list)
    dict_unigram = defaultdict(list)
    dict_trigram=defaultdict(list)
    array=[]
    bigram_count=0
    unigram_count=0
    trigram_count=0
    unique_count=0
    unique_count_unigram=0
    unique_count_bigram = 0
    sentence_probability2=[]
    sentence_probability3 = []

    with open(sys.argv[1],encoding='latin-1') as f:
        for line in f:
            line=line[0:len(line)-1]
            array.append(line)
    train_size=int(len(array)*60/100)
    train_data=array[0:train_size]
    test_data=array[train_size:]

    for i in range(len(train_data)):
        unique_count,trigram_count,dict_trigram=trigram(train_data[i],dict_trigram,trigram_count,unique_count)
    for i in range(len(train_data)):
        unique_count_bigram,bigram_count,dict_bigram = bigram(train_data[i], dict_bigram,bigram_count,unique_count_bigram)
    for i in range(len(train_data)):
        unique_count_unigram,unigram_count,dict_unigram = unigram(train_data[i], dict_unigram,unigram_count,unique_count_unigram)

    file = open(sys.argv[2], "w")
    file.write("Part2:"'\n')
    for i in range(len(test_data)):
        sentence_probability=smoothed_trigram(dict_trigram,test_data[i],unique_count)
        file.write(str(test_data[i].encode("utf-8")))
        file.write(str(sentence_probability)+'\n')
        sentence_probability3.append(sentence_probability)

    for i in range(len(test_data)):
        sentnce=smoothed_bigram(dict_bigram,test_data[i],unigram_count)
        sentence_probability2.append(sentnce)
    file.write('\n')
    file.write('\n')


    file.write("Part 3:"'\n')
    sentence_array=generate_email_unigram(dict_unigram)
    calculate_probability_unigram_unsmoothed(sentence_array,dict_unigram,unique_count_unigram,file)
    file.write('\n')
    sentence_array = generate_email_unigram(dict_unigram)
    calculate_probability_unigram_smoothed(sentence_array, dict_unigram, unique_count_unigram,file)

    file.write('\n')
    file.write("Generate Bigram Smoothed:"'\n')
    sentence_array,prob_unsmoot,prob_smoot=generate_email_bigram(dict_bigram,bigram_count)
    for i in range(len(sentence_array)):
        file.write(str(sentence_array[i].encode("utf-8")) + 'Probability is:')
        file.write(str(prob_smoot[i])+'\n')

    file.write('\n')
    file.write("Generate Bigram Unsmoothed:"'\n')
    sentence_array, prob_unsmoot, prob_smoot =generate_email_bigram(dict_bigram,bigram_count)
    for i in range(len(sentence_array)):
        file.write(str(sentence_array[i].encode("utf-8")) + 'Probability is:')
        file.write(str(prob_unsmoot[i])+'\n')

    file.write('\n')
    file.write("Generate Trigram Smoothed:"+'\n')
    sentence_array, prob_unsmoot, prob_smoot =generate_email_trigram(dict_trigram,trigram_count)
    for i in range(len(sentence_array)):
        file.write(str(sentence_array[i].encode("utf-8")) + 'Probability is:')
        file.write(str(prob_smoot[i])+'\n')

    file.write('\n')
    file.write("Generate Trigram Unsmoothed:"+'\n')
    sentence_array, prob_unsmoot, prob_smoot = generate_email_trigram(dict_trigram,trigram_count)
    for i in range(len(sentence_array)):
        file.write(str(sentence_array[i].encode("utf-8")) + 'Probability is:')
        file.write(str(prob_unsmoot[i])+'\n')

    file.write('\n')
    file.write("Part 4:")
    result=perplexity(sentence_probability3,unique_count_unigram)
    result2=perplexity(sentence_probability2,unique_count_bigram)
    file.write("Bigram Perplexity:")
    file.write(str(result))
    file.write('\n')
    file.write("Trigram Perplexity:")
    file.write(str(result2))



main()

