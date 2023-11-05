import pandas as pd
import numpy as np

data = pd.read_csv("./Dataset/train_snli.csv",sep = "\t",header=0,names = ['Phrase','Suspicious','Class'])
