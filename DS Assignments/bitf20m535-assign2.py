#!/usr/bin/env python
# coding: utf-8

# # Data Science 
# # Assignment '#2 -  Exploratory Data Analysis
# 
# 

# In[395]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#display wide tables 
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)


# We have a list of 10,000 movies with IMDB user rating as imdb.txt. We want to perform a exploratory data analysis of this data in Python by using its Pandas library.  We will perform the cleaning, transformation and then visualization on the raw data. This will help us to understand the data for further processing.

# In[396]:


#!head imdb.txt


# ## 1. Loading data
# 
# Read the imdb.txt into dataframe named data. The data is tab delimited. The columns names are 'imdbID', 'title', 'year', 'score', 'votes', 'runtime', 'genres'

# In[397]:


# Your code here
data = pd.read_csv('imdb.txt', sep='\t', header=None, names=["imdbID", "title", "year", "score", "votes", "runtime", "genres"])

# print(data.head())
data.head()


# __Marks = 2__

# Check the data types of each column

# In[398]:


# Your code here
print(data.dtypes)


# __Marks = 1__

# ## 2. Clean the DataFrame
# 
# The data frame has several problems
# 
# 1. The runtime column is stored as a string
# 2. The genres column has several genres together. This way, it is hard to check which movies are Action movies and so on.
# 3. The movie year is also present in the title
# 
# 
# ### Fix the runtime column
# Convert the string '142 mins' to number 142.

# In[399]:


# Your code here
row1 = data['runtime'][0]
row1 = int(row1[:3])

print("String (142 mins) which is converted to int: ", row1)
print("Now it's type: ", type(row1))


# __Marks = 3__

# Perform this conversion on every element in the dataframe `data`

# In[400]:


# Your code here

# data['runtime'] = data['runtime'].replace(' mins.', '')

data['runtime'] = data['runtime'].str[:3]
data['runtime'] = data['runtime'].astype(int)

print("Now the type of runtime column is: ", data['runtime'].dtypes)


# __Marks = 2__

# In[401]:


print(data.dtypes)


# In[402]:


# print(data.head())
data.head()


# ### Split the genres

# We would like to split the genres column into many columns. Each new column will correspond to a single genre, and each cell will be True or False.
# 
# First, we would like to find the all the unique genres present in any record. Its better to sort the genres to locate easily.

# In[403]:


#determine the unique genres
unique_genre_list = list()
genre_list_of_each_movie = list()

for gen in data['genres']:
    genre_list_of_each_movie = str(gen).split("|")
    for l in genre_list_of_each_movie:
        unique_genre_list.append(l)

unique_genre_list = np.unique(unique_genre_list)
unique_genre_list = np.delete(unique_genre_list, [-1,])

print(unique_genre_list)


# __Marks = 4__

# Then make a column for each genre

# In[404]:


#make a column for each genre
for genre in unique_genre_list:
    data[genre] = data['genres'].str.contains(genre)

# print(data.head())
data.head(10)


# __Marks = 5__

# ### Eliminate year from the title
# We can fix each element by stripping off the last 7 characters

# In[405]:


#Strip off last 7 character from title
data['title'] = data['title'].apply(str)
data['title'] = data['title'].str[:-7]

# print(data)
data
# data['title'].dtypes


# __Marks = 1__

# ## 3. Descriptive Statistics
# 
# Next, we would like to discover outliers. One possible way is to describe some basic, global summaries of the DataFrame on `score`, `runtime`, `year`, `votes`.

# In[406]:


#Call `describe` on relevant columns
print("***Describe Score***")
score = data['score'].describe()
print(score)

print("\n***Describe RunTime***")
runTime = data['runtime'].describe()
print(runTime)

print("\n***Describe Year***")
year = data['year'].describe()
print(year)

print("\n***Describe Votes***")
votes = data['votes'].describe()
print(votes)


# __Marks = 1__

# Do you see any quantity unusual. Better replace with NAN.

# In[407]:


#Your code here
data = data.fillna(np.nan)

score = score.replace(0, np.nan)
runTime = runTime.replace(0, np.nan)
year = year.replace(0, np.nan)
votes = votes.replace(0, np.nan)


# __Marks = 1__

# Lets repeat describe to make sure that it is fine

# In[408]:


#Your code here
print("***Describe Score***")
print(score)

print("\n***Describe RunTime***")
print(runTime)

print("\n***Describe Year***")
print(year)

print("\n***Describe Votes***")
print(votes)


# __Marks = 1__

# ### Basic plots

# Lets draw histograms for release year, IMDB rating, runtime distribution

# In[409]:


#Your code here
fig_ax1 = data[['year']].plot.hist(color = 'k', bins=12)
fig_ax1.set_title("Frequency Distribution of Release Year")
fig_ax1.set_xlabel("Release Year")
fig_ax1.set_ylabel("Frequency")
plt.gca().set_facecolor('grey')
plt.show()


# __Marks = 1__

# In[410]:


#Your code here
fig_ax2 = data[['score']].plot.hist(color= 'r',bins=10)
fig_ax2.set_title("Frequency Distribution of IMDB Rating")
fig_ax2.set_xlabel("IMDB Rating")
fig_ax2.set_ylabel("Frequency")
plt.show()


# __Marks = 1__

# In[411]:


#Your code here
fig_ax3 = data[['runtime']].plot.hist(color='g', bins=8)
fig_ax3.set_title("Frequency Distribution of RunTime")
fig_ax3.set_xlabel("RunTime")
fig_ax3.set_ylabel("Frequency")
plt.show()


# __Marks = 1__

# Scatter plot between IMDB rating and years. Does it shows some trend?

# In[412]:


#Your code here
data.plot.scatter(x = 'year', y = 'score', c='k')
plt.title('Relation between IMDB Ratings & Release Years')
plt.xlabel('Year')
plt.ylabel('IMDB Rating')
plt.show()

print("***Analysis of the above Scatter Plot***")
print("The trend clearly shows that the movies released during 1950s-1980s were among those which got highest IMDB rating (on scale from 7 to 9), while during the years of 1990 to 2010, the movies released were giving variant ratings on scale from 2 to 9.\n")


# __Marks = 2__

# Is there any relationship between IMDB rating and number of votes? Describe

# In[413]:


#Your code here
data.plot.scatter(x = 'votes', y = 'score')
plt.title('Relationship between IMDB Ratings & No. of Votes')
plt.xlabel('Votes')
plt.ylabel('IMDB Rating')
plt.show()

corr_coff = data['score'].corr(data['votes'])
print("Correlation coefficient: " ,corr_coff)

print("\n***Analysis of the above Scatter Plot***")
print("The trend shows that, a movie which has a number of votes in the range between 0 - 200000, the IMDb rating of that movie varies on scale from 2 to 9. While the movies which have more than 200000 votes, are showing IMDb ratings between 7 to 9 on scale.\n")


# __Marks = 2__

# ### Data aggregation/Summarization

# *What genres are the most frequent?* Lay down the genres in descending order of count

# In[414]:


#Your code here
#sum sums over rows by default
freq_gen = dict()

for gen in unique_genre_list:
    freq_gen[gen] = data[gen].sum()

freq_gen = dict(sorted(freq_gen.items(), key=lambda x: x[1], reverse = True))

# print(freq_gen)
df = pd.DataFrame()

df['Movie Name'] = freq_gen.keys()
df['Frequency'] = freq_gen.values()

print(df)
print("\nThe most frequent genre is: ", next(iter(freq_gen)))


# __Marks = 2__

# Draw a bar plot to show top ten genres

# In[415]:


#Your code here
genres = df['Movie Name'].iloc[:10]
frequency = df['Frequency'].iloc[:10]
    
# print(genres)
# print(frequency)
    
plt.figure(figsize=(9, 6))
plt.bar(genres, frequency, color='g')
plt.title('Top Ten Genres')
plt.xlabel('Genres')
plt.ylabel('Frequency')
plt.show()


# __Marks = 2__

# *How many genres does a movie have, on average?*

# In[416]:


#Your code here
#axis=1 sums over columns instead

movie_avrg_genre = data.iloc[:, [1] + list(range(7, len(data.columns)))]

movie_avrg_genre['avrg genres'] = movie_avrg_genre.iloc[:, 1:].mean(axis=1)
movie_avrg_genre = movie_avrg_genre.iloc[:, [0, -1]]

print(movie_avrg_genre)


# __Marks = 2__

# ## Explore Group Properties

# Let's split up movies by decade. Find the decade mean score and draw a plot as follows:
# 
# <img src=score-year-plot.png>

# In[417]:


#Your code here
import matplotlib.colors as mcolors

# Extract the decade from the "year" column and create a new column "Decade"
data['Decade'] = data['year'].apply(lambda x: (x // 10) * 10)
# Group the dataframe by "Decade" and calculate the mean of the "Score" column
data_decade_mean = data.groupby('Decade')['score'].mean().reset_index()


# plotting the points 
x = data_decade_mean.iloc[:, 0]
y = data_decade_mean.iloc[:, 1]
# print(x)
# print(y)

plt.figure(figsize=(9, 6))
# setting grey scale color for scatter dots
gray_values = np.linspace(0, 1, len(data))
norm = mcolors.Normalize(vmin=0, vmax=1)

# plotting simple & scatter plot
plt.plot(x, y, color='red', linewidth = 4, marker='o', markerfacecolor='black', markersize=11)
plt.scatter(data['year'], data['score'], s=15, c=gray_values, cmap='gray', norm=norm)

decade_range = range(1940, 2021, 10)

plt.title("Mean scoress by Decades")
plt.xlabel('year')
plt.ylabel('score')
plt.xticks(decade_range)
plt.yticks(np.arange(1, 11))
plt.legend(["Decade Average"], frameon=False)

plt.show()


# __Marks = 5__

# Find the most popular movie each year
# 

# In[418]:


#Your code here
most_pop = data.groupby(['year'])['score'].idxmax()
most_pop = data.loc[most_pop, ['year', 'title', 'score']]

print("\nMost Popular Movies Each Year\n")
print(most_pop)


# __Marks = 2__

# ### THE END!

# %%
