def insert_record(record, collection):
    result = collection.insert_one(record)
    print(f"Inserted record with id: {result.inserted_id}")


def get_record(query, collection):
    result = collection.find_one(query)
    if result:
        return result
    return None

def update_record(query, update, collection):
    result = collection.update_one(query, {"$set": update})
    print(f"Modified {result.modified_count} documents.")


def delete_record(query, collection):
    result = collection.delete_one(query)
    print(f"Deleted {result.deleted_count} documents.")
