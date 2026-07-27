from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# Replace this with any advisory URL
url = "https://www.ifgtbtreegenie.in/post/pest-and-disease"

# Scrape the page
result = app.scrape_url(
    url,
    formats=["markdown"]
)

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save the markdown
with open("data/pest-and-disease.md", "w", encoding="utf-8") as f:
    f.write(result.markdown)

print("Successfully saved")