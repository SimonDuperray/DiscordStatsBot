class TextChannel:
    def __init__(self, id, name, position, nsfw):
        self.id = id
        self.name = name
        self.position = position
        self.nsfw = nsfw

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def get_nsfw(self):
        return self.nsfw
