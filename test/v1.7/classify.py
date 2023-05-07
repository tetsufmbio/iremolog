import argparse
 
parser = argparse.ArgumentParser(description="Remolog Classifier",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("input", help="input table")
parser.add_argument("model", help="model file from joblib")
parser.add_argument("-o", "--output", default="result.tab", help="output name")
args = parser.parse_args()
config = vars(args)

from joblib import load
from sklearn.preprocessing import RobustScaler
import xgboost as xgb
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
								 
clf = load(config["model"])

header = ["query", "subject",
          "lovo_finalScore", "lovo_coverage", "lovo_rmsd", "lovo_gaps", "lovo_relCov", "lovo_relGaps", "lovo_coverage3a","lovo_relCov3a","lovo_rmsd3a","lovo_relCovDiff","lovo_finalScoreNorm",
          "tm_AliLen", "tm_RMSD", "tm_n_ident/n_aln", "tm_TM-score (chain 2)", "tm_d0 (chain 2)","tm_cov",
          "fatcat_subject-len", "fatcat_Twists", "fatcat_ini-len", "fatcat_ini-rmsd", "fatcat_opt-equ", "fatcat_opt-rmsd", "fatcat_chain-rmsd", "fatcat_Score", "fatcat_align-len", "fatcat_Gaps", "fatcat_rel_score", "fatcat_rel_align",
          'cl=46456', 'cl=48724', 'cl=51349', 'cl=53931', 'cl=56572', 'cl=56835', 'cl=56992']

data = pd.read_csv(config["input"], sep="\t", header=None)
data.columns = header

X = data.iloc[:,2:]
X.drop(X.columns[[1,3,6,11,17,18,19,21,24,25,26,29,30]], axis=1, inplace=True)
pred = clf.predict(X)
pred_proba = clf.predict_proba(X)
data["pred"] = pred
data["pred_proba"] = pred_proba[:,1]
data = data.sort_values(by=["query", "pred_proba"], ascending=[True, False])
data.to_csv(config["output"], index=False)
