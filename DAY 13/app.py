## Travel Agent Code

import streamlit as st
import pandas as pd
from travel_agent import run_travel_planner

st.set_page_config(
    page_title="AI Multi-Agent Travel Planner",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AI Multi-Agent Travel Planner")

st.markdown(
"""
Plan your trips using **AI agents** that collaborate together.

**Agents used:**

• Trip Understanding Agent  
• Travel Advice RAG Agent  
• Budget Planning Agent  
• Geo Routing Agent  
• Travel Itinerary Agent  
"""
)

query = st.text_area(
    "Enter your travel request",
    placeholder="Example: I want to visit Japan for 5 days with my wife and explore cultural places"
)

if st.button("Generate Travel Plan"):

    if query.strip() == "":
        st.warning("Please enter a travel request")
    else:

        with st.spinner("AI agents are planning your trip..."):
            results = run_travel_planner(query)

        st.success("Your travel plan is ready!")

        trip_info = results["trip_info"]
        rag_info = results["rag_info"]
        budget = results["budget"]
        geo_plan = results["geo_plan"]
        itinerary = results["trip_plan"]

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Trip Details",
            "Travel Advice",
            "Budget Breakdown",
            "Geo Routing",
            "Itinerary"
        ])

        # ---------------- Trip Info ----------------
        with tab1:
            st.subheader("Trip Information")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Destination", trip_info.get("destination", "N/A"))

            with col2:
                st.metric("Duration", trip_info.get("dates_duration", "N/A"))

            with col3:
                st.metric("Travel Style", trip_info.get("travel_style", "N/A"))

            st.markdown("### Preferences")
            st.write(trip_info.get("preferences", "Not specified"))

        # ---------------- Travel Advice ----------------
        with tab2:
            st.subheader("Travel Advice")
            st.info(rag_info)

        # ---------------- Budget ----------------
        with tab3:
            st.subheader("Budget Plan")

            if isinstance(budget, dict):

                df = pd.DataFrame(
                    budget.items(),
                    columns=["Category", "Cost (INR)"]
                )

                st.table(df)

                total = sum(budget.values())

                st.metric("Estimated Total Cost", f"₹ {total:,}")

            else:
                st.write(budget)

        # ---------------- Geo Routing ----------------
        with tab4:
            st.subheader("Places to Visit")

            if isinstance(geo_plan, dict):

                for day, places in geo_plan.items():
                    with st.expander(day):
                        for place in places:
                            st.write(f"📍 {place}")

            else:
                st.write(geo_plan)

        # ---------------- Itinerary ----------------
        with tab5:
            st.subheader("Day-Wise Itinerary")

            if isinstance(itinerary, dict):

                for day, plan in itinerary.items():
                    st.markdown(f"### {day}")
                    st.write(plan)

            else:
                st.write(itinerary)