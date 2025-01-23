# YouTube Analytics Dashboard

## Overview

This project is a **YouTube Analytics Dashboard** developed using **Streamlit**, **Plotly**, and **Pandas** to provide an insightful analysis of YouTube videos. Users can explore and visualize both **aggregate** and **individual video metrics** such as views, likes, engagement ratios, and more. It is a helpful tool for content creators to monitor and optimize their YouTube channels.
### Link for App: https://youtube-analytics-dashboard-wqd4lzwcyuzsvdtrgb8kp8.streamlit.app/

---

## Features

- **Aggregate Metrics**: View overall channel statistics like views, likes, shares, RPM, average view duration, and more.
- **Individual Video Analysis**: Delve into detailed metrics of a specific video, including its performance over time and engagement from different regions.
- **Interactive Visualizations**: Visualize data through interactive charts and graphs powered by Plotly.
- **Data Caching**: Optimized data loading and processing using Streamlit’s caching system.
- **Responsive Design**: The app is designed for wide-screen use, making it easy to navigate and analyze large datasets.

---

## Key Metrics

- **Views**: Total number of views a video has accumulated.
- **Likes/Dislikes**: User feedback in the form of likes and dislikes.
- **Shares**: Number of times the video has been shared.
- **Subscribers**: Net change in the number of subscribers due to the video.
- **Engagement Ratio**: A ratio that accounts for comments, shares, dislikes, and likes in relation to views.
- **RPM/CPM**: Revenue per thousand views (RPM) and cost per thousand impressions (CPM).
- **Average % Viewed**: The average percentage of the video that viewers watch.
- **Average View Duration**: The average time viewers spend watching the video.

---

## Setup & Installation

### Prerequisites
- **Python 3.8+**  
- **Streamlit**  
- **Pandas**  
- **Plotly**  
- **NumPy**

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/YouTube-Analytics-Dashboard.git
   cd YouTube-Analytics-Dashboard
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Download or prepare the necessary CSV data files:
   - `Aggregated_Metrics_By_Video.csv`
   - `Aggregated_Metrics_By_Country_And_Subscriber_Status.csv`
   - `Video_Performance_Over_Time.csv`

4. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## Usage

Upon running the application, users will have the option to choose between two modes:

1. **Aggregate Metrics**:  
   Displays key metrics for the entire channel, including median values over the past 6 or 12 months, with the ability to view changes in those metrics.

2. **Individual Video Analysis**:  
   Allows users to select an individual video and view its performance over time, including geographic engagement, cumulative views, and percentile-based comparisons.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

Developed by [Muhammad Rasoul Sahibzadah](http://www.linkedin.com/in/muhammad-rasoul-sahibzadah-b97a47218/). Feel free to reach out via email at [rasoul.sahibbzadah@auaf.edu.af](mailto:rasoul.sahibbzadah@auaf.edu.af).

--- 

This README should help users understand the setup, features, and usage of your YouTube Analytics Dashboard.
