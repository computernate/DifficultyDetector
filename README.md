# Difficulty Detector
A model that is able to detect how difficult for a learner a certain language learning resource would be to understand
# Project Setup
This project is broken up into 4 parts: create_model.py, load_data.py, {language}_sentences.py, and the csvs.

{language}_sentences.py is a holder for all the different methods for getting a resource in a language.
Each website is scraped in a slightly different way, and needs to be regarded differently. Notes about each 
resource can also be found in here

load_data.py relies heavily on {language}_sentences.py. Given each function, it pulls the sentences from the websites
and puts them in the csvs. It also updates collected_sources.csv so if more resources are added in the future, it
doesn't re-load all of them when running again.

create_model.py takes the resources in the csvs, and turns them into a model able to predict which difficulty
a given sentence would go in.

# Language Specific Details
### Korean
Korean is generally broken down into 6 levels: 3 for TOPIK1 and 3 for TOPIK2. New sources should fall into these
categories.

# TODO
* I think load_data could be a function that just takes an array of SourceData and a language name as a parameter
so it doesn't have to be rewritten with each new language
* I want to put korean_sentences inside the korean folder, but I also want the .gitignore to be set up to not push
the CSVs. 
* MORE KOREAN RESOURCES!!!!
* Save the model to be used later
* A basic flask API where you can submit a sentence and get the level
* An API endpoint where given a set of sentences or a whole document, it returns the average sentence difficulty