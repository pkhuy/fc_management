
class Permission():
    def __init__(self, id: int, name: str, entity: str):
        self.id = id
        self.name = name
        self.entity = entity
        #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        #group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def get_as_json(self):
        return{
                "id": self.id,
                "name": self.name,
                "entity": self.entity
            }