import numpy as np
import pandas as pd

def performance(bids, true, budget=6250*1000, verbose=True):
    """
    args:
        bids - np array
        true - dataframe
        budget - stop when the sum of the bids reaches this

    returns:
        <all as defined above>
        CTR, clicks, spend, aCPM, aCPC

        could also return info about when you ran out of money (i.e. what percentage through the data set)
    """
    CTR, num_clicks, spend, aCPM, aCPC = (0,0,0,0,None)


    #--- Combine data in to one dataframe ------
    df = true.copy()
    df['bid'] = bids



    #--- Work out which bids were successful ---
    #> if they are greater than payprice
    success_bids = df[df.bid > df.payprice]



    #--- Only keep bids that are within budget -
    total_spend = np.cumsum(np.array(success_bids.payprice))

    x=0
    if len(total_spend)>0:
        x = np.argmax(total_spend > budget)

    if x>0:
        # then at some point bids went over budget
        in_budget_bids = success_bids[0:x-1]

    else:
        in_budget_bids = success_bids

    spend = in_budget_bids.payprice.sum()


    #--- Find out which bids were clicked ------
    clicked_bids = in_budget_bids[in_budget_bids.click==1]

    num_clicks = len(clicked_bids.payprice)

    #--- click through rate -------
    CTR = num_clicks/len(success_bids) if len(success_bids) > 0 else None



    #--- Calculate average cost per click ------

    if num_clicks > 0:
        aCPC = spend//num_clicks #<--- left as an integer for now

    if verbose:
        print("       CTR:", "({0:.4f})%".format(CTR))
        print("num_clicks:", num_clicks)
        print("     spend:", spend, "({0:.2f})%".format(100*spend/budget))
        print("      aCPM:", aCPM)
        print("      aCPC:", aCPC)


    return CTR, num_clicks, spend, aCPM, aCPC

def new_performance(bids, true_y, budget=6250*1000, verbose=True, return_stats=True):
    """
    args:
        bids - np array
        true - dataframe
        budget - stop when the sum of the bids reaches this
        
    returns:
        <all as defined above>
        CTR, clicks, spend, aCPM, aCPC, num_in_budget_wins, ads_within_budget
        could also return info about when you ran out of money (i.e. what percentage through the data set)
    """
    CTR, num_clicks, spend, aCPM, aCPC = (0,0,0,0,None)
    
    #--- Combine data in to one dataframe ------
    data = true_y.copy()
    data['bid'] = bids
    
    #--- Work out which bids were successful ---
    #> if they are greater than payprice
    won_bid = data.payprice <= data.bid 
    
    #--- Only keep bids that are within budget -
    success_bids_csum = np.cumsum(np.array(data.payprice) * won_bid)

    #--- prior budget check 
    prior_success_bids_csum = ([0] + list(success_bids_csum))[:len(success_bids_csum)]
    new_budget = np.repeat(budget, len(success_bids_csum)) - prior_success_bids_csum
    
    #--- in budget 
    in_budget_bids = (success_bids_csum <= np.repeat(budget, len(success_bids_csum))) & (np.array(data.bid) <= new_budget)
    in_budget_wins = won_bid & in_budget_bids
    num_in_budget_wins = np.sum(in_budget_wins)
    
    #--- Find out which bids were clicked ------
    num_clicks = np.sum(in_budget_wins & (np.array(data.click) == 1))
    spend = int(success_bids_csum[in_budget_bids == True][-1:]) if num_clicks > 0 else 0
    impressions = np.sum(in_budget_bids)
    
    #--- click through rate -------
    CTR = num_clicks/num_in_budget_wins*100 if num_in_budget_wins > 0 else None
    
    #--- Calculate average cost per click ------
    if num_clicks > 0:
        aCPC = (spend/1000)/num_clicks #<--- left as an integer for now
    aCPM = (spend/impressions) if impressions > 0 else 0
    
    if verbose:  
        print("               CTR:", "({0:.4f})%".format(CTR))
        print("        num_clicks:", num_clicks)
        print("             spend:", spend, "({0:.2f})%".format(100*spend/budget))
        print("              aCPM:", aCPM)
        print("              aCPC:", aCPC)
        print("num_in_budget_wins:", num_in_budget_wins)
        print(" ads_within_budget:", impressions)
        
    
    if return_stats:
        return CTR, num_clicks, spend, aCPM, aCPC, num_in_budget_wins, impressions

def performance_statistics(data, budget=200000*1000, verbose=True, return_stats=False):
    """
    args:
        data - dataframe
        budget - stop when the sum of the bids reaches this
        
    returns:
        <all as defined above>
        CTR, clicks, spend, aCPM, aCPC, num_in_budget_wins, ads_within_budget
        could also return info about when you ran out of money (i.e. what percentage through the data set)
    """
    CTR, num_clicks, spend, aCPM, aCPC = (0,0,0,0,None)
    
    #--- Work out which bids were successful ---
    #> if they are greater than or equal to payprice (Winning Criteria #1)
    won_bid = data.payprice <= data.bidprice 
    
    # Cummulative sum of payprice for the bids that were won
    success_bids_csum = np.cumsum(np.array(data.payprice) * won_bid)

    # prior budget check  - works out leftover budget at the time of each impression
    prior_success_bids_csum = ([0] + list(success_bids_csum))[:len(success_bids_csum)]
    new_budget = np.repeat(budget, len(success_bids_csum)) - prior_success_bids_csum
    
    # in budget bids = cumsum is less than the budget and the bidprice is less than the budget at that time (Truth telling)
    in_budget_bids = (success_bids_csum <= np.repeat(budget, len(success_bids_csum))) & (np.array(data.bidprice) <= new_budget)
    impressions = np.sum(in_budget_bids)
    
    # in budget wins
    in_budget_wins = won_bid & in_budget_bids
    num_in_budget_wins = np.sum(in_budget_wins)
    
    # Find out which in-budget bids were clicked & spend------
    num_clicks = np.sum(in_budget_wins & (np.array(data.click) == 1))
    spend = int(success_bids_csum[in_budget_bids == True][-1:]) if num_clicks > 0 else 0
   
    # if budget was set to default then it meant we had no budget ie budget = spend
    budget = spend if budget == 200000*1000 else budget
    
    # click through rate
    CTR = num_clicks/num_in_budget_wins*100 if impressions > 0 else None
    
    # calculate average cost per click 
    if num_clicks > 0:
        aCPC = (spend/1000)//num_clicks #<--- left as an integer for now
    
    # other useful metrics
    avg_market_price = np.average(in_budget_bids*data.payprice)
    avg_bid_price = np.average(in_budget_bids*data.bidprice)
    num_advertisers = len(np.unique(data['advertiser'][in_budget_bids == True]))
    aCPM = (spend/impressions)
    
    if verbose:
        print("               CTR:", "({0:.4f})%".format(CTR))
        print("        num_clicks:", num_clicks)
        print("             spend:", spend, "({0:.2f})%".format(100*spend/budget))
        print("              aCPM:", aCPM)
        print("              aCPC:", aCPC)
        print("num_in_budget_wins:", num_in_budget_wins)
        print(" ads_within_budget:", impressions)
        print("  avg_market_price:", avg_market_price)
        print("   num_advertisers:", num_advertisers)
        print("     avg_bid_price:", avg_bid_price)
    if return_stats:
        return CTR, num_clicks, spend, aCPM, aCPC, num_in_budget_wins, impressions, avg_market_price, num_advertisers, avg_bid_price

def merge_sets(datasets): 
    """
    args:
        datasets: list of datasets e.g. [train_X, valid_X, test_X]
        
    returns:
        concatenated datasets
    """
    data = pd.concat(datasets)

    return data

def one_hot_encoding(data, columns = ['useragent','region', 'city', 'adexchange', 'urlid', 'slotwidth','slotheight', 
                                      'slotvisibility', 'slotformat', 'slotprice', 'creative','keypage', 'advertiser',
                                      'weekday', 'hour']):
    """
    args:
        data: data that needs to be encoded
        columns: relevant columns
        
    returns:
        one hot encoded data
    """
    data = pd.get_dummies(data, columns=columns)

    return data

def split_sets(merged, shapes):
    """
    args:
        merged: merged datasets
        shapes: number of rows in each set (prior to merge
        
    returns:
        merged dataset split into initial datasets
    """
    sets = ()
    splits = []
    max_len = len(merged)
    for i in range(len(shapes)):
        start = 0
        end = max_len
        if i == 0:
            end = shapes[0]
            splits.append(end)
            print ("splits", splits)
        else:
            start = splits[i-1]
            end = start + shapes[i] if start + shapes[i] < max_len else max_len
            splits.append(end)
        sets += (merged[start:end],)
    return sets

def add_user_tag_feature(data):
    data['usertag'] = data['usertag'].str.split(',')
    d_tags = data['usertag'].str.join('#').str.get_dummies('#').add_prefix('usertag_')
    return d_tags

def split_useragent(data):
    return data.join(pd.DataFrame(data['useragent'].str.split('_',1).tolist(), columns = ['os','browser'])).drop(['useragent'], axis=1)

def join_height_width(data):
    return data.join(pd.DataFrame({'slotarea': data['slotheight']*data['slotwidth']})).drop(['slotwidth', 'slotheight'], axis=1)
