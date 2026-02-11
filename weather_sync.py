import os
import json
from google.cloud import bigquery
from genai_client import GenAIClient
from mitigation_agent import MitigationAgent

SYNC_PROMPT = """
You are a Weather Sync Agent. Your task is to link proposed disaster mitigation steps with current weather forecasts.

Mitigation Steps:
{mitigation_report}

Precipitation Forecast (next 24h): {precip} inches
Wind Speed Forecast: {wind} mph

Generate a "Disaster Resilience Summary" that highlights which mitigation steps are most urgent given the weather forecast.
Concise Response (2-3 sentences):
"""

class WeatherSync:
    def __init__(self):
        self.ai_client = GenAIClient()
        self.mitigation_agent = MitigationAgent()
        # BigQuery client would be initialized here in a real environment
        # self.bq_client = bigquery.Client()

    def get_resilience_summary(self, lat=37.5, lng=-77.4): # Default to Richmond, VA
        """
        Fetches mitigation report and weather forecast to create a synced summary.
        """
        # 1. Get mitigation report
        mitigation_report = self.mitigation_agent.generate_report()
        
        # 2. Mock weather data (simulating BigQuery/WeatherNext fetch)
        # In a real scenario, we'd use get_weather_for_location logic from bgr-app.py
        forecast_precip = 2.5 # Simulated heavy rain
        forecast_wind = 15.0  # Simulated moderate wind
        
        # 3. Synchronize using AI
        prompt = SYNC_PROMPT.format(
            mitigation_report=mitigation_report,
            precip=forecast_precip,
            wind=forecast_wind
        )
        
        return self.ai_client.generate_text(prompt)

if __name__ == "__main__":
    # Test Sync
    sync = WeatherSync()
    summary = sync.get_resilience_summary()
    print("\nDisaster Resilience Summary:")
    print(summary)
