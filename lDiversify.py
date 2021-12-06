import sys
import pandas as pd
from pandas.core.frame import DataFrame

FILE_PATH = sys.argv[1]
L = int(sys.argv[2])

df = pd.read_csv(FILE_PATH)

def getLDiversity(dataset: DataFrame):
    l_count = DataFrame(df.groupby(by = ['Age', 'Race', 'Occupation', 'Sex', 'HoursPerWeek']))

    lowestVal = None

    for index, row in l_count.iterrows():
        subset = row[1]
        uniqueVals = len(pd.unique(subset['EducationNum']))

        if(lowestVal is None):
            lowestVal = uniqueVals
        else:
            if(uniqueVals < lowestVal):
                lowestVal = uniqueVals

    return lowestVal
