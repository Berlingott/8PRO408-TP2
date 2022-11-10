# THIS CODE DOES NOT SEEM TO WORK WELL

import os
import pandas as pd
import plotly.express as px
import random
from tqdm import tqdm

file_list = list()

if __name__ == '__main__':
    for person in [person for person in os.listdir() if os.path.isdir(person)]:
        # The abandoned variable is the file count.
        try:
            for sentence in os.listdir(f"{person}/wav/"):
                file_list.append(f"{person}/wav/{sentence}")
        except FileNotFoundError:
            continue
        except NotADirectoryError:
            continue

    # Let's transform the list of location into a sorted list of (sentence, person) tuples.
    file_list.sort()
    file_list = [(location.split('/')[2], location.split('/')[0]) for location in file_list]

    files = pd.DataFrame(file_list)
    files.columns = ['Sentence', 'Person']

    selection = files.groupby('Person').count()
    selection = selection.loc[selection['Sentence'] >= 20]
    selection = selection.reset_index()
    selection = set(selection['Person'])
    selection = [(sentence, person) for (sentence, person) in file_list if person in selection]

'''
monte_carlo = dict()

for i in tqdm(range(10000)):
    roster = [sentence for sentence in files['Sentence'].unique()]
    pick = random.choice(roster)
    roster.remove(pick)
    spectrum = files[files['Sentence'] == pick]
    spectrum = set(spectrum['Person'])
    remainder = len(spectrum)
    count = 1
    while remainder != 0:
        pick = random.choice(roster)
        roster.remove(pick)
        sentences = files[files['Sentence'] == pick]
        sentences = set(sentences['Person'])
        spectrum = spectrum & sentences
        remainder = len(spectrum)
        if remainder > 0:
            count = count + 1
    if count in monte_carlo:
        monte_carlo[count] = monte_carlo[count] + 1
    else:
        monte_carlo[count] = 1

monte_carlo = pd.DataFrame(monte_carlo.items())
monte_carlo.columns = ['number of intersections', 'number of occurrences']

fig = px.scatter(monte_carlo, x='number of intersections', y='number of occurrences')
fig.show()
'''

number_of_categories = 2

best_picks = set()
sentences = set()
for i in tqdm(range(10000)):
    roster = list(set([person for (_, person) in selection]))
    picks = set()
    for j in range(number_of_categories):
        pick = random.choice(roster)
        roster.remove(pick)
        picks.add(pick)
    spectrum = set(files['Sentence'])
    for pick in picks:
        pick_range = files[files['Person'] == pick]
        pick_range = set(pick_range['Sentence'])
        spectrum = spectrum & pick_range
    if len(spectrum) > len(sentences):
        best_picks = picks
        sentences = spectrum

print(f'The {number_of_categories} persons with the greatest number of common sentences ({len(sentences)}) are:')
for pick in best_picks:
    print(pick)
print()
print(f'The relevant sentences are:')
for sentence in sentences:
    print(sentence)