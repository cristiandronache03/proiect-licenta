import streamlit as st
from PIL import Image
import neo
import similarity
import NicknameGenerator
import TextToJava
import quotes


def saveFile(name,text):
    with open(name +'.txt', 'w') as f:
        f.write(text)

st.set_page_config(page_title="Transformers in NLP")


# --logo--------
basewidth = 150
img = Image.open("./Assets/logo.png")
width, height = img.size
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
# ---------------

col1, col2 = st.columns(2)

with col1:
    st.title("NLP using transformers")
    
with col2:
    st.image(img,output_format="PNG")


# Using object notation
options = st.sidebar.selectbox(
    "Choose an application?",
    ("Ask&Answer", "AcronymGenerator", "JavaBuddy","QuoteGenerator")
)

with st.sidebar:
    if options == "Ask&Answer":
        st.write("Settings")
        with st.form("form1"):
            st.write("A&A")
            val1 = st.radio("Choose similarity", ["Cosine", "Jaccard"])
            val2 = st.slider("Tolerance",min_value=0.0,max_value=1.0,step=0.1)
            val3 = st.slider("No. returns",min_value=0,max_value=10,step=1)
            
            submitted = st.form_submit_button("Save")  


if options == "Ask&Answer":
    question = st.text_input("Ask me anything:")
    btn_start =st.button("Start")
    if btn_start:
        similar_questions = similarity.search(question, val1, val2, int(val3))
        ans = neo.answer(question)
        st.text(ans)
        with st.container():
            st.text("Others have also asked:")
            for i in range(0,len(similar_questions)):
                with st.expander(similar_questions[i]):
                    st.write(neo.answer(similar_questions[i]))
            
                
elif options == "AcronymGenerator":
    uinput = st.text_input("Write something and I'll come up with an acronym for it")
    btn_start =st.button("Start")
    if btn_start:
        nickname = NicknameGenerator.generate(uinput)
        st.text(nickname)
elif options == "JavaBuddy":
    uinput = st.text_input("Need help building Java functions? I'll help!")
    file_name = st.text_input("Choose a name for the file")
    btn_start =st.button("Start")
    if btn_start:
        java_text = TextToJava.generate(uinput)
        st.text(java_text)
        var = java_text
        saveFile(file_name, var)
else:
    uinput = st.selectbox("Choose a category and I'll come up with a quote.", ("timp", "prietenie", "iubire", "om", "suflet"))
    btn_start =st.button("Start")
    if btn_start:
        quote = quotes.generate(uinput)
        st.text(quote)




