import os
import json
import math
from google import genai

class SemanticFilter:
    def __init__(self, reference_file="src/defenses/reference_payloads.json", model="gemini-embedding-2-preview"):
        """Initializes the filter by computing embeddings for the reference vectors."""
        self.client = genai.Client()
        self.model = model
        
        # Load the reference payload texts
        with open(reference_file, "r", encoding="utf-8") as f:
            self.reference_texts = json.load(f)
            
        print(f"Initializing SemanticFilter with {len(self.reference_texts)} reference vectors...")
        
        # Compute embeddings for references synchronously during init
        result = self.client.models.embed_content(
            model=self.model,
            contents=self.reference_texts
        )
        self.reference_embeddings = [e.values for e in result.embeddings]
            
    def cosine_similarity(self, vec1, vec2):
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = math.sqrt(sum(a * a for a in vec1))
        mag2 = math.sqrt(sum(b * b for b in vec2))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)
        
    async def get_max_similarity(self, prompt: str) -> float:
        """Returns the maximum cosine similarity score against any reference vector."""
        if not prompt.strip():
            return 0.0
            
        result = await self.client.aio.models.embed_content(
            model=self.model,
            contents=prompt
        )
        embedding = result.embeddings[0].values
        
        max_sim = -1.0
        for ref_emb in self.reference_embeddings:
            sim = self.cosine_similarity(embedding, ref_emb)
            if sim > max_sim:
                max_sim = sim
                
        return max_sim
        
    async def is_malicious(self, prompt: str, threshold: float = 0.85) -> bool:
        """Convenience function returning True if max similarity exceeds threshold."""
        score = await self.get_max_similarity(prompt)
        return score >= threshold
