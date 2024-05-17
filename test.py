import streamlit as st
import pandas as pd

occu_list = {"other"
	,"academic/educator"
	,"artist"
	,"clerical/admin"
	,"college/grad student"
	,"customer service"
	,"doctor/health care"
	,"executive/managerial"
	,"farmer"
	,"homemaker"
	,"K-12 student"
	,"lawyer"
	,"programmer"
	,"retired"
	,"sales/marketing"
	,"scientist"
	,"self-employed"
	,"technician/engineer"
	,"tradesman/craftsman"
	,"unemployed"
	,"writer"
    }

def save_user_data(data):

    """Save the registered user data to a CSV file."""
    df = pd.DataFrame([data])
    st.write(df)

def show_registration_form():
    """Show the registration form and handle data submission."""
    with st.form(key='registration_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        gender = st.selectbox("Gender", options=["Male", "Female"])
        occupation = st.selectbox("Occupation", options=occu_list)
        age = st.number_input("Age", min_value=18, max_value=100, step=1, format='%d')
        submit_button = st.form_submit_button("Register")

        if submit_button:
            user_data = {
                'username': username,
                'password': password,  
                'gender': gender,
                'occupation' : occupation,
                'age': age
            }
            save_user_data(user_data)
            st.success(f"User {username} registered successfully!")

def main():
    st.title("User Registration Form")
    show_registration_form()

if __name__ == "__main__":
    main()