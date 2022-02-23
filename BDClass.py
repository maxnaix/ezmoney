import os


class BDClass():
    def __init__(self):
        self.bdUsers = {}
        self.path_bd = "data/users/"

    def load(self):
        files = os.listdir(self.path_bd)
        for f in files:
            with open(self.path_bd+f) as file:
                chat_id = file.readline()
            if chat_id == "":
                self.bdUsers[f] = None
            else:
                self.bdUsers[f] = int(chat_id)

    def update(self, name, chat_id):
        if chat_id is not None:
            self.bdUsers[name] = chat_id
            with open(self.path_bd+name, 'w') as file:
                f = file.writelines(str(chat_id))
        else:
            self.bdUsers[name] = None
            with open(self.path_bd+name, 'w') as file:
                pass

    def is_enabled(self, name):
        if name in self.bdUsers:
            return True
        return False

    def is_registered(self, name):
        if self.is_enabled(name):
            if self.bdUsers[name] is not None:
                return True
        return False

    def get_all_chats(self):
        lst = []
        for _, chat in self.bdUsers.items():
            if chat is not None:
                lst.append(chat)
        return lst
