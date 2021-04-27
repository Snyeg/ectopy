import pandas as pd
import numpy as np


df = pd.DataFrame(np.random.randint(0,100,size=(100, 1)), columns=["G1"])
df=df/100

data = pd.DataFrame(np.random.randint(0,30,size=(100, 1)), columns=["G1"])
data=data/100


class Threshold:
      def __init__(self, minThr,data):
          self.minThr = np.maximum(minThr,data.max())

threshold=Threshold(0.5,data)
print(df.head(20))
print(df.tail(20))

print(data.max())
print(threshold.minThr)
