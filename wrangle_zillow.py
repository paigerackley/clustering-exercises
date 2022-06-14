import pandas as pd
import numpy as np

import env
import os

## ACQUIRE ##

def get_zillow():
    '''
    This function acquires the requisite zillow data from the Codeup SQL database and caches it locally it for future use in a csv 
    document; once the data is accessed the function then returns it as a dataframe.
    '''

    filename = "zillow.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        query = '''
    SELECT
        prop.*,
        predictions_2017.logerror,
        predictions_2017.transactiondate,
        air.airconditioningdesc,
        arch.architecturalstyledesc,
        build.buildingclassdesc,
        heat.heatingorsystemdesc,
        landuse.propertylandusedesc,
        story.storydesc,
        construct.typeconstructiondesc
    FROM properties_2017 prop
    JOIN (
        SELECT parcelid, MAX(transactiondate) AS max_transactiondate
        FROM predictions_2017
        GROUP BY parcelid
    ) pred USING(parcelid)
    JOIN predictions_2017 ON pred.parcelid = predictions_2017.parcelid
                          AND pred.max_transactiondate = predictions_2017.transactiondate
    LEFT JOIN airconditioningtype air USING (airconditioningtypeid)
    LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid)
    LEFT JOIN buildingclasstype build USING (buildingclasstypeid)
    LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid)
    LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid)
    LEFT JOIN storytype story USING (storytypeid)
    LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid)
    WHERE prop.latitude IS NOT NULL
      AND prop.longitude IS NOT NULL
      AND transactiondate <= '2017-12-31'
      AND propertylandusedesc = "Single Family Residential"
'''

## Other functions ##

def overview(df):
    print('--- Shape: {}'.format(df.shape))
    print()
    print('--- Info')
    df.info()
    print()
    print('--- Column Descriptions')
    print(df.describe(include='all'))

def nulls_by_columns(df):
    return pd.concat([
        df.isna().sum().rename('count'),
        df.isna().mean().rename('percent')
    ], axis=1)

def nulls_by_rows(df):
    return pd.concat([
        df.isna().sum(axis=1).rename('n_missing'),
        df.isna().mean(axis=1).rename('percent_missing'),
    ], axis=1).value_counts().sort_index()

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column * len(df.index), 0))
    df.dropna(axis=1, thresh = threshold, inplace = True)
    threshold = int(round(prop_requred_row * len(df.columns), 0))
    df.dropna(axis = 0, thresh = threshold, inplace = True)


    ## SPLIT ##

def split_zillow_data(df):

    train_validate, test = train_test_split(df, test_size=.2, 
        random_state=123)

    train, validate = train_test_split(train_validate, test_size=.3, 
        random_state=123)
    return train, validate, test