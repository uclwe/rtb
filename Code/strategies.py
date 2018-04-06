import numpy as np

def constant_bidding_strategy(size, c):
    bids = np.ones(size)
    return c*bids

def random_bidding_strategy(size, min_bet=0, max_bet=300, mean=272, std=28, distribution="uniform"):
    
    if distribution=="uniform":
        return np.random.randint(min_bet, max_bet, size=size)
    
    elif distribution=="normal":
        return np.random.normal(mean, std, size=size).astype(int) #integer values for now

def ortb_bidding_strategy(pred, c=30, lmda=1, ortbtype=1):
    n = pred.shape[0]
    if ortbtype==1:
        return np.sqrt(np.repeat(c, n) / np.repeat(lmda, n) * np.array(pred) + np.repeat(c, n) ** 2) - np.repeat(c, n)
    else:
        expr = (np.array(pred) + np.sqrt(np.repeat(c, n) ** 2 * np.repeat(lmda, n) * 2 + np.repeat(c, n) ** 2)) / \
                                                                                       (np.repeat(c, n) * np.repeat(lmda, n))
        return np.repeat(c, n) * (expr ** (1 / 3) - expr ** (-1 / 3))