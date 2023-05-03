import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport

data1 = pd.read_csv('data2022.csv', usecols=[
                    "Age", "LanguageHaveWorkedWith", "LearnCode"])
data1 = data1.rename(columns={'LanguageHaveWorkedWith': 'Language'})
data1 = data1.rename(columns={'LearnCode': 'Platform'})
data1.dropna(axis=0, how='any', inplace=True)
data1 = data1[~data1.isin(['Prefer not to say']).any(axis=1)]
data1 = data1.replace('years old', '', regex=True)

data1 = data1.replace('Under 18 ', '5-17', regex=True)
data1 = data1.replace('18-24 ', '18-24', regex=True)
data1 = data1.replace('25-34 ', '25-34', regex=True)
data1 = data1.replace('35-44 ', '35-44', regex=True)
data1 = data1.replace('45-54 ', '45-54', regex=True)
data1 = data1.replace('55-64 ', '55-64', regex=True)
data1 = data1.replace('65 years or older', '65-100', regex=True)

data1 = data1.replace(';', ',', regex=True)
data1 = data1.replace('(ex: videos, blogs, etc)', '', regex=True)
data1 = data1.replace('(e.g., videos, blogs, forum)', '', regex=True)
data1 = data1.replace('(i.e., University, College, etc)', '', regex=True)
data1 = data1.replace('(please specify)', '', regex=True)
data1 = data1.replace('(virtual or in-person)', '', regex=True)
data1 = data1.replace('/', ',', regex=True)
data1 = data1.replace('(ex: videos, blogs, etc)', '', regex=True)

A_group = data1[data1["Age"] == "5-17"]
B_group = data1[data1["Age"] == "18-24"]
C_group = data1[data1["Age"] == "25-34"]
D_group = data1[data1["Age"] == "35-44"]
E_group = data1[data1["Age"] == "45-54"]
F_group = data1[data1["Age"] == "55-64"]
G_group = data1[data1["Age"] == "65-100"]

profile = ProfileReport(data1)
profile.to_file(output_file="data1.html")


profile = ProfileReport(data2)
profile.to_file(output_file="data2.html")


def count_dict(Language):
    counts = {}
    for row in A_group[Language] : 
        items = row.split(",")
        for item in items :
            counts[item] = counts.get(item, 0)+1
    return counts

def sort_to_per(counts):
    counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}

    tot = sum(counts.values())
    for key, val in counts.items():
        counts[key] = val/tot * 100
    return counts

langworked_counts = count_dict("Language")

langworked_counts = sort_to_per(langworked_counts)

fig, ax = plt.subplots(figsize=(15,8))
ax = sns.barplot(x=list(langworked_counts.values()), y=list(langworked_counts.keys()), palette="muted", orient="h")
ax.bar_label(ax.containers[0])
ax.set_title("Language used by Different Age Group of Survey 2021")
ax.set_xlabel("% of Studens")
ax.set_ylabel("Language")
plt.show()
plt.savefig('groupA.png')

