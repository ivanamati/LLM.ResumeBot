from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage


def retriever_RAG(open_api_key):
    """this function loads the document, creates chunks, embed each chunk 
    and load it into the vector store and make a retriever"""
    raw_documents = TextLoader("my_bio2.txt").load()
    # Split it into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 900, chunk_overlap = 200, length_function = len)
    documents = text_splitter.split_documents(raw_documents)
    # Pass the documents and embeddings to create FAISS vector index
    vectorindex_openai = FAISS.from_documents(documents, OpenAIEmbeddings(api_key=open_api_key))
    # Save the vectorstore object locally
    vectorindex_openai.save_local("vectorindex_openai")
    # Load the vectorstore object
    vectorstore = FAISS.load_local("vectorindex_openai", OpenAIEmbeddings(api_key=open_api_key),allow_dangerous_deserialization=True)
    # Retrieve the information from the vectorestore
    retriever = vectorstore.as_retriever(k=2)
    return retriever


def generate_answer(query,open_api_key):

    llm = ChatOpenAI(temperature=0,
    model="gpt-4o",
    openai_api_key=open_api_key)

    retriever = retriever_RAG(open_api_key)
    data = retriever.invoke(query)
        
    SYSTEM_TEMPLATE = """
    You are IvyBot, an AI assistant dedicated to assisting Ivana in her job search 
    by providing recruiters with relevant and concise information and making her a good and valuable candidate for the company. 

    Your tasks are following:
    1. Answer provide informatona about Ivana only.
    2. When asked to provide information about projects count at least 4 of them.
    3. When asked about education count both - linguistical and developing. 
    4. When asked about skills count developing, scholar and personal.
    5. If you do not know the answer, politely admit it and let recruiters know how to contact Ivana to get more information directly from her. 

    Don't put "IvyBot" or a breakline in the front of your answer. Don't make informations up!
    When you are asked about IvyBot, provide explanation that you are made using RAG approach and GPT-4o to aks questions about Ivana and demonstrating her coding skills. 

    To answer the recruiters questions about Ivana use ONLY the following informations: 
    <informations>
    {context}
    </informations> 

    """

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_TEMPLATE,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    document_chain = create_stuff_documents_chain(llm, question_answering_prompt)

    answer = document_chain.invoke(
        {
            "context": data,
            "messages": [
                HumanMessage(content=query)
            ],
        }
    )
    print()
    print(answer)
    return answer
