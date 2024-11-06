import streamlit as st
import predictor as pr
from predictor import TextDataProcessor
import advanced as ad
import generate_summary as gs

pr.load_dependencies()

st.title("Persona-Find")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'summary_shown' not in st.session_state:
    st.session_state.summary_shown = 0

if 'toggle' not in st.session_state:
    st.session_state.toggle = False

if 'toggle_count' not in st.session_state:
    st.session_state.toggle_count = 0

if 'user_prompt' not in st.session_state:
    st.session_state.user_prompt = 0

if 'final_response' not in st.session_state:
    st.session_state.final_response = ""

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.toggle == False:
    prompt = st.chat_input("Enter the topic of your choice...")
    if prompt is not None:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("human"):
            st.markdown(prompt)
        
        st.session_state.user_prompt = prompt
        st.session_state.summary_shown = TextDataProcessor().process_input("training.txt", prompt, 1)

        # Initialize response as an empty string in case of an error in fetching summaries
        response = ""

        with st.chat_message("assistant"):
            if st.session_state.summary_shown == 1:
                # Attempt to fetch advanced summary
                response = ad.get_advanced_summary(prompt, 400)
                st.markdown(response)
                st.session_state.final_response = response[:]
            else:
                # Attempt to fetch basic summary with error handling
                try:
                    response = gs.gen_summary(prompt)
                    st.markdown(response)
                    st.session_state.final_response = response[:]
                except Exception as e:
                    print("Error is: ", e)  
                    response = e

        # Append response to session messages
        st.session_state.messages.append({"role": "assistant", "content": response})

elif st.session_state.toggle == True and st.session_state.toggle_count == 1:
    print("After toggle, in else statement")
    prompt = st.session_state.user_prompt
    similarity = TextDataProcessor()

    response = ""

    with st.chat_message("assistant"):
        if st.session_state.summary_shown == 1:
            response = ad.get_advanced_summary(prompt, 400)
            st.markdown(response)
            st.session_state.final_response = response[:]
        else:
            try:
                response = gs.gen_summary(prompt)
                st.session_state.final_response = response[:]
                st.markdown(response)
            except Exception as e:
                print("Error is: ", e)
                response = "An error occurred while generating the summary."

    st.session_state.messages.append({"role": "assistant", "content": response})

# Toggle button functionality
if st.session_state.toggle_count == 0:
    if st.button("Toggle Summary"):
        st.session_state.toggle = True
        st.session_state.summary_shown = 1 - st.session_state.summary_shown  # Toggle the state
        st.session_state.toggle_count += 1
        st.rerun()  # Rerun the script to reflect the change

# Done button functionality
if st.button("Done"):
    st.session_state.toggle = False
    st.session_state.toggle_count = 0
    pr.TextDataProcessor.append_summary(None, st.session_state.user_prompt, ad.format_summary(st.session_state.final_response), st.session_state.summary_shown, 'training.txt')
    st.rerun()
