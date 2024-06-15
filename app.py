

from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load your model and data here
df = pd.read_csv("Finbud (set 1).csv")
X = df.drop(columns=['total'])

model = pickle.load(open('model.pkl', 'rb'))
model2 = pickle.load(open('model2.pkl', 'rb'))

# Define routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/models')
def models():
    return render_template('models_pg.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/calendar')
def calendar():
    return render_template('Calendar.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        user_budget = float(request.form["budget"])
        input_data = np.zeros((1, len(X.columns)))
        input_data[0, 0] = user_budget
        predicted_total_spending = model.predict(input_data)[0]
        prop = X.sum(axis=0) / X.sum().sum()
        per_category = prop * predicted_total_spending
        predicted_categories = {category: budget for category, budget in zip(X.columns, per_category)}
        return render_template("result.html", categories_budget=predicted_categories, total_budget=predicted_total_spending)
    else:
        return render_template('index.html')
    

    # ---------------------------------------------------------
features = df.columns.tolist()
features.remove("total")  # Remove the target column from features
categories = features.copy()

@app.route('/predict_2', methods=['GET', 'POST'])
def predict_2():
    if request.method == 'POST':
        budget = float(request.form['budget'])
        top_features = [request.form['first'], request.form['second'], request.form['third']]
        remaining_features = [feature for feature in features if feature not in top_features]

        num_remaining_features = len(remaining_features)
        allocated_budget = {}
        remaining_budget = budget

        for feature in top_features:
            allocated_amount = remaining_budget / (num_remaining_features + len(top_features))
            allocated_budget[feature] = allocated_amount
            remaining_budget -= allocated_amount

        remaining_feature_means = df[remaining_features].mean()
        remaining_total_mean = df[remaining_features].mean().sum()
        for feature in remaining_features:
            feature_mean = df[feature].mean()
            allocated_budget[feature] = budget * (feature_mean / remaining_total_mean)

        total_allocated_budget = sum(allocated_budget.values())
        allocation_factor = budget / total_allocated_budget
        for feature in allocated_budget:
            allocated_budget[feature] *= allocation_factor

        budget_allocation = [allocated_budget[feature] for category in categories]
        input_data = np.array(budget_allocation).reshape(1, -1)
        predicted_total_budget = model2.predict(input_data)[0]

        #return render_template('result2.html', allocated_budget=allocated_budget, predicted_total_budget=predicted_total_budget)
        return render_template('result2.html', allocated_budget=allocated_budget)
    else:
        return render_template('index2.html',categories=categories)

# def predict():
#     if request.method == 'POST':
#         # Handle the POST request
#         user_budget = float(request.form["budget"])
#         # Process the budget, perform prediction, etc.
#         return redirect(url_for('result'))  # Redirect to the result page after processing the form
#     else:
#         # Handle the GET request
#         return render_template('index.html')

