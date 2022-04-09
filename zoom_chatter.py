# 1. importing libraries
import re
import pandas as pd
from datetime import datetime as dt

# 2. settings for dataframe outlook
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.3f}')
pd.set_option('display.width', 500)

# 3. regex time!
with open("kaggle/zoom_chatter_2022/zoom_chatter.txt", "tr", encoding="utf-8", newline='\n') as dosya:
    text_str = dosya.read()

regex = "name: \\\\\"([\w\s]*)\\\\\",\\\\n\"\\r\\n\\t\"time: \\\\\"([\w:]*)\\\\\",\\\\n\"\\r\\n\\t\"content: \\\\\"(.?[\s\w?.@]*)"
matches = re.findall(regex, text_str)
df = []

# 4. creating dataframe
for i in range(len(matches)):
    d = {
        'Name' : matches[i][0],   # this columns about names
        'Time' : matches[i][1],   # this columns about writing times
        'Content' : matches[i][2] # this columns about contents
    }
    df.append(d)

df = pd.DataFrame(df)

# 5. first touch to data
df.head()
df.info()
df.shape

def time_parser(time): # reorganizing the minutes and hour in datetime format
    timer=[]
    for i in time:
        if len(i)<6:
            timer.append(dt.strptime(i, '%M:%S').minute)
        else:
            timer.append(dt.strptime(i, '%X').minute + (dt.strptime(i, '%X').hour*60))
    return timer

def letter_counter(letters): # counting the letters of contents
    letter_box=[]
    for i in letters:
        letter_box.append(len(i))
    return letter_box

df['Minutes'] = time_parser(df['Time']) # parsing the time via function
df['Content_Long'] = letter_counter(df['Content']) # counting letters via function
df['Time_Period'] = pd.qcut(df['Minutes'], 3 , labels=[1,2,3]) # for 3 lessons, we cut into 3 pieces

# 6. analyzing the data

# top 10 most talkers
df.groupby('Name')['Time'].count().sort_values(ascending=False).head(10)

# top 10 longest messages and messagers
indexes = df['Content_Long'].sort_values(ascending=False).head(10).index.to_list()
df[df.index.isin(indexes)][['Name', 'Content', 'Content_Long']]\
    .sort_values(by='Content_Long', ascending=False)

# top 10 most talkers via lessons periods
df[df['Time_Period']==1].groupby('Name')['Time'].count().sort_values(ascending=False).head(10)
df[df['Time_Period']==2].groupby('Name')['Time'].count().sort_values(ascending=False).head(10)
df[df['Time_Period']==3].groupby('Name')['Time'].count().sort_values(ascending=False).head(10)

