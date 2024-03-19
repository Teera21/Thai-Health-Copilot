import pathlib
from typing import Any
import argparse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import sys
sys.path.append(f'{os.getcwd()}')
from config import config as cfg
import httpcore
setattr(httpcore, 'SyncHTTPTransport', Any)
from langchain_community.document_loaders import (
    CSVLoader,
    NotebookLoader,
    PythonLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    UnstructuredWordDocumentLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredPowerPointLoader,
    UnstructuredODTLoader,
    NotebookLoader,
    UnstructuredFileLoader
)

FILE_LOADER_MAPPING = {
    "csv": (CSVLoader, {"encoding": "utf-8"}),
    "doc": (UnstructuredWordDocumentLoader, {}),
    "docx": (UnstructuredWordDocumentLoader, {}),
    "epub": (UnstructuredEPubLoader, {}),
    "html": (UnstructuredHTMLLoader, {}),
    "md": (UnstructuredMarkdownLoader, {}),
    "odt": (UnstructuredODTLoader, {}),
    "pdf": (PyPDFLoader, {}),
    "ppt": (UnstructuredPowerPointLoader, {}),
    "pptx": (UnstructuredPowerPointLoader, {}),
    "txt": (TextLoader, {"encoding": "utf8"}),
    "ipynb": (NotebookLoader, {}),
    "py": (PythonLoader, {}),
}

from googletrans import Translator

translator = Translator()

parser = argparse.ArgumentParser(description='Chat Bot with Your Document')
parser.add_argument('--translate', action='store_true', help='Enable verbose mode')
args = parser.parse_args()

os.environ['HYDRA_FULL_ERROR'] = '1'

class LoadDocumentToChroma:

    """ คลาสนี้เอาไว้สำหรับ แปลงข้อมูลทั้งหมดในโฟลเดอร์ ไฟล์ doc, pdf หรืออื่นๆก็รองรับ หลังจาก
     ดึงข้อมูลจากเอกสารมาหมด ก็จะแปลงเป็น vector และสร้าง chroma db มาเก็บไว้ """
    
    def __init__(self,cfg):
        self.cfg = cfg

    """ split text to chnk and adding source data to metadata document """
    def get_document_chunks_from_source(self,text: str,source: str) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = self.cfg.CHUNK_SIZE,
        chunk_overlap  = self.cfg.CHUNK_OVERLAP,
        length_function = len,
        add_start_index = True,  
    )
        document_ls = text_splitter.create_documents([text])
        each_chunk = text_splitter.split_documents(document_ls)

        if args.translate:
            for idx, text in enumerate(each_chunk):
                document_ls[idx].metadata['source'] = source
                document_ls[idx].page_content = translator.translate(document_ls[idx].page_content, to_lang='en', dest='en').text
        else:
            for idx, text in enumerate(each_chunk):
                document_ls[idx].metadata['source'] = source
        return document_ls

    """get all text from all file in folder"""
    def folder_file_to_document(self) -> list[Document]:
        docs = []
        all_documents = []
        directory_path = os.getcwd() + self.cfg.DATA_SOURCE
        file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        for file in file_names:
            txt = ''
            temp_filepath = os.path.join(directory_path, file).replace('\\','/')
            ext = pathlib.Path(temp_filepath).suffix.lower().replace('.','')
            if ext in FILE_LOADER_MAPPING:
                loader_class, loader_args = FILE_LOADER_MAPPING[ext]
                loader = loader_class(temp_filepath,**loader_args)
                documents_ls = loader.load()
                for text in documents_ls:
                    txt += text.page_content
                all_documents.extend(self.get_document_chunks_from_source(text =txt,source= temp_filepath))
                
            else:
                loader = UnstructuredFileLoader(temp_filepath)
                documents_ls = loader.load()
                for text in documents_ls:
                    txt += text.page_content
                all_documents.extend(self.get_document_chunks_from_source(text =txt,source= temp_filepath))

        return all_documents
    
    """ embedding all document to vector and save this in chroma vector database """
    def ingest_document_to_chroma(self) -> None:
        embedding_hf = HuggingFaceEmbeddings(model_name=self.cfg.EMBEDDING_MODEL)
        all_documents = self.folder_file_to_document()
        Chroma.from_documents(all_documents,
                       embedding_hf,
                       persist_directory= os.getcwd() + self.cfg.CHROMA_PATH)


if __name__ == '__main__':
    LoadDoc = LoadDocumentToChroma(cfg=cfg)
    LoadDoc.ingest_document_to_chroma() 

