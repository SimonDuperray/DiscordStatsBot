class VoiceChannel:
    def __init__(self, id, name, position, bitrate, user_limit, category_id):
        self.id = id
        self.name = name
        self.position = position
        self.bitrate = bitrate
        self.user_limit = user_limit
        self.category_id = category_id

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def get_bitrate(self):
        return self.bitrate

    def get_user_limit(self):
        return self.user_limit

    def get_category_id(self):
        return self.get_category_id()
