
class Item:
    def __init__(self, id: str, title: str, description: str,
            status: str, last_modified_date: str) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.last_modified_date = last_modified_date

