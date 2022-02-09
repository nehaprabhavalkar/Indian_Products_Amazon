import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import warnings
from utils import get_company_list, save_to_csv
warnings.filterwarnings('ignore')


DATA_PATH = '../data/'

FILE_NAME = 'reviews.csv'

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' } 


def get_product_asin(headers, company_list):
    for comp in company_list:
        request = requests.get('https://www.amazon.in/s?k='+ comp, headers=headers)
        soup = BeautifulSoup(request.content)
        
        asin = []
        asins = soup.findAll('div', attrs={'class':['sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20']})                                             
        
        for number in asins:
            asin.append(number['data-asin'])
        
        asin = asin[1:11]

        return asin
        

def get_product_links(headers, company_list, asin):
    link=[]

    for comp in company_list:    
        for number in range(0,len(asin)):
            url='https://www.amazon.in/dp/'+asin[number]

            page=requests.get(url,headers=headers)
            soup=BeautifulSoup(page.content)
            
            hrefs = soup.findAll('a',{'class':['a-link-emphasis a-text-bold']})

            for href in hrefs:
                link.append(href['href'])
    
    link = link[1:11]

    return link


def get_product_details(headers, company_list, asin, link):

    pasin = []
    reviews=[]
    dates = []
    stars = []
    name = []
    
    for comp in company_list:
        for idx in range(0,len(link)):
    
            for pg_no in range(0,2):
            
                url='https://www.amazon.in' + link[idx] + '&pageNumber=' + str(pg_no)
                review_page=requests.get(url, headers=headers)
            
                soup=BeautifulSoup(review_page.content)

                review_body = soup.findAll('span',{'data-hook':'review-body'})

                for body in review_body:
                    reviews.append(body.text.strip() if body else "")
                
                review_stars = soup.findAll('i',{'data-hook':'review-star-rating'})

                for star in review_stars:
                    stars.append(star.text.split(' ')[0].split('.')[0] if star else 0)

                review_dates = soup.findAll('span',{'data-hook':'review-date'})

                for date in review_dates:
                    dates.append(date.text)
                    name.append(link[idx].split('/')[1])
                    pasin.append(asin[idx])

    return pasin, name, dates, stars, reviews


def create_dataframe(pasin, name, dates, stars, reviews):
    reviews_dict = {'asin':pasin,'name':name,'date':dates,'rating':stars,'review':reviews}

    reviews_df=pd.DataFrame(data=reviews_dict, columns=['asin','name','date','rating','review']) 

    return reviews_df 


if __name__ == '__main__':

    company_list = get_company_list() 

    asin = get_product_asin(headers, company_list)

    link = get_product_links(headers, company_list, asin)

    pasin, name, dates, stars, reviews = get_product_details(headers, company_list, asin, link)

    reviews_df = create_dataframe(pasin, name, dates, stars, reviews)

    save_to_csv(reviews_df, DATA_PATH, FILE_NAME)