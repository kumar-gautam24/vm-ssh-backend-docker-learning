from pydantic import BaseModel

class User(BaseModel):
    name:str
    email:str
    balance:float=0.0


    def deposit(self, deposit:float):
        self.balance+=deposit

    def to_dict(self)->dict:
        result :dict[str,str|float]= {
            "Name": self.name,
            "Email": self.email,
            "Balance":self.balance,
        }

        return result





# user = User(name="Gautam", email="gk24feb@gmail.com")
# user2 = User(name="Sahil", email="sh@g.com")
# user3 = User(name="Ravi", email="r@g.com")

# user.deposit(120)
# user2.deposit(20)
# user3.deposit(1200)

# users :list[User]=[user,user2,user3]


# rich_users= [user for user in users if user.balance>100 ]

# for user in rich_users:
#     print(user.to_dict())


