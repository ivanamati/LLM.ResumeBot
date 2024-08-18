# IvyBot - AI Assistant for Job Search

IvyBot is an AI assistant designed to assist Ivana in her job search by providing recruiters with relevant and concise information about her academic background, programming experience, and skills. IvyBot uses a Retrieval-Augmented Generation (RAG) approach combined with GPT-4 to answer questions effectively.

## Overview

IvyBot leverages a combination of text embedding and vector search technologies to retrieve and present the most relevant information about Ivana in response to recruiters' queries. The assistant is tuned to provide specific details about Ivana’s projects, education, and skills, ensuring that recruiters receive accurate and helpful information.

### Key Features

- **Personalized Responses**: IvyBot is tailored to Ivana’s profile, providing detailed answers related to her academic and professional background.
- **RAG Approach**: The assistant uses a RAG approach, combining the power of GPT-4 for generation with a FAISS vector store for retrieval, ensuring precise and contextually relevant answers.
- **Contextual Information Retrieval**: IvyBot retrieves relevant information from a vector store, embedding chunks of Ivana’s biography to provide accurate answers.
- **Predefined System Template**: The assistant operates based on a strict set of instructions to ensure the accuracy and relevance of the information provided.

## How It Works

### 1. Retrieving Information

The `retriever_RAG` function loads Ivana’s biography, splits it into chunks, and embeds these chunks using OpenAI embeddings. The embeddings are stored in a FAISS vector index, which is used to retrieve relevant information in response to queries.

### 2. Generating Answers

The `generate_answer` function utilizes GPT-4 to generate answers based on the retrieved information. It applies a predefined system template to ensure the answers are consistent, accurate, and relevant to Ivana’s profile.

### Important Notes
IvyBot provides information based only on the content in my_bio2.txt. It does not fabricate or guess information.
If IvyBot does not have enough information to answer a question, it will politely direct recruiters to contact Ivana directly.
