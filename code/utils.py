def get_company_list():

    company_list = ['mamaearth','godrej','titan watch','frooti','amul',
                    'patanjai','dettol','cinthol','britannia biscuits','streax',
                    'himalaya products','society tea','tata tea','fastrack watches',
                    'mysore sandal']


    return company_list

def save_to_csv(df, path, file_name):
    df.to_csv(path + file_name, index=False)

