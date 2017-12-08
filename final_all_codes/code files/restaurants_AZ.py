import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly

business = pd.read_csv('business.csv')
business_AZ = business[business['state'] == 'AZ']
business_AZ = business_AZ.reset_index()
del business_AZ['index']
for i in range(0, len(business_AZ)):
    if 'Restaurants' not in business_AZ.loc[i]['categories']:
        business_AZ = business_AZ.drop(i)
        business_AZ = business_AZ.reset_index()
del business_AZ['index']

business_AZ.to_csv('restaurants_AZ.csv', encoding='utf-8', index=False)
