"""
RAG Chain for Grounded Answer Generation
"""
from typing import List, Dict, Optional
from openai import OpenAI
from config.settings import settings
from src.retrieval.hybrid_retriever import HybridRetriever
from src.utils.logger import log


class RAGChain:
    """RAG Chain with grounded generation and citation"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.retriever = HybridRetriever()
        self.model = settings.llm_model
        log.info(f"Initialized RAGChain with model: {self.model}")
    
    def query(
        self,
        question: str,
        top_k: int = None,
        include_sources: bool = True
    ) -> Dict:
        """
        Process a query through the RAG pipeline
        
        Args:
            question: User question
            top_k: Number of context chunks to use
            include_sources: Whether to include source information
            
        Returns:
            Dict with answer, sources, and metadata
        """
        log.info(f"Processing query: {question}")
        
        # Step 1: Retrieve relevant chunks
        retrieved_chunks = self.retriever.search(question, top_k=top_k)
        
        if not retrieved_chunks:
            return {
                "answer": "죄송합니다. 질문에 답변할 수 있는 관련 문서를 찾을 수 없습니다.",
                "sources": [],
                "confidence": 0.0,
                "retrieved_chunks": 0,
                "model": self.model
            }
        
        log.info(f"Retrieved {len(retrieved_chunks)} relevant chunks")
        
        # Step 2: Build context from retrieved chunks
        context = self._build_context(retrieved_chunks)
        
        # Step 3: Generate answer with LLM
        answer, confidence = self._generate_answer(question, context)
        
        # Step 4: Extract source citations
        sources = self._extract_sources(retrieved_chunks) if include_sources else []
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "retrieved_chunks": len(retrieved_chunks),
            "model": self.model
        }
    
    def _build_context(self, chunks: List[Dict]) -> str:
        """Build context string from retrieved chunks with citations"""
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            source = chunk["metadata"]["source"]
            section = chunk["metadata"].get("section_title", "Unknown")
            text = chunk["text"]
            
            context_parts.append(
                f"[문서 {i}: {source} - {section}]\n{text}\n"
            )
        
        return "\n".join(context_parts)
    
    def _generate_answer(self, question: str, context: str) -> tuple[str, float]:
        """Generate grounded answer using LLM"""
        
        system_prompt = """당신은 제공된 문서만을 기반으로 정확하게 답변하는 AI 어시스턴트입니다.

**중요한 규칙:**
1. 제공된 문서 내용만을 사용하여 답변하세요
2. 문서에 없는 내용은 절대 추가하지 마세요
3. 답변할 때 반드시 출처를 [문서 X]와 같은 형식으로 표시하세요
4. 확실하지 않은 내용은 "문서에서 확인할 수 없습니다"라고 답하세요
5. 한국어로 명확하고 간결하게 답변하세요

답변 형식:
- 주요 답변 내용 [문서 1, 문서 2]
- 추가 설명 [문서 3]
"""
        
        user_prompt = f"""다음 문서들을 참고하여 질문에 답변해주세요:

<문서>
{context}
</문서>

<질문>
{question}
</질문>

답변:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )
            
            answer = response.choices[0].message.content
            
            # Calculate confidence based on response quality
            confidence = self._calculate_confidence(answer, context)
            
            log.debug(f"Generated answer with confidence: {confidence:.2f}")
            return answer, confidence
            
        except Exception as e:
            log.error(f"Error generating answer: {e}")
            return f"답변 생성 중 오류가 발생했습니다: {str(e)}", 0.0
    
    def _calculate_confidence(self, answer: str, context: str) -> float:
        """
        Calculate confidence score based on answer characteristics
        This is a simple heuristic - can be improved with more sophisticated methods
        """
        confidence = 1.0
        
        # Reduce confidence if answer is very short
        if len(answer) < 50:
            confidence -= 0.2
        
        # Reduce confidence if no citations found
        if "[문서" not in answer:
            confidence -= 0.3
        
        # Increase confidence if multiple citations
        citation_count = answer.count("[문서")
        if citation_count >= 2:
            confidence = min(1.0, confidence + 0.1)
        
        # Check for uncertainty phrases
        uncertainty_phrases = ["확인할 수 없", "명확하지 않", "불확실"]
        for phrase in uncertainty_phrases:
            if phrase in answer:
                confidence -= 0.2
        
        return max(0.0, min(1.0, confidence))
    
    def _extract_sources(self, chunks: List[Dict]) -> List[Dict]:
        """Extract unique source information from chunks"""
        sources_dict = {}
        
        for chunk in chunks:
            source = chunk["metadata"]["source"]
            if source not in sources_dict:
                sources_dict[source] = {
                    "file_name": source,
                    "sections": set()
                }
            
            section = chunk["metadata"].get("section_title", "Unknown")
            sources_dict[source]["sections"].add(section)
        
        # Convert to list format
        sources = []
        for source, data in sources_dict.items():
            sources.append({
                "file_name": data["file_name"],
                "sections": list(data["sections"])
            })
        
        return sources
    
    def get_retriever_stats(self) -> Dict:
        """Get retriever statistics"""
        return self.retriever.get_stats()


if __name__ == "__main__":
    from src.core.document_loader import DocumentLoader
    from src.core.semantic_chunker import SemanticChunker
    
    # Test RAG chain
    loader = DocumentLoader()
    docs = loader.load_all_documents()
    
    if docs:
        chunker = SemanticChunker()
        chunks = chunker.chunk_documents(docs)
        
        rag = RAGChain()
        rag.retriever.reset()
        rag.retriever.index_chunks(chunks)
        
        # Test query
        result = rag.query("이 문서의 주요 내용을 요약해주세요")
        
        log.info(f"\n질문: 이 문서의 주요 내용을 요약해주세요")
        log.info(f"\n답변: {result['answer']}")
        log.info(f"\n신뢰도: {result['confidence']:.2f}")
        log.info(f"\n출처: {result['sources']}")
    else:
        log.warning("No documents found. Please add DOCX files to data/raw/")
