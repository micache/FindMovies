import streamlit as st
import pandas as pd

st.title('File Upload to MySQL Database')

def gen_data_id():
    ID_LENGTH = 10
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(ID_LENGTH))
    
def save_csv_to_db(uploaded_file):
    dataframe = pd.to_csv(uploaded_file)
    

uploaded_file = st.file_uploader("Choose a file", type='csv')
if uploaded_file is not None:
    # Check if the uploaded file is a CSV by checking its content type
    if uploaded_file.type != "text/csv":
        st.error('Error: The file uploaded is not a CSV file.')
    else:
        # Process the CSV file
        save_csv_to_db(uploaded_file)
        st.success('CSV file successfully uploaded and saved to the database!')