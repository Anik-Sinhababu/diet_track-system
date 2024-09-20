import streamlit as st
import requests
import base64
from datetime import datetime

# Nutritionix API credentials
APP_ID = "b5516349"
API_KEY = "c76436579e5bee1282265ffab0718557"


def get_nutrition_details(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "query": food_item,
        "timezone": "US/Eastern"
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        nutrition_data = response.json()
        nutrition_totals = {
            'calories': 0,
            'total_fat': 0,
            'protein': 0,
            'carbohydrates': 0
        }
        result_string = ""
        for food in nutrition_data['foods']:
            result_string += f"Food: {food['food_name']}\n"
            result_string += f"Calories: {food['nf_calories']} kcal\n"
            result_string += f"Serving Size: {food['serving_qty']} {food['serving_unit']}\n"
            result_string += f"Total Fat: {food['nf_total_fat']} g\n"
            result_string += f"Protein: {food['nf_protein']} g\n"
            result_string += f"Carbohydrates: {food['nf_total_carbohydrate']} g\n"
            result_string += "-" * 30 + "\n"

            # Accumulate totals
            nutrition_totals['calories'] += food['nf_calories']
            nutrition_totals['total_fat'] += food['nf_total_fat']
            nutrition_totals['protein'] += food['nf_protein']
            nutrition_totals['carbohydrates'] += food['nf_total_carbohydrate']

        return result_string, nutrition_totals
    else:
        return f"Error: Unable to fetch details, status code {response.status_code}", None


# Streamlit App
def main():
    # Set background image
    set_background('bgimg.jpg')  # Ensure the image is in the same directory

    st.title("Nutrition Tracker")

    # Input from the user for breakfast, lunch, and dinner
    st.subheader("Enter what you ate for each meal:")

    breakfast = st.text_input("Breakfast")
    lunch = st.text_input("Lunch")
    dinner = st.text_input("Dinner")

    # Initialize total nutrition counters
    total_nutrition = {
        'calories': 0,
        'total_fat': 0,
        'protein': 0,
        'carbohydrates': 0
    }

    # When the user clicks the 'Track Nutrition' button
    if st.button("Track Nutrition"):
        if breakfast or lunch or dinner:
            st.subheader("Nutrition Information:")

            if breakfast:
                st.text(f"Breakfast: {breakfast}")
                nutrition_info, nutrition_totals = get_nutrition_details(breakfast)
                st.text(nutrition_info)  # Display the result for breakfast
                if nutrition_totals:
                    total_nutrition['calories'] += nutrition_totals['calories']
                    total_nutrition['total_fat'] += nutrition_totals['total_fat']
                    total_nutrition['protein'] += nutrition_totals['protein']
                    total_nutrition['carbohydrates'] += nutrition_totals['carbohydrates']

            if lunch:
                st.text(f"Lunch: {lunch}")
                nutrition_info, nutrition_totals = get_nutrition_details(lunch)
                st.text(nutrition_info)  # Display the result for lunch
                if nutrition_totals:
                    total_nutrition['calories'] += nutrition_totals['calories']
                    total_nutrition['total_fat'] += nutrition_totals['total_fat']
                    total_nutrition['protein'] += nutrition_totals['protein']
                    total_nutrition['carbohydrates'] += nutrition_totals['carbohydrates']

            if dinner:
                st.text(f"Dinner: {dinner}")
                nutrition_info, nutrition_totals = get_nutrition_details(dinner)
                st.text(nutrition_info)  # Display the result for dinner
                if nutrition_totals:
                    total_nutrition['calories'] += nutrition_totals['calories']
                    total_nutrition['total_fat'] += nutrition_totals['total_fat']
                    total_nutrition['protein'] += nutrition_totals['protein']
                    total_nutrition['carbohydrates'] += nutrition_totals['carbohydrates']

            # Display total nutrition
            st.subheader("Total Nutrition Information:")
            st.text(f"Total Calories: {total_nutrition['calories']} kcal")
            st.text(f"Total Fat: {total_nutrition['total_fat']} g")
            st.text(f"Total Protein: {total_nutrition['protein']} g")
            st.text(f"Total Carbohydrates: {total_nutrition['carbohydrates']} g")

            # Display today's date
            today_date = datetime.now().strftime("%Y-%m-%d")
            st.text(f"Date: {today_date}")

        else:
            st.subheader("Please enter at least one meal to track.")


# Function to add background image
def set_background(image_file):
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url(data:image/jpg;base64,{get_base64_of_bin_file(image_file)});
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


# Helper function to convert image file to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


if __name__ == "__main__":
    main()
