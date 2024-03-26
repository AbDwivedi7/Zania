import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.llms.openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = "gpt-3.5-turbo"


def get_open_ai_model(documents, sources):
    try:
        embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)
        v_store = Chroma.from_texts(documents, embeddings, metadatas=[{"source": s} for s in sources])
        retriever = v_store.as_retriever()
        retriever.search_kwargs = {'k':2}
        llm = OpenAI(name=OPENAI_MODEL_NAME, api_key = OPENAI_API_KEY, streaming=True)
        model = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        return model

    except Exception as e:
        print("Exception in get_open_ai_model", e)
        return None
        
def get_open_ai_answer(documents, questions):
    try:
        model = get_open_ai_model(documents=documents[0], sources=documents[1])
        if model is None:
            return {}
        
        answers = {}
        for question in questions:
            result = model({"question":question["content"]}, return_only_outputs=True)
            answers[question["content"]] = result['answer']
            
        return answers
    except Exception as e:
        print("Exception in get_open_ai_answer", e)
        return {}