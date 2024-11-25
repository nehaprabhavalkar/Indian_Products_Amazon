import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import re 
from datetime import datetime
from utils import save_to_csv
########

DATA_PATH = '../data/'

FILE_NAME = 'reviews.csv'


def clean_data(reviews_df):
    for i in range(0,len(reviews_df)):
        reviews_df.date[i] = re.sub('Reviewed in India on','',reviews_df.date[i])
        reviews_df.date[i]= reviews_df.date[i].strip()
        reviews_df.date[i] = datetime.strptime(reviews_df.date[i],'%d %B %Y').date()

    reviews_df['rating'] = reviews_df['rating'].astype('int')

    return reviews_df


if __name__ == '__main__':
    df = pd.read_csv(DATA_PATH + FILE_NAME)

    cleaned_df = clean_data(df)

    save_to_csv(cleaned_df, DATA_PATH, FILE_NAME)

    