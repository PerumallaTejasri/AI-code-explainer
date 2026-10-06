import streamlit as st
import os
from google import genai

st.set_page_config(
    page_title="AI Code Explainer",
    page_icon="🤖",
    layout="wide"
)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)

st.title("🤖 AI Code Explainer")
st.write("Understand and analyze your code using Artificial Intelligence.")

st.sidebar.header("Settings")

language = st.sidebar.selectbox(
    "Select Programming Language",
    [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "SQL",
        "Other"
    ]
)

explanation_type = st.sidebar.selectbox(
    "Explanation Type",
    [
        "Simple Explanation",
        "Line-by-Line Explanation",
        "Detailed Explanation",
        "Beginner Friendly Explanation"
    ]
)

uploaded_file = st.file_uploader(
    "Upload Code File",
    type=["py", "java", "c", "cpp", "js", "html", "css", "sql", "txt"]
)

code = ""

if uploaded_file:
    try:
        code = uploaded_file.read().decode("utf-8")
    except:
        st.error("Unable to read the file.")

code = st.text_area(
    "Enter or Paste Your Code",
    value=code,
    height=350,
    placeholder="Paste your code here..."
)

def explain_code(code, language, explanation_type):

    prompt = f"""
You are an expert programming teacher.

Analyze this {language} code.

Give a {explanation_type}.

CODE:
{code}

Explain the following:

1. Purpose of the program
2. How the program works
3. Important lines of code
4. Programming concepts used
5. Input and output
6. Time complexity
7. Space complexity
8. Errors or bugs, if any
9. Suggestions for improvement

Use simple English suitable for a college student.
Use headings and code examples where required.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
if st.button("🤖 Explain Code", type="primary"):

    if not API_KEY:
        st.error("Gemini API key is not configured.")

    elif not code.strip():
        st.warning("Please enter or upload some code.")

    else:

        with st.spinner("AI is analyzing your code..."):

            try:
                explanation = explain_code(
                    code,
                    language,
                    explanation_type
                )

                st.success("Code analysis completed!")

                st.subheader("💻 Your Code")
                st.code(code, language=language.lower())

                st.subheader("🤖 AI Explanation")
                st.markdown(explanation)

                st.download_button(
                    "⬇️ Download Explanation",
                    explanation,
                    file_name="code_explanation.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {e}")
st.markdown("---")
st.caption("AI Code Explainer | Powered by Gemini")