from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)

video_id = input("Please enter Youtube Video ID: ")

try:
    trans_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    transcript = " ".join(chunk["text"] for chunk in trans_list)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    embedding = OllamaEmbeddings(model="mxbai-embed-large:latest")
    vector_store = FAISS.from_documents(chunks, embedding)
    reteriver = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    llm = ChatOllama(model="tinyllama:latest")
    prompt = PromptTemplate(
        template="""
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you dont Know.
        {context}
        question: {question}
        """,
        input_variables=["context", "question"],
    )


    def format_doc(retreived):
        context_text = "\n\n".join(doc.page_content for doc in retreived)
        return context_text


    parallel_chain = RunnableParallel(
        {
            "context": reteriver | RunnableLambda(format_doc),
            "question": RunnablePassthrough(),
        }
    )
    praser = StrOutputParser()

    main_chain = parallel_chain | prompt | llm | praser

    question = input("Ask you question related to video")

    answer = main_chain.invoke(question)

    print(answer)
except Exception as e:
    print(f"There is an error: {e}")