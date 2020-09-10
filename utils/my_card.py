from utils.my_info_judge import pd_card


class IdCard:
    def __init__(self, id_card):
        if not pd_card(id_card):
            raise TypeError(u'请输入标准的第二代身份证号码')

        self.id_card = id_card
        self.birth_year = int(self.id_card[6:10])
        self.birth_month = int(self.id_card[10:12])
        self.birth_day = int(self.id_card[12:14])
        self.sex = -1 if int(self.id_card[-2:-1]) % 2 == 0 else 1
