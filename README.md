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

# Data Preparation
## Rescaling

Min max scaler was applied to competitio distance and competition time month

Robust scaler was applied to promo time week and year. 

This tecniques was applied to avoid bias. 

## Transformation
## Encoding
## Response variable transformation
## Nature Transformation


## Feature Selection
### Boruta
# Machine Learning Modeling

# Evaluation

# Deployment
