# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# fetching data from db smoothies
cnx=st.connection('snowflake')

session = cnx.session()

name_on_order=st.text_input('Name On Smoothie:')

st.write('The name on your smoothie will be :',name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list=st.multiselect(
                  'Choose upto 5 ingrediants:',
                  my_dataframe,
                  max_selections=5
                    )

# view selected list

if ingredients_list:

    # ingrediants string

    ingredients_string=''

    for fruit_selected in ingredients_list:

        ingredients_string+=fruit_selected+' '
        
    # insert statement

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert=st.button('Submit')

    if time_to_insert:
        
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered,'+name_on_order+'!',icon="✅")


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)


    



