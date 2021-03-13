import numpy as np
import pandas as pd
import scipy as sp
from sklearn.metrics import roc_auc_score
from sklearn.datasets import make_classification
from tqdm import trange

def boot_gini_eq(a, b, n=1000, share=0.8, two_sided=True):
    """Function to assess Gini equality for two samples
    
    Parameters
    ----------
        a: pd.DataFrame
            First sample as dataframe with target as first 
            column and score as second
        b: pd.DataFrame
            Second sample as dataframe with target as first 
            column and score as second
        n: int, optional (defaul=1000)
            Number of bootstrapped samples
        share: float, optional (default=0.8)
            Share of observations in bootstrapped subsample
        two_sided: bool, optional (default=True)
            One- or two-sided hypothesis testing
            
    Returns
    -------
        out: list of tuples
            Returns two Gini point estimates and statistic value
            with corresponding p-value
    """
    
    boot_a = np.random.choice(a.index,(int(np.round(a.shape[0] * share), 0), n))
    boot_b = np.random.choice(b.index,(int(np.round(b.shape[0] * share), 0), n))
    gini_a = 2*roc_auc_score(a.iloc[:,0], a.iloc[:,1])-1
    gini_b = 2*roc_auc_score(b.iloc[:,0], b.iloc[:,1])-1
    
    gini_diff = []
    for i in trange(n):
        diff = 2*(roc_auc_score(a.iloc[boot_a[:,i], 0], a.iloc[boot_a[:,i], 1]) - roc_auc_score(b.iloc[boot_b[:,i], 0], b.iloc[boot_b[:,i], 1]))
        gini_diff.append(diff)
        
    s = np.std(gini_diff)
    
    D = (gini_a - gini_b)/s
    p_val = sp.stats.norm.sf(abs(D))*2 if two_sided else sp.stats.norm.sf(abs(D))
    out = [(gini_a, gini_b), (D, p_val)]

    return out

if __name__ == '__main__':

    X, y = make_classification(1000,1,1,0,0,2,1,class_sep=0.5)
    a = pd.concat([pd.Series(y,name='target'), pd.DataFrame(X,columns=['score'])],axis=1)

    X, y = make_classification(200,1,1,0,0,2,1,class_sep=0.2)
    b = pd.concat([pd.Series(y,name='target'), pd.DataFrame(X,columns=['score'])],axis=1)

    print('Generated Gini #1: {0:.5f}'.format(2*roc_auc_score(a.target, a.score)-1))
    print('Generated Gini #2: {0:.5f}'.format(2*roc_auc_score(b.target, b.score)-1))

    out = boot_gini_eq(a, b, n=1000, share=0.8)
    print('D-statistic: {0:.5f}'.format(out[1][0]))
    print('P-value: {0:.5f}%'.format(out[1][1]))
