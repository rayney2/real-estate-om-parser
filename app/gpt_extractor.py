import os
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv

load_dotenv()

def set_api_key_once(api_key: str):
    with open(".env", "w") as f:
        f.write(f"OPENAI_API_KEY={api_key.strip()}")

def init_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        key = input("🔐 Enter your OpenAI API key: ").strip()
        set_api_key_once(key)
        OpenAI.api_key = key
    else:
        OpenAI.api_key = key

def build_underwriting_prompt(text):
    return f"""
You are a real estate underwriting assistant. From the offering memorandum text below, extract the following fields and return a valid JSON object. Use these exact keys:

🔹 PROPERTY INFO
- Property Name
- Year Built
- Address
- Lot Size
- Building Size
- Ask Price
- Offer Price
- Total Apartment Units
- Total Current Rental Units
- Total Parking Spaces

🔹 VALUATION & INCOME
- Price per Unit
- Price per Square Foot
- Cap Rate
- Gross Scheduled Rent
- Effective Gross Income
- Loss to Lease (amount or %)
- Vacancy Rate (amount or %)
- Other Income
- Net Operating Income (NOI)

🔹 EXPENSES
- Total Expenses
- Management Fee
- Repairs and Maintenance
- Utilities (Water, Electric, Gas)
- Insurance
- Property Taxes
- Trash
- Capital Reserves
- Other Expenses

🔹 RENT ROLL & UNIT MIX
- Rent Roll (unit type, # units, As-is rent, Projected rent)

Text:
\"\"\"
{text}
\"\"\"

Only return a valid JSON object with the fields you can extract. Do not include any explanations.
"""

client = OpenAI()

def extract_underwriting_json(text):
    try:
        chat = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful real estate analyst."},
                {"role": "user", "content": build_underwriting_prompt(text)}
            ],
            temperature=0.1
        )
        return chat.choices[0].message.content
    except RateLimitError as e:
        print("❌ You have exceeded your current OpenAI quota.")
        print("👉 Visit https://platform.openai.com/account/usage to check your usage.")
        return "{}"