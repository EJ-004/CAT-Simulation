class Question:
    def __init__(self, id, question="", choices=None, ans='', b=0.0, a=1.0, c=0.0, d=1.0):
        self.id = id
        self.question = question
        self.choices = choices if choices is not None else []
        self.answer = ans
        self.difficulty = b
        self.discrimination = a
        self.lower_asymptote = c
        self.upper_asymptote = d

class ItemBank:
    def __init__(self, items=None):
        self.items = items if items is not None else []

    def update(self, items):
        self.items = items

    def add_items(self, items):
        for item in items:
            self.items.append(item)

    def has_items(self):
        return True if len(self.items) > 0 else False

    def item_amount(self):
        return len(self.items)