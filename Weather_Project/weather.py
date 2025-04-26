import requests
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import plugins

# ✅ Replace with your OpenWeatherMap API key
API_KEY = '1503a35a3115fdf5e65eed2480a1b937'

# ✅ List of 50 cities
cities = [
    "Chennai", "Delhi", "Mumbai", "Bangalore", "Hyderabad",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Surat",
    "Lucknow", "Bhopal", "Nagpur", "Patna", "Indore",
    "Coimbatore", "Thiruvananthapuram", "Visakhapatnam", "Vijayawada", "Amritsar",
    "Rajkot", "Varanasi", "Raipur", "Jodhpur", "Guwahati",
    "Noida", "Ludhiana", "Agra", "Nashik", "Madurai",
    "Jamshedpur", "Mysore", "Tiruchirappalli", "Udaipur", "Dehradun",
    "Ranchi", "Gwalior", "Jalandhar", "Meerut", "Hubli",
    "Kolhapur", "Mangalore", "Kanpur", "Asansol", "Dhanbad",
    "Allahabad", "Howrah", "Vellore", "Warangal", "Bilaspur"
]

# ✅ Prepare a list to hold all the data
weather_data = []

# ✅ Fetch weather data for each city
print("📡 Fetching weather data for cities...")
for city in cities:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_info = {
            'City': city,
            'Temperature': data['main']['temp'],
            'Humidity': data['main']['humidity'],
            'Weather': data['weather'][0]['description'],
            'Lat': data['coord']['lat'],  # Latitude
            'Lon': data['coord']['lon']   # Longitude
        }
        weather_data.append(weather_info)
    else:
        print(f"❌ Failed to fetch data for {city}")

# ✅ Convert list to DataFrame
df = pd.DataFrame(weather_data)

# ✅ Save to CSV
df.to_csv('data.csv', index=False)
print("✅ Weather data saved to 'data.csv'.")

# ---------- 📈 Elbow Method to Choose Optimal k ----------
X = df[['Temperature', 'Humidity']].dropna()
wcss = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Plot the Elbow Graph
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--', color='blue')
plt.title('📈 Elbow Method For Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS')
plt.grid(True)
plt.tight_layout()
plt.savefig("elbow_method.png")
plt.show()

# ---------- 🔵 K-Means Clustering ----------
# ✅ Apply K-Means with chosen k (example: 3)
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)

# ✅ Show the clustered data
print("\n🔍 Clustered Data Preview:")
print(df)

# ---------- 🎨 Graphs Section ----------
# ✅ Set Seaborn styling
sns.set_style('darkgrid')

# 1️⃣ Bar Graph: Temperature by City
plt.figure(figsize=(14, 6))
sns.barplot(x='City', y='Temperature', data=df)
plt.xticks(rotation=90)
plt.title('🌡️ Temperature of Cities')
plt.xlabel('City')
plt.ylabel('Temperature (°C)')
plt.tight_layout()
plt.savefig("temperature_bar_chart.png")
plt.show()

# 2️⃣ Pie Chart: Weather Condition Distribution
plt.figure(figsize=(6, 6))
weather_counts = df['Weather'].value_counts()
plt.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('🌥️ Weather Condition Distribution')
plt.axis('equal')
plt.savefig("weather_pie_chart.png")
plt.show()

# 3️⃣ Scatter Plot: Temperature vs Humidity (Clustering)
plt.figure(figsize=(8, 6))
plt.scatter(df['Temperature'], df['Humidity'], c=df['Cluster'], cmap='viridis', s=100)
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.title('📊 K-Means Clustering of Weather Data')
plt.grid(True)
plt.savefig("clustering_scatter_plot.png")
plt.show()

# 4️⃣ Heatmap: Temperature by City
plt.figure(figsize=(14, 1.5))
temp_data = df.pivot_table(index='City', values='Temperature')
sns.heatmap(temp_data.T, cmap='coolwarm', annot=True, fmt=".1f", cbar=True,
            annot_kws={"size": 12, "weight": "bold", "color": "black"})  # Adjust the font size, weight, and color
plt.title('🔥 Heatmap of Temperature by City', fontsize=16, weight='bold')  # Title font adjustment
plt.yticks(rotation=0, fontsize=12)  # Y-ticks font size adjustment
plt.xticks(fontsize=12)  # X-ticks font size adjustment
plt.tight_layout()
plt.savefig("temperature_heatmap.png")
plt.show()

# 5️⃣ Heatmap: Humidity by City
plt.figure(figsize=(14, 1.5))
humidity_data = df.pivot_table(index='City', values='Humidity')
sns.heatmap(humidity_data.T, cmap='Blues', annot=True, fmt=".0f", cbar=True,
            annot_kws={"size": 12, "weight": "bold", "color": "black"})  # Adjust the font size, weight, and color
plt.title('💧 Heatmap of Humidity by City', fontsize=16, weight='bold')  # Title font adjustment
plt.yticks(rotation=0, fontsize=12)  # Y-ticks font size adjustment
plt.xticks(fontsize=12)  # X-ticks font size adjustment
plt.tight_layout()
plt.savefig("humidity_heatmap.png")
plt.show()

# ---------- 🌍 Map-based Visualization with Folium ----------
# Create a base map centered in India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Add markers for each city with a popup containing weather info
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=8,
        color='blue' if row['Cluster'] == 0 else ('green' if row['Cluster'] == 1 else 'red'),
        fill=True,
        fill_color='blue' if row['Cluster'] == 0 else ('green' if row['Cluster'] == 1 else 'red'),
        fill_opacity=0.6,
        popup=f"<strong>{row['City']}</strong><br>Temp: {row['Temperature']}°C<br>Humidity: {row['Humidity']}%<br>Weather: {row['Weather']}"
    ).add_to(m)

# Save the map to an HTML file
m.save("weather_map.html")
print("✅ Weather map saved to 'weather_map.html'.")

# Open the map directly in a browser (optional)
import webbrowser
webbrowser.open("weather_map.html")
