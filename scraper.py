from bs4 import BeautifulSoup
from urllib.request import urlopen
from requests import get
import re
import pandas as pd


        
            
def scrapelink(link,headers):
    try:
        link = link[link.find('q=')+2:link.find('&sa')]    #the necessary url we need has prefix of ?q= and is followed by &sa therefore following this pattern, extracting the useful URl to further scrape that page
        page=get(link,headers=headers).text   #retrieve page and only the html code
        scraped = BeautifulSoup(page,'lxml')
        return scraped
    except:
        return False

def extract_data(scraped_data):
    tags = ['p','li','blockquote'] #tags which we want to extract data from
    extracted_data = []     #stores the entire extracted data for each tag
    for tag in tags:
        if scraped_data.find(f'{tag}'):
            scraped_tags = scraped_data.find_all(f'{tag}')  
            # print(f"Printing {tag} data")
            data = ""
            for scraped_tag in scraped_tags:
                data+=scraped_tag.text
            extracted_data.append(data)
    return extracted_data


def clean_text(extracted_data):
    extracted_data = ' '.join(str(i) for i in extracted_data)
    extracted_data= extracted_data.lower()
    extracted_data = re.sub('\n',' ',extracted_data)
    extracted_data = re.sub('\r',' ',extracted_data)
    extracted_data = re.sub(' +',' ',extracted_data)
    return extracted_data




def scrape(topic):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'} #necessary for get request to work

    # topic = input("What do you want to search?\n")

    search = "https://www.google.com/search"

    topic = topic.replace(' ','+') #multiple words are concatenated by + sign in query url

    query = f"{search}?q={topic}"

    search_page = get(query,headers=headers).text

    soup = BeautifulSoup(search_page,'lxml')  #first instance of BS to get the scraped search result page

    a_tags = soup.find_all('a',limit=50)

    reslinks = []   #the list to store the top 5 search results links
    
    for tag in a_tags:
        if tag.find('h3'): #the search results are associated with h3 tags
            reslinks.append(tag['href'])
            if len(reslinks)==5:
                break
    # print(reslinks)
    
    scraped_data = [scrapelink(i,headers) for i in reslinks]
    
    
    # extracted_data = extract_data(scraped_data[0])
    extracted_data = []
    for i in scraped_data:
        if type(i) is bool:
            continue
        extracted_data.append(extract_data(i))
    # print(len(extracted_data))
    

    extracted_data = [clean_text(i) for i in extracted_data]
    
    return extracted_data
    # with open('test.txt', "w", encoding="utf-8") as f:
    #     f.write(extracted_data[0])
    
    # print(len(extracted_data[0]))

            
            
# if __name__ == '__main__':
#     main()
    

