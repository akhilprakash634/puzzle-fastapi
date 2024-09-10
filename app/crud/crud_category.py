from typing import List, Optional
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category
from app.core.firebase import db

class CRUDCategory:
    def create(self, obj_in: CategoryCreate) -> Category:
        doc_ref = db.collection("categories").document()
        category_data = obj_in.dict()
        doc_ref.set(category_data)
        return Category(id=doc_ref.id, **category_data)

    def get(self, category_id: str) -> Optional[Category]:
        doc = db.collection("categories").document(category_id).get()
        if doc.exists:
            return Category(id=doc.id, **doc.to_dict())
        return None

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Category]:
        docs = db.collection("categories").limit(limit).offset(skip).stream()
        return [Category(id=doc.id, **doc.to_dict()) for doc in docs]

    def update(self, category_id: str, obj_in: CategoryUpdate) -> Optional[Category]:
        category = self.get(category_id)
        if not category:
            return None
        update_data = obj_in.dict(exclude_unset=True)
        db.collection("categories").document(category_id).update(update_data)
        return self.get(category_id)

    def delete(self, category_id: str) -> bool:
        category = self.get(category_id)
        if not category:
            return False
        db.collection("categories").document(category_id).delete()
        return True

category = CRUDCategory()