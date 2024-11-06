import basic_summary,scraper

# para = ""

# with open('./test.txt',encoding="utf-8") as f:
#     para = f.read()
def gen_summary(topic):
    scraped_data = scraper.scrape(topic)
    scraped_data = ' '.join(scraped_data)
    return basic_summary.generate_summary(scraped_data)


# print(basic_summary.generate_summary(scraped_data[0]))