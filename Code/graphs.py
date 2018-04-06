import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dist_table(data, col):
    dist = pd.DataFrame(data[col].value_counts().reset_index())
    dist.columns = [col, 'count']
    return dist

def analysis_table(data, field):
    data['win'] = data['payprice'] <= data['bidprice']
    df = pd.DataFrame({'impressions': data.groupby(field).size()}).reset_index() 
    df = df.join(pd.DataFrame({'wins': data.groupby(field)['win'].sum()}).reset_index(drop=True))
    df = df.join(pd.DataFrame({'clicks': data.groupby(field)['click'].sum()}).reset_index(drop=True)) # Total Clicks
    df['CTR'] = df['clicks']/df['impressions']*100
    df = df.join(pd.DataFrame({'spend': data.groupby(field)['payprice'].sum()/1000}).reset_index(drop=True)) # Total Pay/Cost
    df['CPM'] = df['spend']*1000/df['impressions'] # Cost per-mille (Cost per Thousand Impressions)
    df['eCPC'] = df['spend']/df['clicks'] # Effective Cost-per-Click 
    df = df.join(pd.DataFrame({'avgPayPrice': data.groupby(field)['payprice'].mean()}).reset_index(drop=True))
    df = df.join(pd.DataFrame({'avgBidPrice': data.groupby(field)['bidprice'].mean()}).reset_index(drop=True))
    df['priceDiff'] = df['avgBidPrice'] - df['avgPayPrice'] # Difference between bidprice and payprice
    #df = df.join(pd.DataFrame({'n_advertisers': data.groupby(field)['advertiser'].nunique()}).reset_index(drop=True))
    #df = df.join(pd.DataFrame({'common_weekday': data.groupby(field)['weekday'].mean()}).reset_index(drop=True))
    df = df.fillna(0)
    
    return df

def plot_bar_graph(summary, xcol, ycol, xlabel, ylabel, title):
    ind = np.arange(len(summary))  # the x locations for the groups
    width = 0.4
    plt.bar(ind, summary[ycol],width, color="lightblue")
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.xticks(ind, summary[xcol])
    plt.show()

def plot_price_distribution(data, price):
    width = 0.6
    dist = dist_table(data, price)
    plt.bar(dist[price], dist['count'],width, color="black")
    plt.ylabel('Count')
    plt.xlabel(price)
    plt.title('Distribution of ' + price)
    plt.show()
    
def plot_pie_chart(data, col):
    
    dist = pd.DataFrame(data[col].value_counts().reset_index())
    dist.columns = [col, 'count']
    labels = dist[col]
    counts = dist['count']
    
    # Data to plot
    colors = ['lightgrey', 'orange', 'yellowgreen', 'lightcoral']
    #explode = (0.1, 0, 0, 0)  # explode 1st slice

    # Plot
    plt.pie(counts, labels=labels, colors=colors, shadow=True, startangle=140)
    plt.legend( loc = 'right', labels=['%s, %1.1f %%' % (l, s) for l, s in zip(labels, counts/np.sum(counts)*100)])

    plt.axis('equal')
    plt.show()
    
    return dist