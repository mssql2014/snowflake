import streamlit
import pandas
import requests
import snowflake.connector

def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)    
  df = fruityvice_response.json()
  fruityvice_normalized = pandas.json_normalize(df)
  return fruityvice_normalized
  
streamlit.title('Italy is great')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.write('Please enter fruit to get information')    
  else:  
    back_from_functoin = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_functoin)
except URLError as e:
  streamlit.error()
  	
add_my_fruit = streamlit.text_input('What fruit would you like to add')
streamlit.write('Thank you for adding ', add_my_fruit)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("THE FRUIT LOAD LIST CONTAINES:")

streamlit.dataframe(my_data_rows)
