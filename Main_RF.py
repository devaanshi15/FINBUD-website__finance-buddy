import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor

# Load the CSV file into a DataFrame
finbud_df = pd.read_csv("Finbud (set 1).csv")

# Assuming you have a list of features in the DataFrame columns
features = finbud_df.columns.tolist()

# Remove the feature named "total" from the list of features
features.remove("total")

# Ask the user for their budget
budget = float(input("Enter your budget: "))

# Ask the user to input their top three features
top_features = []
for i in range(3):
    feature = input("Enter your {} most important feature: ".format("first" if i == 0 else "second" if i == 1 else "third"))
    top_features.append(feature)

# Remove user-selected top features from the list of all features
remaining_features = [feature for feature in features if feature not in top_features]

# Calculate the total number of remaining features
num_remaining_features = len(remaining_features)

# Allocate money to each feature based on their rank and the budget provided by the user
allocated_budget = {}
remaining_budget = budget
for feature in top_features:
    allocated_amount = remaining_budget / (num_remaining_features + len(top_features))
    allocated_budget[feature] = allocated_amount
    remaining_budget -= allocated_amount

# Calculate mean values for the remaining features
remaining_feature_means = finbud_df[remaining_features].mean()

# Rank the remaining features based on their mean values
ranked_remaining_features = remaining_feature_means.sort_values(ascending=False)
# Allocate the remaining budget among the remaining features proportionally based on their mean values
remaining_total_mean = finbud_df[remaining_features].mean().sum()
for feature in remaining_features:
    feature_mean = finbud_df[feature].mean()
    allocated_budget[feature] = budget * (feature_mean / remaining_total_mean)

# Calculate the total allocated budget for all features
total_allocated_budget = sum(allocated_budget.values())

# Normalize the allocated budget to match the input budget provided by the user
allocation_factor = budget / total_allocated_budget
for feature in allocated_budget:
    allocated_budget[feature] *= allocation_factor

# Display the allocated budget for each feature
print("\nAllocated Budget for Each Feature:")
for feature, amount in allocated_budget.items():
    print("{}: {:.2f}".format(feature, amount))



# Train a regression model to predict the total budget allocation
X = finbud_df[features].values
y = finbud_df['total'].values
regr = RandomForestRegressor()
regr.fit(X, y)

pickle.dump(regr,open('model2.pkl','wb'))

#model=pickle.load(open('model.pkl','rb'))

# Construct the budget allocation array in the same order as the features
budget_allocation = [allocated_budget[feature] for feature in features]

# Predict total budget allocation using the trained model
predicted_total_budget = sum(allocated_budget.values())
print("Sum of Allocated Budget for Each Feature:", predicted_total_budget)
# Check if the predicted total budget matches the input budget
print("Budget Matches Predicted Total Budget Allocation:", np.isclose(predicted_total_budget, budget))
