from bson import ObjectId
from datetime import datetime

def serialize_doc(doc):
    # Handle dict
    if isinstance(doc, dict):
        serialized = {}
        for k, v in doc.items():
            if isinstance(v, ObjectId):
                serialized[k] = str(v)
            elif isinstance(v, datetime):
                serialized[k] = v.isoformat()
            elif isinstance(v, dict):
                serialized[k] = serialize_doc(v)
            elif isinstance(v, list):
                serialized[k] = [serialize_doc(i) for i in v]
            else:
                serialized[k] = v
        # Rename _id → id for clarity
        if "_id" in serialized:
            serialized["id"] = serialized.pop("_id")
        return serialized
    
    # Handle list
    if isinstance(doc, list):
        return [serialize_doc(i) for i in doc]
    
    # Handle single ObjectId
    if isinstance(doc, ObjectId):
        return str(doc)
    
    # Handle datetime
    if isinstance(doc, datetime):
        return doc.isoformat()
    
    # Fallback
    return doc
