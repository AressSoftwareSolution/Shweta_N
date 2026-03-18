import json
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)
import streamlit as st
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


## RAG
import pdfplumber

pdf_path = '/workspaces/Travel_Agent/Aress_Task (9).pdf'
pdf_text = ''

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        pdf_text += page.extract_text() + '\n'

import re

cleaned_pdf_text = pdf_text.replace('\n', ' ').strip()    ## remove next line
cleaned_pdf_text = re.sub(r'\s+', ' ', cleaned_pdf_text).lower()  ## remove extra space and lower case the text


import string

# Remove punctuation
cleaned_pdf_text = cleaned_pdf_text.translate(str.maketrans('', '', string.punctuation))

# Tokenize the cleaned text
tokens = nltk.word_tokenize(cleaned_pdf_text)

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

filtered_tokens = [word for word in tokens if word not in stop_words]  ## remove stop words

final_processed_text = ' '.join(filtered_tokens)


from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    add_start_index=True,
)
text_chunks = text_splitter.split_text(final_processed_text)
print(f"Number of text chunks: {len(text_chunks)}")
print(f"First chunk:\n{text_chunks[0]}")


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

document_chunks = [Document(page_content=t) for t in text_chunks]

db = Chroma.from_documents(document_chunks, embeddings)

retriever = db.as_retriever()
print("Chroma vector store created successfully.")

def trip_understanding_agent(user_query):
    """
    Extracts travel details (destination, dates/duration, preferences, travel style)
    from a user query using the Groq client and returns them in a structured dictionary.
    """
    system_prompt = (
        "You are a 'Trip Understanding Agent' in a multi-agent travel planning system.\n"
        "Your task is to extract key travel information from the user's request and provide it in a strict JSON format.\n\n"
        "Extract the following information:\n"
        "- **Destination**: The city, country, or region the user wants to visit.\n"
        "- **Dates and Duration**: Specific dates or a duration (e.g., '2 weeks in August', 'from Jan 1 to Jan 15').\n"
        "- **Preferences**: Any specific interests, activities, or types of experiences (e.g., 'luxury accommodation', 'adventure activities', 'cultural experiences', 'food tour').\n"
        "- **Travel Style**: The nature of the trip (e.g., 'solo', 'family trip', 'romantic getaway', 'business travel', 'backpacking').\n\n"
        "You MUST output ONLY the JSON object. Do not include any additional text, explanations, or formatting outside of the JSON.\n"
        "The JSON object should have the following keys: 'destination', 'dates_duration', 'preferences', 'travel_style'.\n"
        "If a piece of information is not explicitly mentioned, provide an empty string for that key."
    )

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            temperature=0.2  # Low temperature for precise JSON output
        )

        response_content = response.choices[0].message.content
        # Attempt to parse the content as JSON
        extracted_data = json.loads(response_content)
        return extracted_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from model response: {e}")
        print(f"Raw response content: {response_content}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

print("The `trip_understanding_agent` function has been defined.")

def retrieve_chunks(query, retriever, top_k=4):
    results = retriever.invoke(query)
    return results[:top_k]

def build_rag_prompt(Story_Output, retrieved_docs):
    """
    Builds RAG prompt for LLM using retrieved chunks.
    """
    context_text = "\n\n".join([f"Chunk {i+1}: {doc.page_content}"
                                for i, doc in enumerate(retrieved_docs)])

    prompt = f"""
You are a Travel Information Retrieval Agent in a multi-agent travel planning system.

Your primary responsibility is to provide accurate, up-to-date travel information using the retrieved context from the knowledge base.

The knowledge base contains information related to:
- Visa requirements
- Travel safety guidelines
- Packing recommendations
- Local travel advice
- Entry restrictions
- Cultural guidelines

You MUST follow these rules:

1. Use the retrieved context as the primary source of information.
2. If the context contains the answer, generate a clear and helpful response.
3. If the context is insufficient, say:
   "The available travel knowledge base does not contain enough information to answer this query."

4. Do NOT hallucinate or invent visa rules, safety policies, or government regulations.

5. Structure your responses clearly under relevant sections when applicable:
   - Visa Information
   - Travel Safety
   - Packing Advice
   - Local Tips

6. Be concise but informative. Prioritize actionable travel guidance.

7. Assume the user is a traveler asking practical questions such as:
   - "Do I need a visa for Japan?"
   - "Is it safe to travel to Paris?"
   - "What should I pack for Iceland in winter?"

8. If the query is outside your responsibility (for example: flight booking, hotel booking, itinerary generation), respond with:

   "This request should be handled by another travel planning agent."

9. Always prioritize traveler safety and official travel guidelines.

10. When possible, include helpful suggestions such as documents to carry, emergency numbers, or seasonal packing tips.

Your goal is to assist travelers with reliable travel preparation information.

### CONTEXT:
{context_text}

### Trip Information
{Story_Output}

### RESPONSE:
"""
    return prompt
def rag_query(user_query):

    # Retrieve relevant chunks
    retrieved_docs = retrieve_chunks(user_query, retriever)

    # Build prompt
    final_prompt = build_rag_prompt(user_query, retrieved_docs)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a RAG-based assistant designed to help with travel preparation."},
            {"role": "user", "content": final_prompt},
        ],
        temperature=0.3
    )

    try:
        return response.choices[0].message.content
    except Exception as e:
        print("ERROR extracting content:", e)
        return "RAG agent failed to respond."

## MCP:
def get_destination_costs(destination):
    """
    MCP Tool: Fetch estimated daily costs for a destination.
    """
    cost_database = {

    "Paris": {
        "currency": "INR",
        "hotel_per_day": 15000,
        "food_per_day": 5000,
        "transport_per_day": 2000,
        "sightseeing_per_day": 4000,
        "flight_round_trip": 175000,
        "visa_cost": 8000
    },

    "Orlando": {
        "currency": "INR",
        "hotel_per_day": 12000,
        "food_per_day": 4500,
        "transport_per_day": 2500,
        "sightseeing_per_day": 10000,
        "flight_round_trip": 70000,
        "visa_cost": 15000
    },

    "Southeast Asia": {
        "currency": "INR",
        "hotel_per_day": 5000,
        "food_per_day": 2000,
        "transport_per_day": 1200,
        "sightseeing_per_day": 2500,
        "flight_round_trip": 40000,
        "visa_cost": 3500
    },

    "New York": {
        "currency": "INR",
        "hotel_per_day": 18000,
        "food_per_day": 6000,
        "transport_per_day": 3000,
        "sightseeing_per_day": 5000,
        "flight_round_trip": 80000,
        "visa_cost": 15000
    },

    "Japan": {
        "currency": "INR",
        "hotel_per_day": 13000,
        "food_per_day": 5000,
        "transport_per_day": 2500,
        "sightseeing_per_day": 4500,
        "flight_round_trip": 65000,
        "visa_cost": 4000
    },

    "Bali": {
        "currency": "INR",
        "hotel_per_day": 7000,
        "food_per_day": 3000,
        "transport_per_day": 1500,
        "sightseeing_per_day": 3500,
        "flight_round_trip": 45000,
        "visa_cost": 3000
    },

    "Rome": {
        "currency": "INR",
        "hotel_per_day": 14000,
        "food_per_day": 4500,
        "transport_per_day": 2000,
        "sightseeing_per_day": 4000,
        "flight_round_trip": 70000,
        "visa_cost": 8000
    },

    "Malaysia": {
        "currency": "INR",
        "hotel_per_day": 6000,
        "food_per_day": 2500,
        "transport_per_day": 1500,
        "sightseeing_per_day": 3000,
        "flight_round_trip": 30000,
        "visa_cost": 2500
    },

    "USA": {
        "currency": "INR",
        "hotel_per_day": 12500,
        "food_per_day": 5000,
        "transport_per_day": 2000,
        "sightseeing_per_day": 3000,
        "flight_round_trip": 100000,
        "visa_cost": 16500
    },
}


    return cost_database.get(destination, None)

import re

def extract_duration(duration_text):
    match = re.search(r'(\d+)', duration_text)
    
    if match:
        return int(match.group(1))
    
    return 5   # default fallback

def calculate_trip_budget(info):

    destination = info.get("destination", "Unknown Destination")

    duration_text = info.get("dates_duration")

    if duration_text:
        duration = extract_duration(duration_text)
    else:
        duration = 1   # default if missing

    costs = get_destination_costs(destination)

    if costs is None:
        return "Destination cost data not available."

    daily_cost = (
        costs["hotel_per_day"] +
        costs["food_per_day"] +
        costs["transport_per_day"] +
        costs["sightseeing_per_day"]
    )

    total_cost = daily_cost * duration

    flight_cost = costs['flight_round_trip']
    visa_cost = costs['visa_cost']

    total_trip_cost = total_cost + flight_cost + visa_cost

    return {
        "destination": destination,
        "duration_days": duration,
        "daily_cost": daily_cost,
        "stay_cost": total_cost,
        "flight_cost": flight_cost,
        "visa_cost": visa_cost,
        "total_estimated_cost": total_trip_cost
    }


def Budget_agent(user_query):

    if isinstance(user_query, str):
        user_query = json.loads(user_query)
        

    budget_data = calculate_trip_budget(user_query)

    system_prompt = """
You are the Budget Agent of a Travel Multi-Agent System.

Use the provided cost estimates to produce a structured budget plan.

Always include:
- Flight cost
- Accommodation
- Food
- Local transport
- Sightseeing
- Visa cost
- Total trip cost

Traveler is from India so prices must be in INR.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(budget_data)}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


import json

# Placeholder data structure for attractions in various destinations
ATTRACTIONS_DATA = {
    "Paris": [
        {"name": "Eiffel Tower", "type": "landmark", "suitability": ["romantic", "family", "cultural"]},
        {"name": "Louvre Museum", "type": "cultural", "suitability": ["cultural", "family"]},
        {"name": "Notre Dame Cathedral", "type": "cultural", "suitability": ["cultural", "romantic"]},
        {"name": "Montmartre & Sacré-Cœur Basilica", "type": "cultural", "suitability": ["romantic", "cultural"]},
        {"name": "Seine River Cruise", "type": "leisure", "suitability": ["romantic", "family", "relaxing"]},
        {"name": "Disneyland Paris", "type": "adventure", "suitability": ["family"]},
        {"name": "Champs-Élysées", "type": "shopping", "suitability": ["leisure", "romantic"]},
        {"name": "Palace of Versailles", "type": "historical", "suitability": ["cultural", "romantic"]},
        {"name": "Musée d'Orsay", "type": "cultural", "suitability": ["cultural"]}
    ],
    "Orlando": [
        {"name": "Walt Disney World Resort", "type": "theme park", "suitability": ["family", "adventure"]},
        {"name": "Universal Studios Florida", "type": "theme park", "suitability": ["family", "adventure"]},
        {"name": "SeaWorld Orlando", "type": "theme park", "suitability": ["family", "adventure"]},
        {"name": "ICON Park", "type": "entertainment", "suitability": ["family", "leisure"]},
        {"name": "Gatorland", "type": "wildlife", "suitability": ["family", "adventure"]},
        {"name": "Kennedy Space Center Visitor Complex", "type": "educational", "suitability": ["family", "cultural"]}
    ],
    "Southeast Asia": [ # Generic for backpacking, will need more specific destinations for real planning
        {"name": "Angkor Wat (Cambodia)", "type": "cultural", "suitability": ["backpacking", "cultural", "adventure"]},
        {"name": "Ha Long Bay (Vietnam)", "type": "nature", "suitability": ["backpacking", "adventure", "relaxing"]},
        {"name": "Ubud Monkey Forest (Bali, Indonesia)", "type": "nature", "suitability": ["backpacking", "cultural"]},
        {"name": "Full Moon Party (Koh Phangan, Thailand)", "type": "party", "suitability": ["backpacking", "adventure"]},
        {"name": "Phuket Beaches (Thailand)", "type": "relaxing", "suitability": ["backpacking", "relaxing"]},
        {"name": "Ho Chi Minh City War Remnants Museum (Vietnam)", "type": "historical", "suitability": ["cultural", "backpacking"]},
        {"name": "Mount Bromo (Indonesia)", "type": "adventure", "suitability": ["backpacking", "adventure"]}
    ],
    "New York": [
        {"name": "Statue of Liberty", "type": "landmark", "suitability": ["cultural", "family", "business"]},
        {"name": "Times Square", "type": "landmark", "suitability": ["leisure", "business"]},
        {"name": "Central Park", "type": "relaxing", "suitability": ["family", "romantic", "leisure", "business"]},
        {"name": "Broadway Show", "type": "entertainment", "suitability": ["cultural", "romantic", "business"]},
        {"name": "Metropolitan Museum of Art", "type": "cultural", "suitability": ["cultural", "business"]},
        {"name": "Empire State Building", "type": "landmark", "suitability": ["cultural", "romantic", "business"]},
        {"name": "9/11 Memorial & Museum", "type": "historical", "suitability": ["cultural", "business"]},
        {"name": "Brooklyn Bridge", "type": "landmark", "suitability": ["leisure", "romantic"]}
    ],
    "Japan": [
        {"name": "Mount Fuji", "type": "nature", "suitability": ["cultural", "adventure", "relaxing"]},
        {"name": "Tokyo Skytree", "type": "landmark", "suitability": ["leisure", "family"]},
        {"name": "Fushimi Inari-taisha (Kyoto)", "type": "cultural", "suitability": ["cultural", "romantic"]},
        {"name": "Shibuya Crossing (Tokyo)", "type": "leisure", "suitability": ["leisure", "adventure"]},
        {"name": "Arashiyama Bamboo Grove (Kyoto)", "type": "nature", "suitability": ["relaxing", "cultural"]},
        {"name": "Hiroshima Peace Memorial Park", "type": "historical", "suitability": ["cultural"]},
        {"name": "Gion District (Kyoto)", "type": "cultural", "suitability": ["cultural", "romantic"]}
    ],
    "Bali": [
        {"name": "Ubud Monkey Forest", "type": "nature", "suitability": ["relaxing", "cultural", "family"]},
        {"name": "Tanah Lot Temple", "type": "cultural", "suitability": ["romantic", "cultural"]},
        {"name": "Seminyak Beach", "type": "relaxing", "suitability": ["relaxing", "romantic", "family"]},
        {"name": "Tegallalang Rice Terraces", "type": "nature", "suitability": ["relaxing", "cultural"]},
        {"name": "Mount Batur Sunrise Trek", "type": "adventure", "suitability": ["adventure"]},
        {"name": "Yoga Barn (Ubud)", "type": "wellness", "suitability": ["relaxing"]},
        {"name": "Spa treatments (various locations)", "type": "wellness", "suitability": ["relaxing", "romantic"]}
    ],
    "Rome": [
        {"name": "Colosseum", "type": "historical", "suitability": ["cultural", "family", "romantic"]},
        {"name": "Roman Forum & Palatine Hill", "type": "historical", "suitability": ["cultural", "romantic"]},
        {"name": "Vatican City (St. Peter's Basilica, Vatican Museums)", "type": "cultural", "suitability": ["cultural", "family"]},
        {"name": "Trevi Fountain", "type": "landmark", "suitability": ["romantic", "cultural"]},
        {"name": "Pantheon", "type": "historical", "suitability": ["cultural"]},
        {"name": "Spanish Steps", "type": "leisure", "suitability": ["leisure", "romantic"]},
        {"name": "Borghese Gallery and Museum", "type": "cultural", "suitability": ["cultural"]}
    ],
    "Malaysia": [
        {"name": "Petronas Twin Towers (Kuala Lumpur)", "type": "landmark", "suitability": ["leisure", "business", "family"]},
        {"name": "Batu Caves (Kuala Lumpur)", "type": "cultural", "suitability": ["cultural", "adventure"]},
        {"name": "Perdana Botanical Garden (Kuala Lumpur)", "type": "nature", "suitability": ["relaxing", "family"]},
        {"name": "Kuala Lumpur Bird Park", "type": "wildlife", "suitability": ["family"]},
        {"name": "Central Market (Kuala Lumpur)", "type": "shopping", "suitability": ["cultural", "leisure"]},
        {"name": "Penang Hill (Penang)", "type": "nature", "suitability": ["relaxing", "family", "cultural"]},
        {"name": "George Town Street Art (Penang)", "type": "cultural", "suitability": ["cultural", "leisure"]},
        {"name": "Langkawi SkyCab (Langkawi)", "type": "adventure", "suitability": ["adventure", "family", "romantic"]}
    ]
}

def geo_routing_agent(user_travel_details_json):
    """
    Generates a travel itinerary based on user preferences and available attractions.
    """
    try:
        user_details = json.loads(user_travel_details_json)
    except json.JSONDecodeError:
        return "Invalid JSON input for travel details."

    destination = user_details.get("destination", "").split(',')[0].strip()
    preferences = user_details.get("preferences", "").lower()
    travel_style = user_details.get("travel_style", "").lower()
    dates_duration = user_details.get("dates_duration", "")

    print(f"Processing request for: {destination}")
    print(f"Preferences: {preferences}")
    print(f"Travel Style: {travel_style}")
    print(f"Duration: {dates_duration}")

    # Further logic to filter and route attractions will be added here
    return {
        "destination": destination,
        "preferences": preferences,
        "travel_style": travel_style,
        "dates_duration": dates_duration,
        "status": "details_extracted"
    }


import json

def geo_routing_agent(user_travel_details_json):
    """
    Generates a geo-routing plan based on user travel details, including reachable attractions
    and a proposed daily itinerary, presented in a structured JSON format.

    Args:
        user_travel_details_json (str): A JSON string containing user travel details
                                         (destination, preferences, travel_style, dates_duration).

    Returns:
        dict: A dictionary representing the structured geo-routing plan, or an empty dict if an error occurs.
    """
    try:

        if isinstance(user_travel_details_json, str):
            user_details = json.loads(user_travel_details_json)
        
        else:
            user_details = user_travel_details_json

        destination = user_details.get("destination", "").replace("Kuala Lumpur", "Malaysia") # Normalize for lookup
        preferences_str = user_details.get("preferences", "").lower()
        travel_style = user_details.get("travel_style", "").lower()
        dates_duration = user_details.get("dates_duration", "")

        # Extract duration in days for routing
        duration_days = 1 # Default to 1 day if not specified or extractable
        if "days" in dates_duration:
            try:
                duration_days = int(dates_duration.split(" ")[0])
            except ValueError:
                pass # Keep default if conversion fails
        elif "week" in dates_duration:
            try:
                num_weeks = int(dates_duration.split(" ")[0])
                duration_days = num_weeks * 7
            except ValueError:
                duration_days = 7 # Default to 1 week if conversion fails
        elif "day" in dates_duration:
            duration_days = 1 # Single day trip

        # Ensure a minimum of 1 day and a maximum of 7 days for simplified routing
        duration_days = max(1, min(duration_days, 7))


        # Filter attractions based on destination, preferences, and travel style
        available_attractions = ATTRACTIONS_DATA.get(destination.split(',')[0].strip(), [])
        filtered_attractions = []

        # Add "general" keywords to preferences for broader matching if not specific
        keywords = set(preferences_str.split(', ')) if preferences_str else set()
        if not keywords and travel_style: # If no explicit preferences, infer from travel style
            keywords.add(travel_style)
        if "cultural" in preferences_str or "historical" in preferences_str:
            keywords.add("cultural")
            keywords.add("historical")
        if "adventure" in preferences_str or "theme park" in preferences_str:
            keywords.add("adventure")
            keywords.add("theme park")
        if "relaxing" in preferences_str or "beach" in preferences_str or "spa" in preferences_str:
            keywords.add("relaxing")
            keywords.add("wellness")
        if "family" in travel_style:
            keywords.add("family")
        if "romantic" in travel_style:
            keywords.add("romantic")
        if "business" in travel_style:
            keywords.add("business")
        if "backpacking" in travel_style:
            keywords.add("backpacking")
            keywords.add("adventure")
            keywords.add("cultural") # Backpackers often seek culture

        # Add all attraction types if no specific preferences are given
        if not keywords:
            for attraction in available_attractions:
                filtered_attractions.append(attraction)
        else:
            for attraction in available_attractions:
                # Check if any of the keywords match the attraction's suitability or type
                if any(kw in attraction["suitability"] or kw == attraction["type"] for kw in keywords):
                    filtered_attractions.append(attraction)

        # Simple daily routing (distribute attractions evenly or based on a heuristic)
        daily_itinerary = {f"Day {i+1}": [] for i in range(duration_days)}
        if filtered_attractions:
            for i, attraction in enumerate(filtered_attractions):
                day_index = i % duration_days
                daily_itinerary[f"Day {day_index+1}"].append(attraction["name"])

        # Generate structured output using Groq client
        system_prompt = (
            "You are a 'Geo Routing Agent' in a multi-agent travel planning system.\n"
            "Your task is to provide a detailed geo-routing plan, including reachable attractions "
            "and a proposed daily itinerary, based on the user's travel details.\n\n"
            "The output MUST be a strict JSON object with the following structure:\n"
            "{\n"
            "  \"destination\": \"[Destination Name]\",\n"
            "  \"preferences\": \"[User Preferences]\",\n"
            "  \"travel_style\": \"[User Travel Style]\",\n"
            "  \"reachable_attractions\": [\n"
            "    {\"name\": \"[Attraction Name]\", \"type\": \"[Type]\"},\n"
            "    ...\n"
            "  ],\n"
            "  \"daily_itinerary\": {\n"
            "    \"Day 1\": [\"[Attraction 1]\", \"[Attraction 2]\"],\n"
            "    \"Day 2\": [...],\n"
            "    ...\n"
            "  },\n"
            "  \"notes\": \"[Any additional notes or recommendations]\"\n"
            "}\n\n"
            "Ensure that:\n"
            "- 'reachable_attractions' lists all suitable attractions found.\n"
            "- 'daily_itinerary' distributes these attractions into logical daily plans, considering the duration.\n"
            "- If no suitable attractions are found, 'reachable_attractions' should be an empty list, and 'daily_itinerary' should reflect an empty plan for each day.\n"
            "- The 'notes' field can be used for general advice or limitations of the plan."
        )

        user_content = {
            "destination": destination,
            "preferences": preferences_str,
            "travel_style": travel_style,
            "duration_days": duration_days,
            "filtered_attractions": [{"name": attr["name"], "type": attr["type"]} for attr in filtered_attractions],
            "daily_itinerary_draft": daily_itinerary
        }

        # Assuming 'client' is a global Groq client instance available in the environment
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_content, indent=2)},
            ],
            temperature=0.2, # Low temperature for structured output
            response_format={"type": "json_object"}
        )

        response_content = response.choices[0].message.content
        geo_plan = json.loads(response_content)
        return geo_plan

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON input or model response: {e}")
        print(f"Input: {user_travel_details_json}")
        return {"error": f"JSON Decode Error: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred in geo_routing_agent: {e}")
        return {"error": f"Unexpected Error: {e}"}


import json
from groq import Groq

def planning_agent(user_travel_details_json, geo_plan_json):

    try:

        # Convert inputs to dict if they are JSON strings
        if isinstance(user_travel_details_json, str):
            user_details = json.loads(user_travel_details_json)
        else:
            user_details = user_travel_details_json

        if isinstance(geo_plan_json, str):
            geo_plan = json.loads(geo_plan_json)
        else:
            geo_plan = geo_plan_json

        system_prompt = """
You are a **Travel Planning Agent** in a multi-agent travel planning system.

Your job is to create a **complete day-wise itinerary** using:

1. User travel details
2. Geo-routing attractions

You must include:
- Day wise travel plan
- Recommended food places
- Authentic local food for breakfast, lunch and dinner
- Small travel tips

Return ONLY a JSON object in the following format:

{
 "destination": "",
 "travel_style": "",
 "trip_plan": {
    "Day 1": {
        "places_to_visit": [],
        "breakfast": {"food": "", "place": ""},
        "lunch": {"food": "", "place": ""},
        "dinner": {"food": "", "place": ""}
    },
    "Day 2": {}
 },
 "tips": ""
}
"""
        user_content = {
            "user_details": user_details,
            "geo_routing_plan": geo_plan
        }

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_content, indent=2)}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        response_content = response.choices[0].message.content
        trip_plan = json.loads(response_content)

        return trip_plan

    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        return {}

    except Exception as e:
        print("Unexpected error:", e)
        return {}

 


def itinerary_agent(
    user_details_json,
    rag_info_json,
    geo_plan_json,
    budget_json,
    planning_json
):

    try:

        # Convert JSON string to dict if necessary
        def parse_json(data):
            if isinstance(data, str):
                return json.loads(data)
            return data

        user_details = parse_json(user_details_json)
        rag_info = parse_json(rag_info_json)
        geo_plan = parse_json(geo_plan_json)
        budget = parse_json(budget_json)
        planning = parse_json(planning_json)

        system_prompt = """
You are a **Final Itinerary Agent** in a multi-agent travel planning system.

Your job is to combine outputs from multiple agents and present them in a **clear, structured, user-friendly travel itinerary**.

The final output should be **well formatted and easy to read**.

Structure the response with the following sections:

1️⃣ Trip Overview
- Destination
- Duration
- Travel Style
- Preferences

2️⃣ Day Wise Travel Plan
Provide clear daily plans.

3️⃣ Food Recommendations
Breakfast, Lunch, Dinner suggestions.

4️⃣ Budget Summary
Break down total cost.

5️⃣ Visa / Safety / Travel Tips

6️⃣ Packing Checklist

Use bullet points, headings, and clear formatting.
Make the itinerary easy to read and visually structured.

Return the output as a **formatted travel guide text**.
"""

        agent_data = {
            "user_details": user_details,
            "rag_information": rag_info,
            "geo_routing_plan": geo_plan,
            "budget_plan": budget,
            "travel_plan": planning
        }

      

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(agent_data, indent=2)}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Error in itinerary agent:", e)
        return "Failed to generate itinerary."


def run_travel_planner(user_query):

    # 1 Trip understanding
    trip_info = trip_understanding_agent(user_query)

    # 2 RAG travel advice
    rag_info = rag_query(user_query)

    # 3 Budget
    budget = Budget_agent(trip_info)

    # 4 Geo routing
    geo_plan = geo_routing_agent(trip_info)

    # 5 Final planning
    trip_plan = planning_agent(trip_info, geo_plan)

    return {
        "trip_info": trip_info,
        "rag_info": rag_info,
        "budget": budget,
        "geo_plan": geo_plan,
        "trip_plan": trip_plan
    }