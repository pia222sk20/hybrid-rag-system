"""
Document Loader for DOCX files
"""
import os
from pathlib import Path
from typing import List, Dict
from docx import Document
from docx.document import Document as DocumentType
from config.settings import settings
from src.utils.logger import log


class DocumentLoader:
    """Load and parse DOCX documents"""
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path or settings.data_raw_path
        
    def load_all_documents(self) -> List[Dict]:
        """Load all DOCX files from data directory"""
        documents = []
        data_dir = Path(self.data_path)
        
        if not data_dir.exists():
            log.error(f"Data directory not found: {data_dir}")
            return documents
        
        docx_files = list(data_dir.glob("*.docx"))
        log.info(f"Found {len(docx_files)} DOCX files")
        
        for file_path in docx_files:
            try:
                doc_data = self.load_document(str(file_path))
                if doc_data:
                    documents.append(doc_data)
                    log.info(f"Loaded: {file_path.name}")
            except Exception as e:
                log.error(f"Failed to load {file_path.name}: {e}")
        
        return documents
    
    def load_document(self, file_path: str) -> Dict:
        """Load a single DOCX document"""
        try:
            doc = Document(file_path)
            file_name = Path(file_path).name
            
            # Extract text with structure
            content = self._extract_structured_content(doc)
            
            return {
                "file_name": file_name,
                "file_path": file_path,
                "content": content,
                "full_text": "\n".join([p["text"] for p in content if p["text"].strip()]),
                "metadata": {
                    "source": file_name,
                    "total_paragraphs": len(content),
                }
            }
        except Exception as e:
            log.error(f"Error loading document {file_path}: {e}")
            return None
    
    def _extract_structured_content(self, doc: DocumentType) -> List[Dict]:
        """Extract content with heading hierarchy"""
        content = []
        current_section = None
        paragraph_index = 0
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            
            # Detect heading style
            style_name = para.style.name.lower() if para.style else ""
            is_heading = "heading" in style_name
            heading_level = 0
            
            if is_heading:
                # Extract heading level (e.g., "Heading 1" -> 1)
                try:
                    heading_level = int(style_name.split()[-1])
                except:
                    heading_level = 1
                current_section = text
            
            content.append({
                "text": text,
                "paragraph_index": paragraph_index,
                "is_heading": is_heading,
                "heading_level": heading_level,
                "section": current_section,
                "style": para.style.name if para.style else "Normal"
            })
            paragraph_index += 1
        
        return content


if __name__ == "__main__":
    # Test document loading
    loader = DocumentLoader()
    docs = loader.load_all_documents()
    
    log.info(f"Total documents loaded: {len(docs)}")
    for doc in docs:
        log.info(f"- {doc['file_name']}: {doc['metadata']['total_paragraphs']} paragraphs")
