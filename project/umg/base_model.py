from project.umg import db


class ModelActionMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    def post_update(self):
        pass

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)

        self.post_update()

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
