import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_useful_text(soup):
    try:
        h2 = str(soup.find('h2').text)
        strong = str(soup.find('strong').text)
        return [h2, strong]
    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return ["Error", "Error"]
    
    

# Function to scrape data from a website using Selenium and interact with the website as a user
def scrape_data(url):
    try:
        driver = webdriver.Chrome(executable_path="C:\\Webdrivers\\chromedriver.exe")
        driver.get(url)
        
        data_list = []
        
        while True:
            # Wait for the "Next" button to be clickable , when there is no button left the scraping is finished
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "next ›"))
            )
            
            # Find all the newsletter links on the current page
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            listGroupItems = page_soup.find_all('a', {'class': 'list-group-item'})
            
            for a in listGroupItems:
                title = a.text
                newsletter_url = 'https://www.eba.europa.eu' + a['href']
                
                
                newsletter_page = BeautifulSoup(requests.get(newsletter_url).content, 'lxml')
                details = get_useful_text(newsletter_page)
                
                data_list.append([title] + details)
            
            
            next_button.click()
        
        return data_list
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")
        return []
    finally:
        # Close the Selenium driver
        driver.quit()

# Function to export data to Excel and CSV
def export_data(data, filename, output_path):
    try:
        df = pd.DataFrame(data, columns=['Title', 'H2', 'Strong']) #We're extracting only the title of each news letter, its link and the first paragraph written in Strong
        excel_file = f"{output_path}/{filename}"
        df.to_excel(excel_file, index=False)
        df.to_csv(excel_file.replace("xlsx", "csv"), index=False)
        print(f"Excel file saved to {output_path}/{filename}")
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")

if __name__ == '__main':
    news_url = 'https://www.eba.europa.eu/all-news-and-press-releases'
    data_list = scrape_data(news_url)

    output_path = "C:\\Users\\Omote\\Desktop\\Scrapping"
    excel_filename = "Scrapping_data.xlsx"
    
    excel_file = f"{output_path}/{excel_filename}"
    print(f"Full Excel file path: {excel_file}")

    export_data(data_list, excel_filename, output_path)
    
    print("Done")
