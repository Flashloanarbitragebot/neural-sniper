import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("trade_history.csv")
df['hour'] = pd.to_datetime(df['timestamp'], unit='s').dt.hour

X = df[['spread', 'gas_price', 'hour']]
y = df['profitable']

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

def predict(spread, gas, hour):
    return model.predict([[spread, gas, hour]])[0]

