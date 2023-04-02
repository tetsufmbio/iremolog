import argparse
 
parser = argparse.ArgumentParser(description="Remolog Classifier Generator",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("input", help="input table (data/data.csv)")
parser.add_argument("-o", "--output", default="model.joblib", help="model name")
args = parser.parse_args()
config = vars(args)


import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from joblib import dump, load

#url = "https://raw.githubusercontent.com/tetsufmbio/remolog/main/data/"
#dataset = "data.csv"

data = pd.read_csv(config["input"], header=None)
X = data.iloc[:,3:-1]
y = data.iloc[:,-1]
pipe = Pipeline([('scaler', StandardScaler()), ('svc', SVC(C=10.0000, gamma=0.010, kernel="rbf", class_weight="balanced", probability=True))])
pipe.fit(X, y)

dump(pipe, 'model.joblib')