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


class ProjectOutputTables:

    __params = {
        ProjectType.PROMO: ['promo-line-quarter', 'promo-line-month', 'promo-sku-quarter', 'promo-sku-month'],
        ProjectType.RTM: ['rtm_cts_wh', 'rtm_cts_t1', 'rtm_cts_t2', 'rtm_cts_total'],
        ProjectType.TETRIS: None,
        ProjectType.CFR: ['main', 'randomizer', 'detailed'],
    }

    @classmethod
    def get(cls, optimizer_type: str):
        return cls.__params[optimizer_type]
