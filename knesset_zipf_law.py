import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np





if __name__ == "__main__":
    df = pd.read_csv(os.path.join(os.getcwd(),'our_data.csv'))#read the data 
    frequncy_dictionary = {}
    #count 
    for row in df.itertuples():
        if row[5] not in frequncy_dictionary.keys():
            frequncy_dictionary[str(row[5])]=1
        else:
            frequncy_dictionary[str(row[5])]+=1

    frequncy_list = []
    numbers_list =[]
    for i , word in enumerate(frequncy_dictionary.keys()):
        numbers_list.append(np.log(i+1))
        frequncy_list.append(np.log(frequncy_dictionary[word]))
    frequncy_list.sort(reverse= True)

    plt.plot(numbers_list,frequncy_list)
    plt.show()
