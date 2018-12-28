from requests import get
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from time import sleep
from time import time
from random import randint
from warnings import warn

# Scraping tutorial from - https://www.dataquest.io/blog/web-scraping-beautifulsoup/
# nltk tutorial - https://www.geeksforgeeks.org/removing-stop-words-nltk-python/

url = 'https://www.lifehack.org/508435/50-highly-motivational-quotes-prepare-you-for-2017'
url2 = 'https://motivationping.com/quotes/'
url3 = 'https://www.briantracy.com/blog/personal-success/26-motivational-quotes-for-success/'
url4 = 'http://www.planetofsuccess.com/blog/2015/the-75-most-motivational-quotes-ever-spoken/'
url5 = 'https://www.daniel-wong.com/2015/10/05/study-motivation-quotes/'
url6 = 'https://www.entrepreneur.com/article/247213'

response = get(url)
response2 = get(url2)
response3 = get(url3)
response4 = get(url4)
response5 = get(url5)
response6 = get(url6)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)
html_soup2 = BeautifulSoup(response2.text, 'html.parser')
type(html_soup2)
html_soup3 = BeautifulSoup(response3.text, 'html.parser')
type(html_soup3)
html_soup4 = BeautifulSoup(response4.text, 'html.parser')
type(html_soup4)
html_soup5 = BeautifulSoup(response5.text, 'html.parser')
type(html_soup5)
html_soup6 = BeautifulSoup(response6.text, 'html.parser')
type(html_soup6)

allQuotes = html_soup.find('div', class_ = 'article-content')
allQuotes2 = html_soup2.find_all('p')
allQuotes3 = html_soup3.find_all('h3')
quote_containers = html_soup4.find_all('blockquote')
quotes = allQuotes.find_all('p')
quote_main5 = html_soup5.find('div', class_ ='entry-content')
quotes5 = quote_main5.find_all('p')
quote_main6 = html_soup6.find('ol')
quotes6 = quote_main6.find_all('li')

cleanedS = []
i=0
for quote in quotes:
    temp = quote.text
    for s in temp:
        if s.isalpha():
            temp = temp[i:]
            i=0
            break;
        i+=1
    cleanedS.append(temp.lower())

for quote2 in allQuotes2:
    temp = quote2.text
    if len(temp) > 0:
        if temp[0].isdigit():
            for s in temp:
                if s.isalpha():
                    temp = temp[i:]
                    i=0
                    break;
                i=+1
            cleanedS.append(temp.lower())

for quote3 in allQuotes3:
    temp = quote3.text
    newString = ''
    for s in temp:
        if s.isalpha() or s == " ":
            newString += str(s)
        continue;
    cleanedS.append(newString.lower())

for container in quote_containers:
    q = container.find('p')
    newString = q.text
    if newString.find("""\n""") > 0:
        index = newString.index("""\n""")
        newString = newString[3:index]
    cleanedS.append(newString.lower())

for quote in quotes5:
    newString = quote.text
    if len(newString) > 0:
        if newString[0].isalpha():
            continue
        if newString.find("–") > 0:
            index = newString.index("–")
            newString = newString[:index]
        cleanedS.append(newString[3:].lower())

for quote in quotes6:
    newString = quote.text
    # print(newString)
    if newString.find("—") > 0:
        index = newString.index("—")
        newString = newString[:index]
    cleanedS.append(newString.lower())

print("Quotes evaluated: " + str(len(cleanedS)))
stop_words = set(stopwords.words('english'))
newStopWords = [".",",","’","–","―","0.",":","1.","2.","3.","4.","5.",";","]","—"]
stop_words.update(newStopWords)
words = []

for string in cleanedS:
    word_tokens = word_tokenize(string)

    for w in word_tokens:
        if w not in stop_words:
            words.append(w)

# print(words)
print("Words evaluated: " + str(len(words)))

fdist = nltk.FreqDist(words)
for word, frequency in fdist.most_common(50):
    print(u'{};{}'.format(word, frequency))

# movie_containers = html_soup.find_all('p')
# print(type(movie_containers))
# print(len(movie_containers))

# first_movie = movie_containers[0]
# print(first_movie)

# first_name = first_movie.h3.a.text
# print(first_name)
# #
# # first_year = first_movie.h3.find('span', class_ = "lister-item-year text-muted unbold")
# # first_year = first_year.text
# # # print(first_year)
# #
# # first_imdb = float(first_movie.strong.text)
# # # print(first_imdb)
# #
# # first_meta = first_movie.find('span', class_ = "metascore favorable")
# # first_meta = int(first_meta.text)
# # # print(first_meta)
# #
# # first_votes = first_movie.find('span', attrs = {'name' : 'nv'})
# # first_votes = int(first_votes['data-value'])
# # # print(first_votes)
#
# # Lists to store the scraped data in
# names = []
# years = []
# imdb_ratings = []
# metascores = []
# votes = []
#
# # Extract data from individual movie container
# for container in movie_containers:
#
#     # If the movie has Metascore, then extract:
#     if container.find('div', class_ = 'ratings-metascore') is not None:
#
#         # The name
#         name = container.h3.a.text
#         names.append(name)
#
#         # The year
#         year = container.h3.find('span', class_ = 'lister-item-year').text
#         years.append(year)
#
#         # The IMDB rating
#         imdb = float(container.strong.text)
#         imdb_ratings.append(imdb)
#
#         # The Metascore
#         m_score = container.find('span', class_ = 'metascore').text
#         metascores.append(int(m_score))
#
#         # The number of votes
#         vote = container.find('span', attrs = {'name':'nv'})['data-value']
#         votes.append(int(vote))
#
# # test_df = pd.DataFrame({'movie' : names,
# #                         'year' : years,
# #                         'imdb' : imdb_ratings,
# #                         'metascore' : metascores,
# #                         'votes' : votes})
# #
# # print(test_df.info())
# # test_df
#
# pages = [str(i) for i in range(1,5)]
# years_url = [str(i) for i in range(2000, 2018)]
#
# start_time = time()
# requests = 0
#
# for _ in range(5):
#
#     requests+=1
#     sleep(randint(1,3))
#     elapsed_time = time() - start_time
#
#     print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
#
# # Redeclaring the lists to store data in
# names = []
# years = []
# imdb_ratings = []
# metascores = []
# votes = []
#
# # Preparing the monitoring of the loop
# start_time = time()
# requests = 0
#
# # For every year in the interval 2000-2017
# for year_url in years_url:
#
#     # For every page in the interval 1-4
#     for page in pages:
#
#         # Make a get request
#         response = get('http://www.imdb.com/search/title?release_date=' + year_url +
#         '&sort=num_votes,desc&page=' + page)
#
#         # Pause the loop
#         sleep(randint(8,15))
#
#         # Monitor the requests
#         requests += 1
#         elapsed_time = time() - start_time
#         print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
#
#         # Throw a warning for non-200 status codes
#         if response.status_code != 200:
#             warn('Request: {}; Status code: {}'.format(requests, response.status_code))
#
#         # Break the loop if the number of requests is greater than expected
#         if requests > 72:
#             warn('Number of requests was greater than expected.')
#             break
#
#         # Parse the content of the request with BeautifulSoup
#         page_html = BeautifulSoup(response.text, 'html.parser')
#
#         # Select all the 50 movie containers from a single page
#         mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
#
#         # For every movie of these 50
#         for container in mv_containers:
#             # If the movie has a Metascore, then:
#             if container.find('div', class_ = 'ratings-metascore') is not None:
#
#                 # Scrape the name
#                 name = container.h3.a.text
#                 names.append(name)
#
#                 # Scrape the year
#                 year = container.h3.find('span', class_ = 'lister-item-year').text
#                 years.append(year)
#
#                 # Scrape the IMDB rating
#                 imdb = float(container.strong.text)
#                 imdb_ratings.append(imdb)
#
#                 # Scrape the Metascore
#                 m_score = container.find('span', class_ = 'metascore').text
#                 metascores.append(int(m_score))
#
#                 # Scrape the number of votes
#                 vote = container.find('span', attrs = {'name':'nv'})['data-value']
#                 votes.append(int(vote))