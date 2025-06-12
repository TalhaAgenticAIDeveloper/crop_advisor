from crewai import  Task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os 
load_dotenv()


os.getenv("GEMINI_API_KEY")

research_tool = SerperDevTool()


class Farmer_Tasks:

    ##############################################################################################################
        # Task 1
    ##############################################################################################################
    def Soil_Analysis_Task(self, agent, soil_sensor_data):
        return Task(
            description=f"""Analyze the provided soil sensor data for the given agricultural location.

            The agent will:
            - Interpret sensor readings for moisture, temperature, pH, nitrogen, phosphorus, and potassium.
            - Classify the soil type (e.g., loamy, sandy, clayey).
            - Assess the fertility level (low, medium, high) based on nutrient values.
            - Determine which general crop categories (e.g., leafy vegetables, grains, root crops) are suitable for this soil.

            Parameters:
            - Soil Sensor Data: {soil_sensor_data}
        

            The agent will output an analysis of soil quality, structure, and suitability for growing crops.
            """,

            tools=[],
            agent=agent,
            expected_output="""
                    A structured JSON report containing:
                    - Soil Type (e.g., Loamy, Sandy)
                    - Fertility Level (Low, Medium, High)
                    - Suggested Crop Categories (e.g., Leafy Greens, Root Vegetables, Grains)
                 """
        )


    ##############################################################################################################
        # Task 2
    ##############################################################################################################
    def Weather_Analysis_Task(self, agent, weather_data,context):
        return Task(
            description=f"""Analyze the current weather conditions to assess their suitability for agricultural activity.

            The agent will:
            - Interpret real-time weather data including temperature, humidity, wind speed, and weather description.
            - Determine the climate type (e.g., warm-dry, humid, moderate).
            - Identify any environmental risks to crop growth such as heat stress, low humidity, or high winds.
            - Evaluate the overall growing condition (Favorable, Moderate, or Poor) based on the weather.

            Parameters:
            - Weather Data: {weather_data}
    

            The agent will provide an environmental assessment useful for crop planning.
            """,
            context = context,
            tools=[],
            agent=agent,
            expected_output="""
                    A structured JSON report containing:
                    - Climate Type (e.g., Warm-Dry, Humid-Tropical)
                    - Weather Risks (list of potential risks)
                    - Growing Condition Assessment (Favorable, Moderate, Poor)
                """
        )



    ##############################################################################################################
        # Task 3
    ##############################################################################################################
    def Crop_Selection_Task(self, agent, soil_analysis_output, weather_analysis_output, context):
        return Task(
            description=f"""Using the analyzed soil and weather data, recommend the top 3 crops suitable for cultivation.

            The agent will:
            - Review soil analysis including type, fertility level, and crop category suggestions.
            - Review weather analysis including climate type, risks, and growing condition.
            - Select the 3 most compatible crops based on combined soil and weather profiles.
            - For each crop, estimate:
                1. Time to harvest (in days)
                2. Watering frequency per day

            Parameters:
            - Soil Analysis Output: {soil_analysis_output}
            - Weather Analysis Output: {weather_analysis_output}

            The agent will return crop names, growth durations, and water schedules.
            """,
            context = context,
            tools=[],
            agent=agent,
            expected_output="""
                    A structured JSON list of 3 crops, each with:
                    - Crop Name
                    - Estimated Days to Harvest
                    - Recommended Watering Frequency Per Day
                """
        )
    


    ##############################################################################################################
        # Task 4
    ##############################################################################################################
        # def Advisory_Message_Task(self, agent, crop_recommendations,context, language="Roman Urdu"):
        #     return Task(
        #         description=f"""Convert crop recommendations into a clear and friendly advisory message in {language} 
        #         for local farmers.

        #         The agent will:
        #         - Use spoken-style Roman Urdu
        #         - Write structured output:
        #             1. Crop name
        #             2. Kitne din mein tayar ho gi
        #             3. Roz kitni dafa pani dena hai
        #             4. Har watering ka exact time (e.g., subha 7 baje, shaam 6 baje)

        #         Message should feel like direct advice from an experienced farmer, in simple, warm tone.

        #         Parameters:
        #         - Crop Recommendations: {crop_recommendations}
        #         - Language: {language}

        #         Output:
        #         Structured Roman Urdu message for farmers with each crop and its details.
        #         """
        #     ,   context = context,
        #         tools=[],
        #         agent=agent,
        #         expected_output="""
        #                 Pehli crop: Tamatar
        #                 • 75 din mein tayar ho ga
        #                 • Roz 2 dafa pani den: subha 7 baje, shaam 6 baje

        #                 Dusri crop: Bhindi
        #                 • 60 din mein tayar ho gi
        #                 • Roz 2 dafa pani: subha 8 baje, shaam 5:30 baje

        #                 Teesri crop: Palak
        #                 • 45 din mein ready ho gi
        #                 • Roz sirf 1 dafa pani: subha 8 baje

        #                 Yeh crops aap ke ilaqay ke liye behtareen hain. InshaAllah achi paidawaar aur munafa hoga.
        #             """
        #     )

    def Advisory_Message_Task(self, agent, crop_recommendations, context, language="Roman Urdu"):
        return Task(
            description=f"""Convert crop recommendations into a clear and friendly advisory message in {language} 
                    for local farmers.

                    The agent will:
                    - Use spoken-style Roman Urdu
                    - Write human-like natural output:
                        - Pehle crop ka naam
                        - Kitne din mein tayar ho gi
                        - Roz kitni dafa pani dena hai
                        - Har dafa pani dene ka time (jaise subha 7 baje, shaam 6 baje)

                    - Message aisa ho jaise koi tajurba kaar kisaan dosray kisaan ko mashwara de raha ho, asaan aur garam lehja mein.

                    Important:
                    - Expected output mein koi symbols na ho jaise dot, bullet, ya colon.
                    - Sirf plain text ho, jaise aam baat cheet mein hota hai.

                    Parameters:
                    - Crop Recommendations: {crop_recommendations}
                    - Language: {language}

                    Output:
                    Plain Roman Urdu message for farmers based on soil and weather analysis.
                    """,
            context=context,
            tools=[],
            agent=agent,
            expected_output="""
                    Main ne aap ki zameen aur mausam ka jaiza lia hai. Mere tajziye ke mutabiq sab se behtareen fasal jo aap laga saktay hain wo hai bhindi. Ye fasal takreeban 60 din mein tayar ho jaye gi aur aap isay market mein achi qeemat par bech saktay hain. Bhindi ko rozana do martaba pani ki zarurat ho gi pehla pani subha fajar ke baad ya nashtay se pehle dein aur doosra pani shaam mein maghrib ke baad ya raat ke khanay se thodi der pehle dein

                    Dusri behtareen fasal aap ke ilaqay ke liye tamatar hai. Ye lagbhag 75 din mein ready ho jaye gi. Isay bhi roz do dafa pani chahiye subha 7 baje ke kareeb aur shaam 6 baje ke aas paas

                    Teesri fasal jo aap ke liye faidamand ho sakti hai wo hai palak. Palak 45 din mein ready ho jaye gi. Isay sirf ek martaba pani dena kaafi ho ga subha 8 baje ke kareeb pani dein

                    In teenon mein se aap kisi bhi fasal ka intekhab kar saktay hain lekin agar aap jaldi munafa chahte hain to palak ya bhindi behtareen rahein gi. InshaAllah achi paidawaar aur faida hoga
                    """
        )
