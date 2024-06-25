import requests
from bs4 import BeautifulSoup
import csv

''' This function access page with list of 5-letters words.
    Parses the words and creates a list
    Saves a list into a file
'''


def main():
    words_list = scrape_five_letter_words()
    print(words_list[0])

    with open("wordle_list.txt", "w") as f:
        for word in words_list:
            word = word.upper()
            f.write(f"{word}\n")


def scrape_five_letter_words():
    url = 'https://www.wordunscrambler.net/word-list/wordle-word-list'  # Page with 5-letters words
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser') #parse the page content
    words = soup.find_all('li', {'class':'invert light'}) #getting all the 5-letters words
    words_list = [] #create list to store the words

    #going through the list of founbd items and clearing it from tags and symbols
    for item in words:
        href_value = item.find('a').get('href')
        word = item.get_text()
        word = word.translate({ord('\n'): None})
        words_list.append(word)

    return words_list




if __name__ == "__main__":
    main()
