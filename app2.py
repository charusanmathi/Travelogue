import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
from io import BytesIO
from fpdf import FPDF
import pandas as pd

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Generate itinerary using Gemini Pro
def generate_gemini_content(destination, num_days, budget, num_people, children_status, preferences):
    prompt = f"""
    You are an expert travel agent. Plan a detailed itinerary for a trip to {destination}. 
    The trip is for {num_days} days, with a budget of {budget} dollars. 
    The trip is for {num_people} people, including {children_status}. 
    The user has the following preferences: {preferences}. 
    The itinerary should be presented in a tabular format with the following columns:
    1. Day Number: Plan for the day
    2. Activities: List of activities
    3. Meals: Suggested meal options
    4. Additional Notes: Any tips or recommendations
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating itinerary: {e}"

# Fetch weather information
def fetch_weather(destination):
    try:
        weather_api_key = os.getenv("WEATHER_API_KEY")
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={destination}&appid={weather_api_key}&units=metric"
        response = requests.get(weather_url).json()
        if response.get("weather"):
            return f"{response['weather'][0]['description'].capitalize()} with a temperature of {response['main']['temp']}°C."
        else:
            return "Weather information unavailable."
    except Exception as e:
        return f"Error fetching weather: {e}"

# Export itinerary to PDF
def export_to_pdf(destination, num_days, itinerary, weather):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.cell(200, 10, txt=f"Travel Itinerary for {destination} ({num_days} days)", ln=True, align="C")
    pdf.ln(10)

    # Add itinerary details
    pdf.multi_cell(0, 10, itinerary)
    pdf.ln(10)

    # Add weather details
    pdf.cell(200, 10, txt="Weather Details:", ln=True)
    pdf.multi_cell(0, 10, weather)

    # Save to BytesIO
    buffer = BytesIO()
    pdf_output = pdf.output(dest="S").encode("latin1")  # Get PDF as string and encode it
    buffer.write(pdf_output)
    buffer.seek(0)  # Reset buffer position to the beginning
    return buffer


# Generate map with destinations
def generate_map(destinations):
    data = [{"lat": dest["lat"], "lon": dest["lon"]} for dest in destinations]
    return pd.DataFrame(data)

# Streamlit App
def app():
    st.set_page_config(page_title="TRAVEL ITENERARY BUILDER", layout="wide")
    st.title("🧳 TRAVELOGUE")
    st.write("Plan your dream trip effortlessly with AI.")

    # User inputs
    st.sidebar.title("Trip Details")
    destinations = st.sidebar.text_area("Enter destinations (one per line):")
    num_days = st.sidebar.slider("Number of days:", 1, 30, 5)
    budget = st.sidebar.slider("Budget ($):", 100, 20000, 1000)
    num_people = st.sidebar.slider("Number of people:", 1, 10, 2)
    include_children = st.sidebar.checkbox("Are children included in the trip?")
    children_status = "children included" if include_children else "no children"
    preferences = st.sidebar.multiselect(
        "Select your preferences:",
        ["Adventure", "Relaxation", "Food & Drink", "Cultural Experiences", "Shopping"]
    )

    # Process destinations
    destination_list = [dest.strip() for dest in destinations.split("\n") if dest.strip()]

    # Generate itinerary
    if st.button("Generate Itinerary"):
        if not destination_list:
            st.error("Please enter at least one destination.")
        else:
            with st.spinner("Building your itinerary..."):
                itinerary = ""
                all_weather = []

                for destination in destination_list:
                    dest_itinerary = generate_gemini_content(
                        destination, num_days, budget, num_people, children_status, preferences
                    )
                    dest_weather = fetch_weather(destination)
                    itinerary += f"## Itinerary for {destination}:\n" + dest_itinerary + "\n\n"
                    all_weather.append(f"{destination}: {dest_weather}")

                all_weather = "\n".join(all_weather)

                # Display results
                st.markdown("## ✈️ Your Itinerary:")
                st.write(itinerary)
                st.markdown("## ☀️ Destination Weather:")
                st.write(all_weather)

                # Map integration
                destination_data = [{"lat": 37.7749, "lon": -122.4194} for _ in destination_list]  # Example: Replace with real lat/lon
                map_df = generate_map(destination_data)
                st.map(map_df)

                # Export to PDF
                pdf = export_to_pdf(" & ".join(destination_list), num_days, itinerary, all_weather)
                st.download_button(
                    "Download Itinerary as PDF",
                    data=pdf,
                    file_name="itinerary.pdf",
                    mime="application/pdf",
                )

# Run the app
if __name__ == "__main__":
    app()
