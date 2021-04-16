"""Define data name of person file."""

# Official Librariees
from enum import Enum


__all__ = (
        'PersonItem',
        'PersonDetail',
        'PersonLife',
        )


class PersonItem(Enum):
    NAME = 'name'
    FULLNAE = 'fullname'
    AGE = 'age'
    BIRTH = 'birth'
    SEX = 'sex'
    JOB = 'job'
    BELONG = 'belong'
    CALLING = 'calling'
    INFO = 'info'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DETAIL = 'detail'
    LIFE = 'life'
    HISTORY = 'history'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value


class PersonDetail(Enum):
    HEIGHT = 'height'
    WEIGHT = 'weight'
    APPEARANCE = 'appearance'
    FAMILY = 'family'
    PARENTS = 'parents'


class PersonLife(Enum):
    HOME = 'home'
    ADDRESS = 'address'
    FASHION = 'fashion'
    FOODS = 'foods'
    HIOBBIES = 'hobbies'
    ABILITIES = 'abilities'


# NOTE: historyについては据え置き。考え中
