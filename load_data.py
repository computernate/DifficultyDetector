import pandas as pd
import os

import korean_sentences


class SourceData:
    def __init__(self, tag, url, function, level):
        self.tag = tag
        self.url = url
        self.function = function
        self.level = level


korean_data = [
    # You may be wondering why htsk uses such inconsistent names for all their units.
    # I am wondering too.
    SourceData("htsk1", "https://www.howtostudykorean.com/unit1/", korean_sentences.get_howtostudykorean_sentences, 1),
    SourceData("htsk2", "https://www.howtostudykorean.com/unit-2-lower-intermediate-korean-grammar/", korean_sentences.get_howtostudykorean_sentences, 2),
    SourceData("htsk3", "https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/", korean_sentences.get_howtostudykorean_sentences, 3),
    SourceData("htsk4", "https://www.howtostudykorean.com/upper-intermediate-korean-grammar/", korean_sentences.get_howtostudykorean_sentences, 4),
    SourceData("htsk5", "https://www.howtostudykorean.com/unit-5/", korean_sentences.get_howtostudykorean_sentences, 5),
]

def load_korean_data():
    # Check if the CSV files exist, and if not, create them with the appropriate columns
    if not os.path.exists('korean/collected_sources.csv'):
        pd.DataFrame(columns=['tag']).to_csv('korean/collected_sources.csv', index=False)
    if not os.path.exists('korean/sentences.csv'):
        pd.DataFrame(columns=['level', 'sentence']).to_csv('korean/sentences.csv', index=False)

    # Load the existing data
    collected_sources = pd.read_csv('korean/collected_sources.csv')
    sentences = pd.read_csv('korean/sentences.csv')
    new_sources_to_save = []
    new_sentences_to_save = []

    for obj in korean_data:
        print("Tag: "+obj.tag)
        if obj.tag not in collected_sources['tag'].values:
            print("Getting data: "+obj.tag)
            new_sentences = obj.function(obj.url)
            for sentence in new_sentences:
                new_sentences_to_save.append([obj.level, sentence])
            new_sources_to_save.append(obj.tag)

    # Save the updated data
    new_sentences_df = pd.DataFrame(new_sentences_to_save, columns=["level", "sentence"])
    sentences = pd.concat([sentences, new_sentences_df], ignore_index=True)
    new_sources_df = pd.DataFrame(new_sources_to_save, columns=["tag"])
    collected_sources = pd.concat([collected_sources, new_sources_df], ignore_index=True)

    collected_sources.to_csv('korean/collected_sources.csv', index=False)
    sentences.to_csv('korean/sentences.csv', index=False)


load_korean_data()