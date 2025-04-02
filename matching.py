import numpy as np
from sentence_transformers import SentenceTransformer

class TaskMatcher:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def calculate_similarity(self, task_requirements, user_skills):
        req_embedding = self.model.encode(task_requirements)
        user_embedding = self.model.encode(user_skills)
        similarity = np.dot(req_embedding, user_embedding) / (
            np.linalg.norm(req_embedding) * np.linalg.norm(user_embedding)
        )
        return float(similarity)