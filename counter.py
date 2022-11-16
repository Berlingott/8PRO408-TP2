import os
import pandas as pd
import plotly.express as px
import random
from tqdm import tqdm

wav_files = list()
selection = list()
extended_selection = list()

if __name__ == '__main__':
    # This loop creates a list of all the WAV files in the corpus.
    for folder in os.listdir():
        try:
            for file in os.listdir(f"{folder}/wav/"):
                wav_files.append(file)
        except FileNotFoundError:
            continue
        except NotADirectoryError:
            continue

    count = pd.DataFrame(wav_files)

    count.columns = ['Sentence']
    count['Count'] = 1

    # This loop extracts the 20 most common sentences and keeps the location of each recording
    for file_to_search in [file_to_search for file_to_search, _ in count.groupby('Sentence', sort=True).count().head(20).iterrows()]:
        # The abandoned variable is the file count.

        for folder in os.listdir():
            try:
                for file in os.listdir(f"{folder}/wav/"):
                    if file == file_to_search:
                        selection.append(f"{folder}/wav/{file}")
            except FileNotFoundError:
                continue
            except NotADirectoryError:
                continue

    # Let's transform the list of location into a sorted list of (person, sentence) tuples.
    selection.sort()
    selection = [tuple((location.split('/')[0], location.split('/')[2])) for location in selection]
    
    # This loop adds the recordings that are not in the 20 most common but that were made by the same persons.
    folders = [folder for folder, _ in selection]
    for folder in folders:
        try:
            for file in os.listdir(f"{folder}/wav/"):
                extended_selection.append(tuple((folder, file)))
        except FileNotFoundError:
            continue
        except NotADirectoryError:
            continue

    extended_selection = pd.DataFrame(extended_selection)
    extended_selection.columns = ['Person', 'Sentence']

monte_carlo = dict()

# The following loop is a Monte-Carlo algorithm. Its goal is to use a high number of random selections
# to generate possibilities. If a possibility is considered valid, it is recorded along with its path.
# At the end of the process, the array of valid possiblities are compared in order to select the optimal path.
# The high number of iterations make this selection more evident because of the output frequencies.

# In our case, the Monte-Carlo algorithms uses 10K iterations to select persons at random and make
# an intersection of their sentences. Those intersections are made until there is no longer any sentence
# in common, and this number of intersections is recorded in a dictionary. This dictionary is then
# transformed into a graph where we will see where the optimal number of sentences (or categories) is to be found.
# It should be in the 'middle' of the curve, with a slope that is neither to steep (not enough categories)
# not too flat (not enough persons).
for i in tqdm(range(10000)):
    roster = [person for person in extended_selection['Person'].unique()]
    pick = random.choice(roster)
    roster.remove(pick)
    spectrum = extended_selection[extended_selection['Person'] == pick]
    spectrum = set(spectrum['Sentence'])
    remainder = len(spectrum)
    count = 1
    while remainder != 0:
        pick = random.choice(roster)
        roster.remove(pick)
        sentences = extended_selection[extended_selection['Person'] == pick]
        sentences = set(sentences['Sentence'])
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
# pip install kaleido==0.1.0.post1
fig.write_image("counter.png")

# From this Monte-Carlo graph we can see the optimal number of sentences that does not dramatically 
# reduce the number of persons that recorded them in common. In our case, the middle of the
# curve seems to be around four (4) sentences, or categories. This number should in theory yield
# the greatest total of CSV files converted from WAV recordings. However since this study aims to
# recognize the speaker, a higher number of recordings per person is preferrable. That is why we chose
# to augment this number to six (6) sentences, even though that reduces the speakers to sixteen (16).
number_of_sentences = 6

# The next Monte-Carlo algorithm will try to find the combination of four (6) sentences
# that is common to the greatest number of persons. It will do the opposite of the previous algorithm:
# instead of picking persons at random and intersecting their sentences, it will pick sentences at random
# and intersect their persons, until zero (0) is reached. The largest set of persons will be he output.
best_picks = set()
persons = set()
for i in tqdm(range(10000)):
    roster = [sentence for sentence in extended_selection['Sentence'].unique()]
    picks = set()
    for j in range(number_of_sentences):
        pick = random.choice(roster)
        roster.remove(pick)
        picks.add(pick)
    spectrum = set(extended_selection['Person'])
    for pick in picks:
        pick_range = extended_selection[extended_selection['Sentence'] == pick]
        pick_range = set(pick_range['Person'])
        spectrum = spectrum & pick_range
    if len(spectrum) > len(persons):
        best_picks = picks
        persons = spectrum

print(f'The {number_of_sentences} sentences with the greatest number of common persons ({len(persons)}) are:')
for pick in best_picks:
    print(pick)
print()
print(f'The relevant persons are:')
for person in persons:
    print(person)