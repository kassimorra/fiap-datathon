# fiap-datathon


## Objetivo  

Este projeto visa implementar um projeto de MLOps para prever os próximos cliques de notícias de um usuário.

## O que foi utilizado

Neste projeto, foram aplicadas técnicas de tratamento de dados e ETL para ingestão no banco de dados **PostgreSQL**.  

Toda a arquitetura foi conteinerizada, incluindo o **pipeline de dados**, o **modelo de machine learning**, a **feature store** e a interface **Streamlit**. A orquestração dos containers foi realizada via **Docker Compose**, garantindo a comunicação entre os serviços por meio das portas apropriadas.  

### 🔹 Feature Store  
Para a **feature store**, utilizamos o **Feast**, permitindo a gestão e materialização eficiente das features. A interface para simulação de usuários e controle da materialização da feature store foi desenvolvida em **Streamlit**.  

### 🔹 Comunicação Entre Serviços  
A comunicação entre os containers ocorre via **Web API**, implementada com **FastAPI** em Python.  

### 🔹 Modelo de Machine Learning  
O modelo utilizado neste projeto é baseado em **Content-Based Filtering**, permitindo recomendar notícias relevantes ao usuário com base em seu histórico de interesse.  

####
- As notícias são convertidas em **embeddings**.  
- Utilizamos **TF-IDF** para processar os textos.  
- Construímos uma **matriz de similaridade** para identificar conteúdos relevantes.  
- O objetivo é recomendar **notícias mais recentes e ainda não lidas**, alinhadas aos interesses individuais do usuário.  

## Desenho de solução

![Fiap Datathon](fiap_datathon.png)