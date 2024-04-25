import pandas as pd
import numpy as np
#print("jeekl")
df=pd.read_csv("Finbud (set 1).csv")

X = df.drop(columns=['total'])  # Adjust 'total' to the name of your target column
y = df['total']

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

regr = LinearRegression()
regr.fit(X_train, y_train)

predictions = regr.predict(X_test)
# Calculate Mean Squared Error
mse = mean_squared_error(y_test, predictions)
print("Mean Squared Error:", mse)
user_budget = float(input("Enter your budget: "))
input_data = np.zeros((1, len(X_train.columns)))
input_data[0, 0] = user_budget

predicted_total_spending = regr.predict(input_data)[0]
prop = X.sum(axis=0) / X.sum().sum()
per_category = prop* predicted_total_spending
sum=0
for category, budget in zip(X.columns, per_category):
   print(f"{category}: {budget:.2f}")

print(per_category.sum())

#print(df.head(5))

import pickle

pickle.dump(regr,open('model.pkl','wb'))

model=pickle.load(open('model.pkl','rb'))
#print(len(model.columns))