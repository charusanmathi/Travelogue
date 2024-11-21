# Travelogue
🧳 TRAVELOGUE - Travel Itinerary Builder  Plan your dream trip effortlessly with AI-powered recommendations, real-time weather updates, and custom itineraries!


🚀 Features

Custom Itineraries: Generates detailed day-by-day plans tailored to your destination, preferences, and budget.
Weather Updates: Fetches live weather information for each destination.
Interactive Maps: Displays your trip locations on an interactive map.
Downloadable PDFs: Exports your itinerary as a professionally formatted PDF.
🛠️ Tech Stack

Python
- Streamlit
- Google Gemini Pro API
- OpenWeather API
- FPDF for PDF generation

📦 Installation

* Clone the Repository:
git clone https://github.com/charusanamthi/travelogue-itinerary-builder.git
cd travelogue-itinerary-builder

* Install Dependencies:
pip install -r requirements.txt

* Set Up API Keys:
Create a .env file in the project root.
Add your API keys for Google Gemini and OpenWeather:
GOOGLE_API_KEY=your_google_gemini_key


* Run the App:
streamlit run app.py


📄 How It Works

- Enter your destination(s) and trip details (number of days, budget, number of people, etc.).
- Select your travel preferences (adventure, food, culture, etc.).
- Click "Generate Itinerary" to create your plan.
- View your trip details, weather updates, and an interactive map.
- Download your personalized itinerary as a PDF
