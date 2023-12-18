# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 19:20:44 2023

@author: beave
"""

import pandas as pd
#%%
project_repo = 'G:/Code/IE104-retailer-web-project/'
project_data = 'G:/Code/IE104-retailer-web-project/data/'
#%%
df = pd.read_csv(project_data+'DataCoSupplyChainDataset.csv',encoding='latin1')
#%%
df_items = df[['Department Id','Department Name','Category Name','Category Id','Product Card Id','Product Description','Product Name','Product Price'
           ,'Product Status']].drop_duplicates(subset=['Product Card Id'],keep='last')
df_items['ProductSoldQuantity'] = df_items['Product Card Id'].apply(lambda x : df[['Product Card Id','Order Item Quantity']]
                                                                    [df['Product Card Id']==x].groupby(['Product Card Id']).sum().values[0,0])
df_items_with_desc = pd.read_csv("G:/Code/IE104-retailer-web-project/product_descriptions/Products2.csv")
df_items['Product Description'] = df_items['Product Card Id'].apply(lambda x: df_items_with_desc[df_items_with_desc['ProductCardId'] == x]['ProductDescription'].values[0])
df_items.to_csv(project_data+'Products.csv',header = [ i.replace(' ','') for i in df_items.columns], index=False)
#%%
df_customers = df[['Customer Id', 'Customer City','Customer Country','Customer Fname','Customer Lname','Customer Password','Customer Segment','Customer State',
                     'Customer Street','Customer Zipcode']].drop_duplicates(subset=['Customer Id'],keep='last')
df_customers['Customer Zipcode'] = df['Customer Zipcode'].apply(lambda x: int(x) if float(x).is_integer() else 0 )
df_customers['Customer Email']=df['Customer Id'].apply(lambda x: str(x)+"@fakeaddress.wobble")
df_customers['Customer Password']=df['Customer Id'].apply(lambda x: "pw"+str(x))
df_customers.to_csv(project_data+'Customers.csv',header = [ i.replace(' ','') for i in df_customers.columns],index=False)
#%%
df_payments = df[['Type','Customer Id','Customer Lname','Customer Fname',
                  'Order Id','order date (DateOrders)','Order Item Total',
                  'Department Id','Department Name','Order Status']].groupby(['Type','Customer Id','Customer Lname','Customer Fname',
                                    'Order Id','order date (DateOrders)',
                                    'Department Id','Department Name','Order Status']).sum().reset_index()
df_payments.to_csv(project_data+"Payments.csv",header = [ i.replace(' ','') for i in df_payments.columns],index=False)
#%%
df_orders = df
df_orders = df_orders.drop(['Benefit per order','Sales per customer','Category Id','Category Name','Order Item Cardprod Id'
                ,'Order Item Discount','Order Item Id','Order Item Product Price','Order Item Profit Ratio',
                'Order Item Quantity','Sales','Product Card Id','Product Category Id','Product Description',
                'Order Zipcode', 'Market','Latitude','Longitude','Department Name','Department Id','Order City',
                'Order Country','Order Customer Id','Order State','Order Region',
                'Product Image','Product Name','Product Price','Product Status','Order Item Discount Rate',
                'Order Profit Per Order','Order Item Total','Customer Password'],axis=1).drop_duplicates(subset=['Order Id'],keep='last')
# order_cols = list(df_orders.columns)
# order_cols.remove('Order Item Total')
df_test = df[['Order Id','Order Item Total']].groupby(['Order Id'],as_index=False).sum()
df_orders['Total'] = df_orders['Order Id'].apply(lambda x: df_test[df_test['Order Id'] == x ]['Order Item Total'].values[0])
df_orders.to_csv(project_data+"Orders.csv",header = [ i.replace(' ','') for i in df_orders.columns],index=False)
#%%
df_order_details = df[['Category Id','Category Name','Department Id','Department Name','Order Id',
                       'Order Item Discount','Order Item Discount Rate','Order Item Id',
                       'Order Item Profit Ratio','Order Item Quantity','Sales','Product Price',
                       'Order Item Total','Product Card Id','Product Price','Product Name','Customer Id']]
df_order_details.to_csv(project_data+"Order_details.csv",header = [ i.replace(' ','') for i in df_order_details.columns],index=False)
#%%
df_departments = df[['Department Name','Department Id']].drop_duplicates(subset=['Department Id'],keep='last')
df_departments.to_csv(project_data+"Deparmtents.csv",header = [ i.replace(' ','') for i in df_departments.columns],index=False)
#%%
df_categories = df[['Category Id','Category Name']].drop_duplicates(subset=['Category Id'],keep='last')
df_categories.to_csv(project_data + "Categories.csv",header = [ i.replace(' ','') for i in df_categories.columns],index=False)