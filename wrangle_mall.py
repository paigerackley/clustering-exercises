### IMPORTS ####
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

import env


def get_mall():
    query = '''
    SELECT * 
    FROM customers;
    '''
    url = env.get_db_url('mall_customers')
    df = pd.read_sql(query, url)
    return df


def split(df):
    train_and_validate, test = train_test_split(df, random_state=13, test_size=.15)
    train, validate = train_test_split(train_and_validate, random_state=13, test_size=.2)

    print('Train: %d rows, %d cols' % train.shape)
    print('Validate: %d rows, %d cols' % validate.shape)
    print('Test: %d rows, %d cols' % test.shape)

def scale_df(df):
    # making dummies for categorical column
    dummy_df = pd.get_dummies(df, columns = ['gender'], drop_first=True, dummy_na=False)

    # Scaling columns
    columns_to_scale = dummy_df.select_dtypes('number').columns.tolist()
    scaler = MinMaxScaler()
    scaled_df = dummy_df.copy()
    scaled_df[columns_to_scale] = pd.DataFrame(scaler.fit_transform(dummy_df[columns_to_scale]),
                                          columns=columns_to_scale).set_index([dummy_df.index])
    
    return scaled_df