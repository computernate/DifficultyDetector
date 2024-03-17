import requests
from bs4 import BeautifulSoup
import re


"""
This gets all the sentences from the website howtostudykorean, given a "unit." There are 6 units, each more advanced
than the last. This may not be very representitive of the korean language as a whole, as it is very centered around
textbook learning instead of natural input. However, it is a great starting resource for labelling the data.
"""
def get_howtostudykorean_sentences(start_url):
    sentences_with_audio_links = []

    # Get the HTML content of the main page
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links containing images
    image_links = [a['href'] for a in soup.find_all('a', href=True) if 'img' in str(a)]

    # There are some links that are always present. We don't want to follow them.
    bad_links = [
        "https://www.howtostudykorean.com/",
        "https://www.howtostudykorean.com/homeschool/",
        "https://www.howtostudykorean.com/app/",
        "https://www.howtostudykorean.com/2024sale/",
        "https://www.amazon.com/s?i=stripbooks&rh=p_27%3ASeulgi+Lee",
        "https://www.howtostudykorean.com/anki/",
        "https://www.howtostudykorean.com/workbooks",
        "https://www.howtostudykorean.com/homeschool/",
        "https://www.youtube.com/playlist?list=PLpkY2PdR9aLO_V0LFnP3_cdapJBcuG3-O",
        "https://www.youtube.com/playlist?list=PLpkY2PdR9aLOKW0N5CqSDNJF7rVaQCwpX",
        "https://www.youtube.com/playlist?list=PLpkY2PdR9aLMLiZnUBQFJxvr2Bs4eMbI6",
        "https://www.howtostudykorean.com/wordsearch/",
        "https://www.italki.com/affshare?ref=af945426"
    ]

    # Follow each link and find new links containing images
    for link in image_links:
        if link in bad_links:
            continue
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        new_image_links = [a['href'] for a in soup.find_all('a', href=True) if 'img' in str(a)]

        # For each new page, find all sentences in 'a' tags with links to .mp3 files
        for new_link in new_image_links:
            if new_link in bad_links:
                continue
            response = requests.get(new_link)
            soup = BeautifulSoup(response.content, 'html.parser')
            audio_links = soup.find_all('a', href=re.compile(r'\.mp3$'))

            #Now, let's add all of the sentences on this page to our list to return.
            for audio_link in audio_links:
                contents = audio_link.contents
                if not contents:
                    continue
                contents = contents[0]
                if  " " in contents:
                    # Sometimes, the website shows that you can say something in 2 different ways, indicated by " / ".
                    # These are two separate sentences and should be treated separately.
                    if " / " in contents:
                        sentences_with_audio_links.append(contents.split(" / ")[0])
                        sentences_with_audio_links.append(contents.split(" / ")[1])
                    else:
                        sentences_with_audio_links.append(contents)
    print(f"ADDING {len(sentences_with_audio_links)} SENTENCES")
    return sentences_with_audio_links
