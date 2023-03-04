import pandas as pd
from joblib import dump, load
from sklearn.metrics.pairwise import cosine_similarity
# Load the saved model from disk
# kmeans = load('kmeans_model.joblib')


def predict(budjet,mass,products):
    # -------------------------user--------------------
    kmeans= load('C:\\Users\\NEW.PC\\Documents\\GitHub\\JumperMicroHack\\main\\model\\kmeans_model.joblib')
    df_sorted=pd.read_excel('C:\\Users\\NEW.PC\\Documents\\GitHub\\JumperMicroHack\\main\\model\\data_clustered.xlsx')
    budget = budjet
    products_list = products
    mass = mass 
    def get_quality(price):
        if price >=50 :
            return 'high'
        elif price >=10 and price<50 :
            return 'medium'
        elif price >0 and price<10 :
            return 'low'
    def get_quantity(mass):
        if mass >=100 :
            return 'high'
        elif mass >=20 and mass<100 :
            return 'medium'
        elif mass >=1 and mass<20 :
            return 'low'
    price_unit=(budget/len(products_list))/mass
    user_row=[]
    for i in products_list:
        user_row.append( {
            'product_id': i,
            'quality': get_quality(price_unit),
            'quantity': get_quantity(mass) ,
            'price': price_unit,
        })
    user_df = pd.DataFrame(user_row)
    quality_map = {'low': 0, 'medium': 1, 'high': 2}
    user_df['quality'] = user_df['quality'].replace(quality_map)
    user_df['quantity'] = user_df['quantity'].replace(quality_map)
    print(user_df)
    X_user = user_df[['product_id','quality', 'quantity','price']]

    user_cluster = kmeans.predict(X_user)
    result=[]
    for i in range(len(products_list)):
        clust=df_sorted[df_sorted['cluster'] == user_cluster[i]]
        prod_clust=clust[clust['product_id'] == products_list[i]]
        similarity = cosine_similarity(X_user.loc[i].values.reshape(1, -1), prod_clust[['product_id','quality', 'quantity','price']])
        # Add similarity as a column to the filtered data
        prod_clust['similarity'] = similarity[0]
        prod_clust = prod_clust.sort_values(by=['similarity'], ascending=False)
        sub_res=[]
        for j in range(4):
            q=list(prod_clust['business_id'])[j]
            q=q.replace("B", "")
            q=int(q)
            s=list(prod_clust['product_id'])[j]
            d=list(prod_clust['similarity'])[j]
            sub_res.append({'business_id':q,'similarity':"{:.2f}".format(d*100),'product_id':s})
        result.append(sub_res)        
        # print('product : ',products_list[i],' belong to cluster : ')
        # print(prod_clust)
    return result
