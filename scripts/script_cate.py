import numpy as np
import pandas as pd

from causalml.inference.meta import BaseTRegressor
from xgboost import XGBRegressor

def script_cate():

    df = pd.read_csv('../data/demo_data.csv')
    
    #define outcome (y), features (X), treatment for metalearner
    y=df['healthscore_post'].values
    y = (y-np.mean(y))/np.std(y)
    
    treatment = df['intervention']
    X=pd.concat([df['healthscore_pre'],df['age group'],df['gender'],df['exercise frequency'],
                df['pre existing conditions'],df['income group'],df['vegetarian/vegan']],axis=1).values

    #ATE (T-Learner)
    learner_t_xgb = BaseTRegressor(learner=XGBRegressor())
    ate_t = learner_t_xgb.estimate_ate(X=X, treatment=treatment, y=y)

    #ITE
    cate_t = learner_t_xgb.fit_predict(X=X, treatment=treatment, y=y)

    df['cate_t'] = cate_t

    #Rename column values
    df.replace({'age group':{1:'Age 21-30',2:'Age 31-40',3:'Age 41 and above'},
                'gender':{0:'Male',1:'Female'},
                'exercise frequency':{0:'0/week',1:'1/week',2:'2/week',3:'3/week',4:'4/week',5:'5/week',6:'6/week',7:'7/week'},
                'pre existing conditions':{0:'None',1:'Yes'},
                'income group':{0:'No',1:'Yes'},
                'vegetarian/vegan':{0:'No',1:'Yes'}},inplace=True)
    df.to_csv('../data/demo_data_ite.csv',index=False)

    return df,ate_t

if __name__ == '__main__':
    script_cate()
