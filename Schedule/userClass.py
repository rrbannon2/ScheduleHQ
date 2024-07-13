class User():

    users = {}
    @staticmethod
    def add_user(user):
        User.users[user.user_id] = user

    def __init__(self, user_info):
        self.user_id = user_info["user_id"]
        self.email = user_info["email"]
        self.organization = user_info["organization"]
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False
        self.tokens = []
        
        User.add_user(self)
    
    def get_id(self):
        return str(self.user_id)
    
    def get_organization(self):
        return str(self.organization)