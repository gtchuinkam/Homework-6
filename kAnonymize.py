import sys
import pandas as pd
from pandas.core.frame import DataFrame
# from pathlib import Path

# fle = Path('kCensusData.csv')
# fle.touch(exist_ok=True)

FILE_PATH = sys.argv[1]
K = int(sys.argv[2])

def getKAnonymity(dataset: DataFrame):
    ck = dataset.groupby(['Age', 'Race', 'Occupation', 'Sex', 'HoursPerWeek']).size().reset_index(name = 'Count')
    return ck['Count'].min()

def anonymizeAge(dataset : DataFrame):
    dataset['Age'] = dataset['Age'].transform(lambda x: str(x)[:-1] + "*")

def anonymizeOccupation(dataset: DataFrame):
    dataset['Occupation'] = dataset['Occupation'].transform(lambda x: x.split("-")[0])

def anonymizeHoursWorked(dataset: DataFrame):
    dataset['HoursPerWeek'] = dataset['HoursPerWeek'].transform(lambda x: str(x)[:-1] + "*")

def anonymizeSex(dataset: DataFrame):
    dataset['Sex'] = dataset["Sex"].transform(lambda x: "*")

def anonymizeRace(dataset: DataFrame):
    dataset['Race'] = dataset["Race"].transform(lambda x: "*")

def completelyAnonymizeOccupation(dataset: DataFrame):
    dataset['Occupation'] = dataset['Occupation'].transform(lambda x: "*")

def completelyAnonymizeAge(dataset: DataFrame):
    dataset['Age'] = dataset['Age'].transform(lambda x: "*")

def completelyAnonymizeHoursWorked(dataset: DataFrame):
    dataset['HoursPerWeek'] = dataset['HoursPerWeek'].transform(lambda x: "*")


def anonymizeDataset(): 

    df = pd.read_csv(FILE_PATH)

    total_rows = len(df.index)
    counter = 0

    #Partial Anonymization
    for i in [1, 2, 3]:
        if i == 1:
            anonymizeAge(df)
            counter += total_rows
            if(getKAnonymity(df) >= K):
                return
        if(i == 2):
            anonymizeHoursWorked(df)
            counter += total_rows
            if(getKAnonymity(df) >= K):
                return
        if(i == 3):
            anonymizeOccupation(df)
            counter += total_rows
            if(getKAnonymity(df) >= K):
                return

    #More indepth anonymization
    attrTracker = 0
    attr = ['Age', 'HoursPerWeek', 'Race', 'Sex', 'Occupation']

    while (getKAnonymity(df) < K):
        k_count = df.groupby(['Age', 'Race', 'Occupation', 'Sex', 'HoursPerWeek']).size().reset_index(name = 'Count')
        k_count = k_count[k_count['Count'] < K]

        for index, row in k_count.iterrows():
            localCount = row['Count']
            counter += int(localCount)

            df.loc[(df['Age'] == row['Age']) &
                    (df['Race'] == row['Race']) &
                    (df['Occupation'] == row['Occupation']) &
                    (df['Sex'] == row['Sex']) &
                    (df['HoursPerWeek'] == row['HoursPerWeek']), attr[attrTracker]]='*'
        
        attrTracker += 1
    
    df.to_csv('kCensusData.csv', index=False)
    return counter

anonymizeDataset()