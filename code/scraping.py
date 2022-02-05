import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import datetime
import warnings
from utils import get_company_list
warnings.filterwarnings('ignore')


DATA_PATH = '../data/'

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' } 


def get_product_asin(headers, company_list):
    for comp in company_list:
        request = requests.get('https://www.amazon.in/s?k='+ comp, headers=headers)
        soup = BeautifulSoup(request.content)
        
        asin = []
                                                    
        for i in soup.findAll('div', attrs={'class':['sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20']}):
            asin.append(i['data-asin'])
        
        asin = asin[1:21]

        return asin
        

def get_product_links(headers, company_list, asin):
    link=[]
    for comp in company_list:    
        for i in range(0,len(asin)):
            url='https://www.amazon.in/dp/'+asin[i]
            page=requests.get(url,headers=headers)
            soup=BeautifulSoup(page.content)
            
            for i in soup.findAll('a',{'class':['a-link-emphasis a-text-bold']}):
                link.append(i['href'])
    
    link = link[1:11]

    return link


def get_product_details(headers, company_list, asin, link):

    pasin = []
    reviews=[]
    dates = []
    stars = []
    name = []
    
    for comp in company_list:
        for i in range(0,len(link)):
    
            for j in range(0,10):
            
                url='https://www.amazon.in'+link[i]+'&pageNumber='+str(j)
                rev_page=requests.get(url,headers=headers)
            
                soup=BeautifulSoup(rev_page.content)
            
                for k in soup.findAll('span',{'data-hook':'review-body'}):
                    reviews.append(k.text.strip())
                
                for k in soup.findAll('i',{'data-hook':'review-star-rating'}):
                    stars.append(k.text.split(' ')[0].split('.')[0])
            
                for k in soup.findAll('span',{'data-hook':'review-date'}):
                    dates.append(k.text)
                    name.append(link[i].split('/')[1])
                    pasin.append(asin[i])


if __name__ == '__main__':

    company_list = get_company_list() 

    asin = get_product_asin(headers, company_list)

    link = get_product_links(headers, company_list, asin)

    get_product_details(headers, company_list, asin, link)