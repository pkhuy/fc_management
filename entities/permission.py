
class Permission():
    def __init__(self, id: int, name: str, content_type_id: str, codename: str):
        id = id
        name = name
        content_type_id = content_type_id
        codename = codename
        #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        #group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def get_as_json(self):
        return{
            "permissionID": self.id,
            "permissionname": self.name,
            "content_type_id": self.content_type_id,
            "codename": self.codename
        }