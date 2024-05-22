from streamlit.testing.v1 import AppTest

def test_registration_form():
    at = AppTest.from_file('app.py', default_timeout=30).run()

    # check username
    at.text_input[0].set_value('username')
    at.text_input[1].set_value('password')
    
    assert at.selectbox[0].value == 'Male'
    assert at.selectbox[1].value == 'other'
    assert at.number_input[0].value == 18

    at.button[0].click().run()
    at.button[0].click().run()

    assert at.session_state['user_data'] == {
                'username': 'username',
                'password': 'password',  
                'gender': 'Male',
                'occupation' : 'other',
                'age': 18
            }

def test_home_page():
    
    at = AppTest.from_file('app.py', default_timeout=30).run()

    at.session_state['user_data'] = {
                'username': 'username',
                'password': 'password',  
                'gender': 'Male',
                'occupation' : 'other',
                'age': 18
            }
    at.run()

    # check page state
    assert at.session_state.page == 'home'

    # check title
    assert at.title[0].value == 'Hello, username!'

    # check checkbox
    assert at.checkbox[0].value == False
    at.checkbox[0].check().run()
    assert at.checkbox[0].value == True

    # tick more than one box
    assert at.checkbox[10].value == False
    at.checkbox[10].check().run()
    assert at.checkbox[10].value == True and at.checkbox[0].value == True

    # check slider
    assert at.slider[0].value == 0
    at.slider[0].set_value(5).run()
    assert at.slider[0].value == 5

def test_search():
    at = AppTest.from_file('app.py', default_timeout=30).run()

    at.session_state['user_data'] = {
                'username': 'username',
                'password': 'password',  
                'gender': 'Male',
                'occupation' : 'other',
                'age': 18
            }
    at.run()

    # check search bar (forrest gump)
    at.text_input[0].set_value('forrest').run()
    assert at.button[0].label == 'Forrest Gump (1994)'
    at.button[0].click().run()
    # check if plot is call success
    assert at.markdown[5].value == "Plot: Forrest Gump is a simple man with a low I.Q. but good intentions. He is running through childhood with his best and only friend Jenny. His 'mama' teaches him the ways of life and leaves him to choose his destiny. Forrest joins the army for service in Vietnam, finding new friends called Dan and Bubba, he wins medals, creates a famous shrimp fishing fleet, inspires people to jog, starts a ping-pong craze, creates the smiley, writes bumper stickers and songs, donates to people and meets the president several times. However, this is all irrelevant to Forrest who can only think of his childhood sweetheart Jenny Curran, who has messed up her life. Although in the end all he wants to prove is that anyone can love anyone."
    # go to page 2
    at.button[1].click().run()
    assert at.session_state.page == 'page2'

    # test page 2
    assert at.title[0].value == 'Result'

    # go back to page 1
    at.button[10].click().run()
    assert at.session_state.page == 'home'
