from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage


def rag(open_api_key):
    # Load the document embed each chunk and load it into the vector store.
    raw_documents = TextLoader("my_bio1.txt").load()
    # Split it into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 900, chunk_overlap = 200, length_function = len)
    documents = text_splitter.split_documents(raw_documents)
    #print(documents[4])
    # Embedd the chunks and load it into vector store
    embeddings = OpenAIEmbeddings(api_key=open_api_key)
    # Pass the documents and embeddings inorder to create FAISS vector index
    vectorindex_openai = FAISS.from_texts(documents, embeddings)
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

    retriever = rag(open_api_key)
    data = retriever.invoke(query)
        
    SYSTEM_TEMPLATE = """
        You are IvyBot, an AI assistant dedicated to assisting Ivana in her job search by providing recruiters with relevant and concise information. 
        If you do not know the answer, politely admit it and let recruiters know how to contact Ivana to get more information directly from her. 
        Don't put "IvyBot" or a breakline in the front of your answer. Don't make informations up!

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
