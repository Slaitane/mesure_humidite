import pandas as pd 
import json 
import numpy as np 
import matplotlib.pyplot as plt

def clean_data(data):
    """ Cette fonction remplacera toutes les valeurs saturées 200 par la valeur np.nan """
    for i in range(len(data)):
        if data[i] == 200:
            data[i]=np.nan
    return data

def save_plot_to_file(dataframe,title, labels,
                      start_date, end_date,filename):
    """Générer les graphs demandés avec un appel par fichier à la fonction."""
    j = 0   
    plt.rcParams['figure.dpi'] = 100 
    
    fig, axs = plt.subplots(3,sharex=True,sharey=True,figsize=(10,10))
    fig.autofmt_xdate()
    plt.yticks([7.5, 22.5, 45, 80, 150]) 
    axs[0].set_yticklabels(['saturated','too wet','perfect','plan to water','dry']) 
    fig.suptitle(title)
    index  = humidity_dataframe[start_date:end_date].index
    ones = np.ones(len(index))
    for i in labels :
            values = humidity_dataframe[start_date:end_date][i].values                  
            axs[j].plot(index, values,label=i)
            axs[j].legend(loc='upper left')                                             
            axs[j].fill_between(index,15*ones,0*ones,  facecolor='red',alpha = 0.2)     
            axs[j].fill_between(index,30*ones,15*ones, facecolor='orange',alpha = 0.2)   
            axs[j].fill_between(index,60*ones,30*ones,  facecolor='green',alpha = 0.2)
            axs[j].fill_between(index,100*ones,60*ones,  facecolor='yellow',alpha = 0.2)
            axs[j].fill_between(index,200*ones,100*ones,  facecolor='red',alpha = 0.2)
            j=j+1
    plt.margins(0) 
    plt.ylim(0, 200)
    plt.savefig(filename) 
        
if __name__ == '__main__':
    
    A = open("eco-sensors_irrigation_2020-06-01_2020-08-31.json","r")
    
    json_data = json.load(A)
    
    A_1 = json_data[0]
    A_2 = json_data[1]
    A_3 = json_data[2]
    data_1 = A_1['datasets']['data']
    data_2 = A_2['datasets']['data']
    data_3 = A_3['datasets']['data']   
    label_1 = A_1['datasets']['label']
    label_2 = A_2['datasets']['label']
    label_3 = A_3['datasets']['label']
    time_index = A_1['labels']
    

    humidity_dataframe = pd.DataFrame(
        data = {
            label_1: data_1,
            label_2: data_2,
            label_3: data_3,
        },
        index = time_index,
        dtype = 'float'
    )
    humidity_dataframe.index = pd.to_datetime(humidity_dataframe.index)
    
    humidity_dataframe[label_1]= clean_data(data_1)
    humidity_dataframe[label_2]= clean_data(data_2)
    humidity_dataframe[label_3]= clean_data(data_3)
    
    save_plot_to_file(humidity_dataframe,"Irrigation June 2020", [label_1,label_2,label_3],'2020-06-2', '2020-06-30',"irrigation_graph_2020-06.png")
    save_plot_to_file(humidity_dataframe,"Irrigation July 2020", [label_1,label_2,label_3],'2020-07-1', '2020-07-30',"irrigation_graph_2020-07.png") 
    save_plot_to_file(humidity_dataframe,"Irrigation August 2020", [label_1,label_2,label_3],'2020-08-1', '2020-08-30',"irrigation_graph_2020-08.png") 
