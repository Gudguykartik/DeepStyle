import os
import datetime
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_current_season():
    """Determine current season based on month"""
    month = datetime.datetime.now().month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"

def get_weather():
    """Get current weather (mock function for demo)"""
    season = get_current_season()
    weather_data = {
        'winter': {'temperature': 10, 'condition': 'cold'},
        'spring': {'temperature': 20, 'condition': 'mild'},
        'summer': {'temperature': 30, 'condition': 'sunny'},
        'autumn': {'temperature': 15, 'condition': 'mild'}
    }
    current = weather_data.get(season, weather_data['spring'])
    return {
        'temperature': current['temperature'],
        'condition': current['condition'],
        'time_of_day': datetime.datetime.now().hour
    }

def get_day_context():
    """Get context about the current day"""
    current_time = datetime.datetime.now()
    hour = current_time.hour
    
    if 5 <= hour < 12:
        time_of_day = "morning"
    elif 12 <= hour < 17:
        time_of_day = "afternoon"
    elif 17 <= hour < 21:
        time_of_day = "evening"
    else:
        time_of_day = "night"
    
    weather = get_weather()
    
    return {
        'time_of_day': time_of_day,
        'temperature': weather['temperature'],
        'weather': weather['condition']
    }

def load_and_prepare_data():
    """Load the fashion dataset"""
    dataset_path = os.path.join(os.path.dirname(__file__), 'fashion_dataset_full.pkl')
    return pd.read_pickle(dataset_path)

def get_outfit_recommendations(query, gender, data):
    """Get outfit recommendations using Gemini API"""
    context = get_day_context()
    season = get_current_season()
    
    # Determine if this is a casual or formal request
    is_casual = 'casual' in query.lower()
    is_party = 'party' in query.lower()
    
    if is_casual:
        style_prompt = """You are a fashion expert specializing in modern casual wear. Create a stylish yet comfortable outfit that's perfect for everyday activities while maintaining a put-together look.
        
        Focus on:
        - Comfort and versatility
        - Modern casual style
        - Easy-to-wear combinations
        - Seasonal appropriateness
        - Smart layering options"""
    elif is_party:
        style_prompt = """You are a luxury fashion stylist specializing in party and formal wear. Create an elegant and fashionable party outfit that's both stylish and appropriate for the season.
        
        Focus on:
        - Statement pieces that stand out
        - Luxurious fabrics and textures
        - Appropriate level of formality
        - Seasonal appropriateness
        - Accessories that elevate the look"""
    else:
        style_prompt = """You are a fashion expert. Create a versatile outfit that balances style with practicality.
        
        Focus on:
        - Current fashion trends
        - Versatile pieces
        - Seasonal appropriateness
        - Comfortable yet stylish options
        - Easy-to-style combinations"""
    
    prompt = f"""{style_prompt}

    Generate a detailed outfit recommendation based on:
    - Query: {query}
    - Gender: {gender}
    - Season: {season}
    - Time: {context['time_of_day']}
    - Weather: {context['weather']} ({context['temperature']}°C)

    Provide a response with:
    1. A detailed description of the complete outfit and how the pieces complement each other
    2. 3 key pieces that form the core of the outfit, including specific styles, materials, and how to wear them

    Format the response as a JSON object with:
    {{
        "description": "outfit description",
        "items": [
            {{
                "name": "item name",
                "description": "detailed item description including material, fit, and styling tips",
                "color": "color name",
                "color_hex": "hex code",
                "text_color": "contrasting hex code for text"
            }}
        ]
    }}
    """
    
    response = model.generate_content(prompt)
    try:
        result = json.loads(response.text)
        return result
    except:
        # Fallback response based on request type
        if is_casual:
            return {
                "description": "A comfortable and stylish casual outfit perfect for everyday wear.",
                "items": [
                    {
                        "name": "Premium Cotton T-Shirt",
                        "description": "Soft, breathable cotton in a relaxed fit",
                        "color": "Heather Gray",
                        "color_hex": "D3D3D3",
                        "text_color": "000000"
                    },
                    {
                        "name": "Slim Fit Jeans",
                        "description": "Classic dark wash denim with stretch",
                        "color": "Indigo",
                        "color_hex": "4B0082",
                        "text_color": "ffffff"
                    },
                    {
                        "name": "White Sneakers",
                        "description": "Clean, minimalist design for versatility",
                        "color": "White",
                        "color_hex": "FFFFFF",
                        "text_color": "000000"
                    }
                ]
            }
        elif is_party:
            return {
                "description": "For a sophisticated party look, I recommend a carefully curated outfit that combines elegance with modern style.",
                "items": [
                    {
                        "name": "Designer Evening Wear",
                        "description": "A perfectly tailored piece in a luxurious fabric",
                        "color": "Midnight Blue",
                        "color_hex": "191970",
                        "text_color": "ffffff"
                    },
                    {
                        "name": "Statement Accessories",
                        "description": "Elegant accessories to complete the look",
                        "color": "Gold",
                        "color_hex": "FFD700",
                        "text_color": "000000"
                    },
                    {
                        "name": "Designer Footwear",
                        "description": "Sophisticated footwear that complements the outfit",
                        "color": "Black",
                        "color_hex": "000000",
                        "text_color": "ffffff"
                    }
                ]
            }
        else:
            return {
                "description": "A versatile outfit that combines style with comfort.",
                "items": [
                    {
                        "name": "Cotton Button-Down Shirt",
                        "description": "Classic fit in breathable cotton",
                        "color": "Light Blue",
                        "color_hex": "ADD8E6",
                        "text_color": "000000"
                    },
                    {
                        "name": "Chino Pants",
                        "description": "Tailored fit in stretch cotton",
                        "color": "Khaki",
                        "color_hex": "F0E68C",
                        "text_color": "000000"
                    },
                    {
                        "name": "Leather Loafers",
                        "description": "Comfortable slip-on style",
                        "color": "Brown",
                        "color_hex": "8B4513",
                        "text_color": "ffffff"
                    }
                ]
            }

def get_daily_outfit(gender, data):
    """Generate a daily outfit recommendation"""
    context = get_day_context()
    season = get_current_season()
    
    prompt = f"""As a fashion expert, recommend an outfit for:
    - Gender: {gender}
    - Season: {season}
    - Time: {context['time_of_day']}
    - Weather: {context['weather']} ({context['temperature']}°C)

    Provide a concise response with:
    1. A brief description why this outfit works for today
    2. 3 specific items that work well together

    Format the response as a JSON object with:
    {{
        "description": "outfit description",
        "items": [
            {{"name": "item name", "description": "item description", "color": "color name", "color_hex": "hex code"}}
        ]
    }}
    """
    
    response = model.generate_content(prompt)
    try:
        result = json.loads(response.text)
        return result
    except:
        # Fallback response if API fails
        return {
            "description": f"A weather-appropriate outfit for {context['time_of_day']} in {season}.",
            "items": [
                {"name": "Crew Neck Sweater", "description": "Warm wool blend sweater", "color": "Gray", "color_hex": "808080"},
                {"name": "Slim Jeans", "description": "Classic fit denim", "color": "Dark Blue", "color_hex": "00008b"},
                {"name": "Ankle Boots", "description": "Leather boots", "color": "Black", "color_hex": "000000"}
            ]
        }

def get_outfit_approval(items):
    """Get AI feedback on the outfit combination"""
    prompt = f"""As a fashion expert, evaluate this outfit combination:
    {json.dumps(items, indent=2)}

    Provide a concise response with:
    1. Yes/No if the combination works
    2. A brief reason why (1 sentence)

    Format the response as a JSON object:
    {{
        "response": "Yes/No: reason"
    }}
    """
    
    response = model.generate_content(prompt)
    try:
        result = json.loads(response.text)
        return result
    except:
        # Fallback response if API fails
        return {
            "response": "Yes: The items create a cohesive and balanced outfit."
        }

def main():
    """Main function to run the fashion assistant"""
    print("Welcome to your AI Fashion Assistant!")
    
    # Load the dataset
    data = load_and_prepare_data()
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Get outfit recommendation")
        print("2. Get daily outfit")
        print("3. Exit")
        
        choice = input("Choose (1-3): ").strip()
        
        if choice == "1":
            query = input("Enter your query: ").strip()
            gender = input("Enter your gender (Men/Women): ").strip()
            result = get_outfit_recommendations(query, gender, data)
            print("\nOutfit Recommendation:")
            print(result["description"])
            for item in result["items"]:
                print(f"- {item['name']}: {item['description']}, Color: {item['color']}")
        
        elif choice == "2":
            gender = input("Enter your gender (Men/Women): ").strip()
            result = get_daily_outfit(gender, data)
            print("\nDaily Outfit Recommendation:")
            print(result["description"])
            for item in result["items"]:
                print(f"- {item['name']}: {item['description']}, Color: {item['color']}")
        
        elif choice == "3":
            print("Thank you for using AI Fashion Assistant!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
