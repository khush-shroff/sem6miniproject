
import streamlit as st
from questions import questions
from recommender import get_recommendation

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

        st.write("### Score Breakdown")
        
        logical, numerical, verbal = result["scores"]

        max_score = max(logical, numerical, verbal, 1)  # avoid division by zero
        max_score=60
        st.write(f"🧠 Logical Ability: {logical}")
        st.progress(logical / max_score)

        st.write(f"🔢 Numerical Ability: {numerical}")
        st.progress(numerical / max_score)

        st.write(f"🗣️ Verbal Ability: {verbal}")
        st.progress(verbal / max_score)

        st.write("### Career Options")
        for c in result["careers"]:
            st.write("-",c)

        st.write("### Roadmap")
        st.write(result["roadmap"])

        st.write("### Skills Required")
        for s in result["skills"]:
            st.write("-",s)
