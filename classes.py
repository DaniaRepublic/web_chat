# Stores date and time
class DateTime :
    def __init__(self, date) -> None :
        self.dd = date.day
        self.mm = date.month
        self.yy = date.year
        self.hour = date.hour
        self.min = date.minute
        self.sec = date.second

    def __repr__(self) -> str:
        return f'{self.dd}.{self.mm}.{self.yy}'


# Describes chat instance
class Chat :
    def __init__(self, id : int, users_ids : list, name : str, created : DateTime, desc=None, pic_path=None) -> None :
        self.id = id
        self.users_ids = users_ids
        self.name = name
        self.created = created
        self.desc = desc

    def add_user(self, user_id : int) -> str :
        if user_id in self.users_ids :
            return 'User already in chat.'
    
        self.members_ids.append(user_id)
        return 'Added user successfully.'

    def delete_user(self, user_id : int) -> str :
        if user_id in self.users_ids :
            self.members_ids.remove(user_id)
            return 'Deleted user successfully.'
        
        return 'User not in chat.'

    def set_name(self, name : str) :
        self.name = name
    
    def get_name(self) -> str :
        return self.name

    def set_desc(self, desc : str) :
        self.desc = desc

    def get_gesc(self) -> str :
        return self.desc

    def __repr__(self) -> str :
        return f'<Chat: "{ self.name }">'


# Describes user instance
class User :
    def __init__(self, id : int, name : str, reg_date : DateTime, bio=None, chats_ids=None, pic_path=None) -> None :
        self.id = id
        self.chats_ids = chats_ids
        self.name = name
        self.reg_date = DateTime(reg_date)
        self.bio = bio

    def get_id(self) -> int :
        return self.id

    def get_reg_date(self) -> DateTime :
        return self.reg_date

    def set_bio(self, bio : str) :
        self.bio = bio
    
    def get_bio(self) -> str :
        return self.bio

    def set_name(self, name : str) :
        self.name = name

    def get_name(self) -> str :
        return self.name


# Describes message instance
class Message :
    def __init__(self, chat_id : int, user_id : int, text : str, date_of_sent : DateTime) -> None :
        self.chat_id = chat_id
        self.user_id = user_id
        self.text = text
        self.date = date_of_sent
    
