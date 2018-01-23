# Watching the Watchers: Forecasting Calculator

## Description
The idea for this app is to measure how well the OpenWeatherMap API forecasts the weather. I'll start by charting out the API's 5-day prediction for temperature, humidity, etc., and storing that info in the database (by day, and by how early the prediction is made). Then, I'll be able to check the weather on a given day (using the same API), and compare it to the API's earlier predictions. (A super stretch goal will be to implement some machine learning to generate a better predictor.)

## Built With
- Django
- Python
- MySQL
- Django Graphos
- Open Weather Map API
