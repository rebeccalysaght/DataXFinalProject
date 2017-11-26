import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import re

restaurants = pd.read_csv('restaurants_AZ.csv')
c = restaurants['categories']
categories = []


for i in range(0, 2867):
    d = re.findall(r"'(.*?)'", c[i], re.DOTALL)
    for element in d:
        if element not in categories:
            categories.append(element)
categories_df = pd.DataFrame(categories)
categories_df.to_csv('categories_AZ.csv', encoding='utf-8', index=False)
