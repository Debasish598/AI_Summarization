import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader


## sstreamlit APP
st.set_page_config(page_title="Summarize Text From YT or Website", page_icon=":guardsman:", layout="wide")
st.title("Summarize Text From YT or Website")
st.subheader('Summarize URL')


## Get the Groq API Key and url(YT or website)to be summarized
with st.sidebar:
    groq_api_key=st.text_input("Groq API Key",value="",type="password")

generic_url=st.text_input("URL",label_visibility="collapsed")


## Gemma Model Using Groq API
if groq_api_key.strip():
    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)
else:
    st.error("Please provide a valid Groq API Key.")

prompt_template="""
Provide a summary of the following content in 300 words:
Content:{text}

"""


prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize Text From YT or Website"):
     ## Validate all the inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide a valid Groq API Key and URL.")
    elif not validators.url(generic_url):
          st.error("Please enter a valid Url. It can may be a YT video utl or website url")
    else:
        try:
              with st.spinner("Loading..."):
                    if "youtube.com" in generic_url:
                        loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=False)
                    else:
                        loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                    docs=loader.load()

                    ## Chain For Summarization
                    chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                    output_summary=chain.run(docs)

                    st.success(output_summary)
        
        
        except Exception as e:
            st.exception(f"Exception:{e}")


