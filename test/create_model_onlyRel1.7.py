import argparse
 
parser = argparse.ArgumentParser(description="Remolog Classifier Generator",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("input", help="input table (data/data.csv)")
parser.add_argument("-o", "--output", default="model.joblib", help="model name")
args = parser.parse_args()
config = vars(args)


import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
import xgboost as xgb
from sklearn.pipeline import Pipeline
from joblib import dump, load

#url = "https://raw.githubusercontent.com/tetsufmbio/remolog/main/data/"
#dataset = "data.csv"

data = pd.read_csv(config["input"])
X = data.iloc[:,3:-1]
X.drop(X.columns[[1,3,6,11,17,18,19,21,24,25,26,29,30]], axis=1, inplace=True)
#X = X.filter(regex="tm_|lovo_|cl=")
y = data.iloc[:,-1]
pipe = Pipeline([('scaler', RobustScaler()), ('clf', xgb.XGBClassifier(
        colsample_bylevel=0.4, 
        colsample_bytree=0.7, 
        learning_rate=0.1, 
        max_depth=15,
        n_estimators=500,
        subsample=0.5,
        use_label_encoder=False
    ))])
pipe.fit(X, y)

dump(pipe, config["output"])
