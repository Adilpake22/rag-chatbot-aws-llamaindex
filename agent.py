import os
import boto3
import tempfile
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings, Document
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pypdf import PdfReader

load_dotenv()

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

def setup_llm_and_embeddings():
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
    llm = Groq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
    Settings.llm = llm
    Settings.embed_model = embed_model
    return llm, embed_model

def read_file(file_path: str):
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return [Document(text=text)]
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [Document(text=f.read())]

def ingest_from_s3(filename: str):
    try:
        setup_llm_and_embeddings()
        s3 = boto3.client('s3', region_name=AWS_REGION)
        
        suffix = os.path.splitext(filename)[1]
        tmp_path = os.path.join(tempfile.gettempdir(), f"rag_{filename.replace('/', '_')}")
        
        s3.download_file(S3_BUCKET, filename, tmp_path)
        documents = read_file(tmp_path)
        index = VectorStoreIndex.from_documents(documents)
        
        try:
            os.remove(tmp_path)
        except:
            pass
            
        return index, f"Successfully ingested {filename} from S3"
    except Exception as e:
        return None, f"S3 ingestion error: {str(e)}"
        
def ingest_documents(file_path: str):
    try:
        setup_llm_and_embeddings()
        documents = read_file(file_path)
        index = VectorStoreIndex.from_documents(documents)
        return index, f"Successfully ingested {len(documents)} document(s)"
    except Exception as e:
        return None, f"Ingestion error: {str(e)}"

def list_s3_documents():
    try:
        s3 = boto3.client('s3', region_name=AWS_REGION)
        response = s3.list_objects_v2(Bucket=S3_BUCKET)
        if 'Contents' not in response:
            return []
        return [obj['Key'] for obj in response['Contents']]
    except Exception as e:
        return []

def query_rag(index, user_query: str):
    try:
        if index is None:
            return "Please upload a document first."
        setup_llm_and_embeddings()
        query_engine = index.as_query_engine(
            similarity_top_k=3,
            response_mode="compact"
        )
        response = query_engine.query(user_query)
        result = str(response)
        result = result.encode('utf-8', errors='ignore').decode('utf-8')
        return result
    except Exception as e:
        return f"Query error: {str(e)}"