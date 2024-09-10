import json
from typing import Dict, List
from app.schemas.question import Question

def load_questions() -> Dict[str, List[Question]]:
    with open("/home/ubuntu/puzzle/fastapi_Quiz_app/app/data/questions.json", "r") as f:
        data = json.load(f)
    
    questions_by_category = {}
    for category, category_questions in data.items():
        questions_by_category[category] = [
            Question(
                id=f"{category}_{i}",
                text=q["question"],
                options=q["options"],
                correct_answer=q["answer"],
                category=category,
                set_number=1  # All questions are in set 1 for now
            )
            for i, q in enumerate(category_questions)
        ]
    
    return questions_by_category

questions = load_questions()