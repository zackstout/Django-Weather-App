# Watching the Watchers: Forecasting Calculator

## Description
The idea for this app is to measure how well the OpenWeatherMap API forecasts the weather. I'll start by charting out the API's 5-day prediction for temperature, humidity, etc., and storing that info in the database (by day, and by how early the prediction is made). Then, I'll be able to check the weather on a given day (using the same API), and compare it to the API's earlier predictions. (A super stretch goal will be to implement some machine learning to generate a better predictor.)

## Built With
- Django
- Python
- MySQL
- Django Graphos
- Open Weather Map API



## Stretch Goals:
- Grab historical data and predict temp based on hum, hum based on temp, etc. See where the correlations are (compare with correlations in current predictions);
- Determine which predictions are more reliable (e.g. pressure vs windspeed);
- Think of a way to visualize accuracy of predictions from 5 days out vs 3 days out etc.;
- Seek trends in historical data, over say the last forty years (probably will get best results by choosing a single day, or month averaged out);
- Let user input which city to view;
- Could weight 5-day predictions lower than 1-day predictions in order to determine overall success rate of the predictor function.
