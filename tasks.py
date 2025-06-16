from crewai import  Task
# from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os 
load_dotenv()


os.getenv("GEMINI_API_KEY")

# research_tool = SerperDevTool()


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
    def Weather_Analysis_Task(self, agent, weather_data):
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
                    - 'ga' or 'gi' in dono lafzo ka use bhi nhi krna.

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
                    G to kisan Bhai main ne aap ki zameen aur mausam ka jaiza lia hai. Mere hisab sy sab se behtareen fasal jo aap laga saktay hain wo hai bhindi. Ye fasal takreeban 60 din mein tayar ho jaye gi aur aap esay market mein achi qeemat par bech saktay hain. Bhindi ko rozana do martaba pani ki zarurat hoti hai pehla pani subha fajar ke baad ya nashtay se pehle dein aur doosra pani shaam mein maghrib ke baad ya raat ke khanay se thodi der pehle dein

                    Dusri behtareen fasal aap ke ilaqay ke liye tamatar hai. Ye lagbhag 75 din mein ready ho jati hai. Esay bhi roz do dafa pani chahiye subha 7 baje ke kareeb aur shaam 6 baje ke aas paas

                    Teesri fasal jo aap ke liye faydamand ho sakti hai wo hai paalak. Paalak 45 din mein ready ho jati hai. Esay sirf ek martaba pani dena kaafi ho ga subha 8 baje ke kareeb pani dein

                    In teenon mein se aap kisi bhi fasal ka intekhab kar saktay hain lekin agar aap jaldi munafa chahte hain to paalak ya bhindi behtareen hain. InshaAllah achi paidawaar aur faida hoga
                    """
        )


    ##############################################################################################################
        # Task 5
    ##############################################################################################################
    def Urdu_Agri_Advisor_Task(self, agent, soil_data, suggestedCrops, user_question):
        return Task(
            description=f"""Assist a Pakistani farmer by answering their crop-related question based on soil data.

            The agent will:
            - Use the provided soil information to assess suitability of the crop the farmer asks about.
            - Compare it with already suggested crops and determine whether the new crop is better.
            - If the question is only about soil, respond only with relevant soil details.
            - If the question is unrelated to soil or crops, respond politely in Roman Urdu, stating it's out of expertise.

            Parameters:
            - Soil Data: {soil_data}
            - Suggested Crops: {suggestedCrops}
            - Farmer’s Question: "{user_question}"

            The agent will respond in concise, polite Roman Urdu without using emojis or symbols.
            """,

            tools=[],
            agent=agent,

            expected_output="""
                A short, clear, Urdu-language response:
                - If crop is suitable: state why and compare with suggested crops.
                - If crop is unsuitable: give reason and optionally suggest alternatives.
                - If question is soil-related only: respond with soil information.
                - If question is irrelevant: politely decline in Urdu.
            """
        )



    ##############################################################################################################
        # Task 6
    ##############################################################################################################
    def Irrigation_Advisor_Task(self, agent, soil_data, weather_data, crop_name):
        return Task(
            description=f"""Aik Pakistani kisan ko guide karein ke usay apni fasal ("{crop_name}") ko paani dena chahiye ya nahi, soil aur weather data ke analysis ki buniyad par.

            Agent ka kaam:
            - Soil moisture, temperature, aur weather conditions ka tajziya karein
            - Faslon ki zarurat ko samjhein (crop_name ki khasiyat ke mutabiq)
            - Agar paani dena zaroori ho:
                - **Detail se bataayein ke kyun**
                - Moisture level ya high temperature ki buniyad par reasoning dein
                - Kitne ghanto ke andar dena chahiye, yeh bhi mention karein
            - Agar paani dena zaroori nahi:
                - **Detail se waja batayein**
                - Moisture kaafi hai ya mausam thanda hai to explain karein
                - Bataayein ke kitne ghanto tak paani ki zaroorat nahi padegi

            Parameters:
            - Soil Data: {soil_data}
            - Weather Data: {weather_data}
            - Crop Name: "{crop_name}"

            Jawab sirf Roman Urdu mein ho — understandable, friendly, aur kisan ki zaban mein. Koi emoji ya complex terms use na karein.
            """,

            tools=[],
            agent=agent,

            expected_output="""
                Roman Urdu mein tafseelat ke sath jawab:
                - Agar paani zaroori hai: "Aap ne tinda lagaya hai. Is waqt zameen ka moisture 18% hai jo kam hai, aur temperature bhi 32°C hai. Ye sabzi ko stress de sakta hai. Agle 2 ghanto ke andar paani de dein."
                - Agar paani zaroori nahi: "Aap ne palak lagayi hai. Zameen ka moisture 30% hai aur mausam thanda hai. Agle 10 ghanto tak paani ki koi zaroorat nahi."
            """
        )
