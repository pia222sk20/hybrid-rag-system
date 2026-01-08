"""
Semantic Chunker for intelligent text splitting
"""
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import settings
from src.utils.logger import log


class SemanticChunker:
    """Intelligent text chunking with heading awareness"""
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True,
        )
    
    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """Chunk all documents with metadata preservation"""
        all_chunks = []
        
        for doc in documents:
            chunks = self._chunk_single_document(doc)
            all_chunks.extend(chunks)
            log.debug(f"Created {len(chunks)} chunks from {doc['file_name']}")
        
        log.info(f"Total chunks created: {len(all_chunks)}")
        return all_chunks
    
    def _chunk_single_document(self, doc: Dict) -> List[Dict]:
        """Chunk a single document with structure awareness"""
        chunks = []
        content = doc["content"]
        
        # Group paragraphs by section
        sections = self._group_by_sections(content)
        
        chunk_id = 0
        for section_title, paragraphs in sections.items():
            section_text = "\n".join([p["text"] for p in paragraphs])
            
            # Split section text into chunks
            text_chunks = self.text_splitter.split_text(section_text)
            
            for i, chunk_text in enumerate(text_chunks):
                chunk_metadata = {
                    "chunk_id": f"{doc['file_name']}_chunk_{chunk_id}",
                    "source": doc["file_name"],
                    "file_path": doc["file_path"],
                    "section_title": section_title or "Introduction",
                    "chunk_index": i,
                    "total_chunks_in_section": len(text_chunks),
                }
                
                chunks.append({
                    "text": chunk_text,
                    "metadata": chunk_metadata
                })
                chunk_id += 1
        
        return chunks
    
    def _group_by_sections(self, content: List[Dict]) -> Dict[str, List[Dict]]:
        """Group paragraphs by their section headers"""
        sections = {}
        current_section = None
        current_paragraphs = []
        
        for item in content:
            if item["is_heading"]:
                # Save previous section
                if current_section or current_paragraphs:
                    section_key = current_section or "Introduction"
                    sections[section_key] = current_paragraphs
                
                # Start new section
                current_section = item["text"]
                current_paragraphs = []
            else:
                current_paragraphs.append(item)
        
        # Save last section
        if current_section or current_paragraphs:
            section_key = current_section or "Introduction"
            sections[section_key] = current_paragraphs
        
        return sections


if __name__ == "__main__":
    from src.core.document_loader import DocumentLoader
    
    # Test chunking
    loader = DocumentLoader()
    docs = loader.load_all_documents()
    
    chunker = SemanticChunker()
    chunks = chunker.chunk_documents(docs)
    
    log.info(f"Total chunks: {len(chunks)}")
    if chunks:
        log.info(f"Sample chunk: {chunks[0]['text'][:200]}...")
        log.info(f"Sample metadata: {chunks[0]['metadata']}")
