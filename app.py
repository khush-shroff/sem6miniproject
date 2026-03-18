

import streamlit as st
from questions import questions
from recommender import get_recommendation
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Career Guidance", layout="wide")

st.title("🎯 Advanced Career Guidance System")

progress = st.progress(0)

responses = []

for i,q in enumerate(questions):
    st.write(f"Q{i+1}: {q['question']}")
    ans = st.radio("Select:", q["options"], index=None, key=i)
    if ans is not None:
       responses.append(q["scores"][q["options"].index(ans)])
    else:
        responses.append([0,0,0])
    progress.progress((i+1)/len(questions))

interest = st.selectbox("Select your career interest:",
["Undecided","Engineer","Doctor","Scientist","CA","Entrepreneur","Lawyer","Designer","Writer","Diploma Engineer"])

if st.button("Generate Result"):
    if None in [st.session_state.get(i) for i in range(len(questions))]:
        st.error("Please answer all questions before submitting.")
    else:
        result = get_recommendation(responses, interest)

        st.success(f"Recommended Path: {result['stream']}")

        st.write("### 📊 Aptitude Analysis")

        logical, numerical, verbal = result["scores"]

        data = {
        "Category": ["Logical", "Numerical", "Verbal"],
        "Score": [logical, numerical, verbal]
        }
        dominant = max(
        [("Logical", logical), ("Numerical", numerical), ("Verbal", verbal)],
        key=lambda x: x[1]
        )

        st.success(f"Your strongest area is: {dominant[0]}")
        df = pd.DataFrame(data)
       
        st.write("### 📈 Score Comparison")
        st.bar_chart(df.set_index("Category"))
        fig, ax = plt.subplots()
        ax.pie(df["Score"], labels=df["Category"], autopct='%1.1f%%')
        ax.set_title("Aptitude Distribution")

        st.pyplot(fig)
        dominant = df.loc[df["Score"].idxmax()]["Category"]
       

        st.write("### Career Options")
        for c in result["careers"]:
            st.write("-",c)

        st.write("### Roadmap")
        st.write(result["roadmap"])

        st.write("### Skills Required")
        for s in result["skills"]:
            st.write("-",s)

