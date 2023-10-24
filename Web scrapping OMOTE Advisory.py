import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_useful_text(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'lxml')
    h2 = str(soup.find('h2').text)
    strong = str(soup.find('strong').text)
    return [h2, strong]

def scrape_data(url):
    html_news = requests.get(url)
    soup = BeautifulSoup(html_news.content, 'lxml')
    listGroupItems = soup.find_all('a', {'class': 'list-group-item'})
    news_list = []

    for a in listGroupItems:
        title = a.text
        url = 'https://www.eba.europa.eu' + a['href']
        news_list.append([title, url])

    return news_list

def export_data(data, filename, output_path):
    df = pd.DataFrame(data, columns=['Title', 'URL'])
    excel_file = f"{output_path}/{filename}"
    df.to_excel(excel_file, index=False)
    df.to_csv(excel_file.replace("xlsx", "csv"), index=False)

if __name__ == '__main':
    news_url = 'https://www.eba.europa.eu/all-news-and-press-releases'
    news_list = scrape_data(news_url)
    data_list = []

    for title, url in news_list:
        details = get_useful_text(url)
        data_list.append([title] + details)

    output_path = 'C:/Users/Omote/Desktop/Scrapping'  
    excel_filename = "Scrapping_data.xlsx"

    try:
        export_data(data_list, excel_filename, output_path)
        print(f"Excel file saved to {output_path}/{excel_filename}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    print("Done")
