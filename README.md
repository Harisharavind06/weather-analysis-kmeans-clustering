# weather-analysis-kmeans-clustering
This project uses real-time weather data and K-Means clustering to group temperature patterns. Built with Python, it helps identify trends in weather for insights in forecasting and climate behavior.

# Weather Analysis using K-Means Clustering

This project uses K-Means Clustering to analyze real-time weather data and group cities based on temperature similarities. It integrates weather APIs, processes data, and visualizes clustered results to help understand weather trends and patterns.

## 📌 Objective

To collect real-time weather data of various cities and apply K-Means Clustering to identify hidden patterns or groups based on temperature, aiding in weather analysis and forecasting.

## 🧠 Key Features

- Real-time weather data fetching using OpenWeatherMap API
- Data cleaning and normalization
- Clustering using K-Means (unsupervised learning)
- Interactive visualizations using matplotlib
- CSV export of city data with cluster labels

## 📊 Technologies Used

- Python 3
- Requests (for API calls)
- pandas (for data handling)
- scikit-learn (for clustering)
- matplotlib (for visualization)

## 📁 Project Structure


## 🔄 How It Works

1. Takes a list of cities and fetches their current temperature using the OpenWeatherMap API.
2. Preprocesses and normalizes the temperature data.
3. Applies K-Means clustering to group cities based on similarity.
4. Plots the clusters for easy understanding.
5. Saves the output to `clustered_output.csv`.

## 📌 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-analysis-kmeans-clustering.git
   cd weather-analysis-kmeans-clustering

Install the required packages:

bash
Copy
Edit
pip install requests pandas scikit-learn matplotlib
Replace the API key in weather_kmeans.py with your OpenWeatherMap API key.

Run the script:

bash
Copy
Edit
python weather_kmeans.py

📈 Example Output
A scatter plot showing clusters of cities

clustered_output.csv file with city-wise cluster IDs

📚 References
OpenWeatherMap API

scikit-learn documentation

K-Means Clustering algorithm

<img src="https://t.bkit.co/w_6810c2370e27e.gif" />
