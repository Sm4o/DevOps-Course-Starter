from enum import Enum


class CardStatus(Enum):
    DONE = 'Done'
    TODO = 'To Do'
    DOING = 'Doing'

    @classmethod
    def get_status(cls, status: str) -> Enum:
        if status == cls.DONE.value:
            return cls.DONE
        elif status == cls.TODO.value:
            return cls.TODO
        elif status == cls.DOING.value:
            return cls.DOING
        else:
            raise ValueError('Unknown status')