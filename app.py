import streamlit as st
from main import agent_executor  # Pulls your working agent from main.py

# Setup the basic webpage headers
st.title("🤖 My Research Assistant")
st.write("Type a topic below to search the web and save the results.")

# Create a simple text box for the user
user_query = st.text_input("Enter your research topic:")

# Create a button to kick off the agent
if st.button("Run Research"):
    
    # Check if the user forgot to type something
    if not user_query.strip():
        st.warning("Please enter a topic first!")
        
    else:
        # Show a simple loading message while it runs
        with st.spinner("Searching and writing file..."):
            
            # Send the input to your working backend agent loop
            result = agent_executor.invoke({"query": user_query, "chat_history": []})
            
            # Extract the raw text report text out of the response dictionary
            report_text = result.get("output", "")
            
            # Show a success banner and print the report beautifully on screen
            st.success("Done!")
            
            # 📥 NEW FEATURE: The Download Button Actions
            st.download_button(
                label="📥 Download Research Report (.txt)",
                data=report_text,
                file_name="research_report.txt",
                mime="text/plain"
            )
            
            st.write("---")  # Adds a clean visual dividing line
            st.subheader("Results View:")
            st.markdown(report_text)