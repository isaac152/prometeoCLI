#External libraries import
from typing import List
import matplotlib.pyplot as plt
import numpy as np

#Local imports
from config import IMAGE_FOLDER

def pie_chart(info:List[List[str]])->None:
    """ Create a pie chart of the amount of debit and credits movements"""
    #Formating the data into a simple dict
    credit,debit = 0,0
    for row in info[1:]:
        credit = credit if not(row[3].split()) else credit+1
        debit = debit if not(row[2].split()) else debit+1
    data={'Credit counts':credit,'Debit counts':debit}

    #Creating the chart and its details
    fg1,ax1= plt.subplots()
    ax1.pie(
        data.values(),
        explode=(0,0.1),
        labels=data.keys(),
        shadow=True,
        startangle=90,
        autopct='%1.1f%%',
        colors=['#deb4e0','#cc7c80']
        )
    ax1.set_title('(%) Debit and credit movements ',fontsize=20)
    ax1.axis('equal')

    #Saving the chart
    plt.savefig(f'{IMAGE_FOLDER}/pie_chart.png')
    plt.close(fg1)

def total_balance_bar_chart(info:List[List[str]])->None:
    """ Create a bar chart of the relation between the balance and the days"""
    #Formating the data to get the balances per day
    #Balances would be equal to credit-debit
    data = {}
    for row in info[1:]:
        debit= 0 if not (row[2].strip()) else float(row[2])
        credit= 0 if not (row[3].strip()) else float(row[3])
        result = data.get(row[0],0)
        data[row[0]]= round(result +(credit-debit),2)
    
    #Creating the chart and its details
    width = 0.5 
    x=np.arange(len(data.keys()))
    fig, ax = plt.subplots(figsize=(10,7))
    rects1 = ax.bar(x, data.values(), width,color=['r' if i<0 else 'b' for i in data.values()])
    ax.set_ylabel('Balances',fontsize=14,labelpad=5)
    ax.set_xlabel('Dates',fontsize=14,labelpad=5)
    ax.set_title('Total balance ',fontsize=20)
    ax.set_xticks(x, data.keys())
    ax.bar_label(rects1)
    ax.set_axisbelow(True)
    plt.axhline(0)

    #Saving the chart
    ax.grid(color='gray', linestyle='dashed',axis='y')
    plt.savefig(f'{IMAGE_FOLDER}/total_balance.png')
    plt.close(fig)

def credit_debit_bar_chart(info:List[List[str]])->None:
    """Create a dual (or comparative) bar chart of the credit/debit amounts per day"""
    #Formating the data
    data= {}
    for row in info[1:]:
        result = data.get(row[0],[0,0])
        debit = round(result[0] +(0 if not (row[2].strip()) else float(row[2])),2)
        credit = round(result[1] +(0 if not (row[3].strip()) else float(row[3])),2)
        data[row[0]]=[debit,credit]
    
    debit = [d[0] for d in data.values()]
    credit = [d[1] for d in data.values()]

    #Creating the chart and its details
    width = 0.35 
    x=np.arange(len(data.keys()))
    fig, ax = plt.subplots(figsize=(10,7))
    rects1 = ax.bar(x - width/2, credit, width,label="Credit")
    rects2 = ax.bar(x+width/2, debit, width,label="Debit")
    ax.set_ylabel('Amount',fontsize=14,labelpad=5)
    ax.set_xlabel('Dates',fontsize=14,labelpad=5)
    ax.set_title('Amounts per dates ',fontsize=20)
    ax.set_xticks(x, data.keys())
    ax.legend()
    ax.bar_label(rects1)
    ax.bar_label(rects2)
    ax.set_axisbelow(True)
    plt.axhline(0)

    #Saving the chart
    ax.grid(color='gray', linestyle='dashed',axis='y')
    plt.savefig(f'{IMAGE_FOLDER}/credit_bar.png')
    plt.close(fig)


def wrapper_graphs(movements_info:List[List[str]])->None:
    """Call all the graphs functions availables"""
    pie_chart(movements_info)
    total_balance_bar_chart(movements_info)
    credit_debit_bar_chart(movements_info)
