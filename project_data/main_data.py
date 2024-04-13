class ProjectType:
    PROMO = 'promo'
    RTM = 'rtm'
    TETRIS = 'tetris'
    CFR = 'cfr'


class ProjectLanguage:

    __languages = {
        ProjectType.PROMO: 'eng',
        ProjectType.RTM: 'eng',
        ProjectType.TETRIS: 'rus',
        ProjectType.CFR: 'eng'
    }

    @classmethod
    def get(cls, optimizer_type: str):
        return cls.__languages[optimizer_type]


