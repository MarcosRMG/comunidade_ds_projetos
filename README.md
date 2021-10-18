# Rossmann Store Sales
![alt_text](storytelling/img/rossmann_store.jpeg)

# 1 Business Understanding
Rossmann operates over 3,000 drug stores in 7 European countries. Currently, Rossmann store managers are tasked with predicting their daily sales for up to six weeks in advance. Store sales are influenced by many factors, including promotions, competition, school and state holidays, seasonality, and locality. 
With thousands of individual managers predicting sales based on their unique circumstances, the accuracy of results can be quite varied. (kaggle.com)


## 1.1 Business Question

What will be the sales per store for the next 6 weeks?

## 1.2 Business Objectives

Develop a standardized methodology for sales forecasting.

## 1.3 Project Plan

Through Exploratory Data Analysis, choose a Machine Learning Algorithm to forecast sales.

### 1.4 Data Product

API in Telegram that receives the store number and returns the sales forecast.
   
# 2 Data Undastanding
## 2.1 Collect Initial Data

The data was collected on the website kaggle.com, referring to the sales history of 1,115 Rossmann stores, the files are in csv format.

train.csv - historical data including Sales

test.csv - historical data excluding Sales

store.csv - supplemental information about the stores

<a href="https://www.kaggle.com/c/rossmann-store-sales/data" target="_blank">Data Source</a>
 
## 2.2 Data Description

### 2.2.1 Dimensions

Number of rows: 1017209

Number of columns: 18 

### 2.2.2 Missing values

![alt_text](storytelling/img/missing.png)

### 2.2.3 Numerical Attribues

![alt_text](storytelling/img/numerical_attributes.png)

Obs: NaN values have been filled in

### 2.2.4 Categorical Attributes

![alt_text](storytelling/img/categorical_attributes.png)

# 3 Feature Engineering
## 3.1 Mind Map Hypothesis

![alt_text](storytelling/img/mapa_mental_hipotesis.png)

The hypotheses mind map helps to think about what will be explored in the Data Exploration step and what features are not available and need to be created.

### 3.1.1 New features derived

Year: The year of sale

Month: The month of sale 

Day: The day of sale

Week of year: The number of week of the year

Year week: The year and week of sale

Competiton since: The month and year of the competition

Competition month: Competition month number

Promo since: Promotion start date

Promo time week: Number of weeks the promotion took place


# 4 Exploratory Data Analysis
## 4.1 Response Variable
![alt_text](storytelling/img/distribuicao_vendas.png)

The distribution of sales is skewed to the right, which means that sales of some stores are much higher than most stores.

## 4.2 Hyphoteses Results

![alt_text](storytelling/img/sumario_hipoteses.png)

This information can be used in feature importance selection and to validate the empirical knowledge of the business.

# 5 Data Preparation

![alt_text](storytelling/img/modeling_summary.png)

# 6 Machine Learning
## 6.1 Train and Test

Training min date: 2013-01-01

Training max date: 2015-06-18

Test min date: 2015-06-19

Test max date: 2015-07-31
## 6.2 Feature Selection - Boruta

Features selected with Boruta

store, promo, store_type, assortment, competition_distance, competition_open_since_month,  competition_open_since_year, promo2, promo2_since_week, promo2_since_year, competition_time_month, promo_time_week, day_of_week_sin, day_of_week_cos, month_cos, day_sin, day_cos, week_of_year_cos

## 6.3 Models
![alt_text](storytelling/img/models_real_performance.png)

XGBoost Regressor was selected to deploy because the performance is close to Random Forest Regressor and it uses less computational resources.

# 7 Error Interpretation
## 7.1 Business Performance
![alt_text](storytelling/img/mape.png)
![alt_text](storytelling/img/business_performance.png)

Business team can use the prediction and consider the best and worst scenario base no Mean Absolute Percentage Erro - MAPE.

## 7.2 Machine Learning Performance
![alt_text](storytelling/img/predictions_error.png)

Some stores have a higher error rate compared to others; these stores are harder to predict, requiring another modeling strategy. 

# Deployment
[![Alt text](storytelling/img/bot.png)](https://www.youtube.com/watch?v=u14_T0MEuoA)

![IMAGE ALT TEXT](https://www.youtube.com/watch?v=u14_T0MEuoA)