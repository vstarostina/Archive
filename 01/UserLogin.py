class UserLogin():
    '''метод, наполняет содержимое авторизованым пользователем'''
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self #Возвращаем экземпляр

    def create(self, user):
        self.__user = user
        return self

    '''Функция проверки авторизации'''
    def is_authenticated(self):
        return True

    '''Функция проверки активности'''
    def is_active (self):
        return True

    '''Функция проверки не авторизованных пользователей'''
    def is_anonymous(self):
        return False

    '''Функция, возвращающая уникальный индетификатор'''
    def get_id(self):
        return str(self.__user['id'])