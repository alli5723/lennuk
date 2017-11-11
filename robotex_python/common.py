class ROBOT_STATE:
    STOP, SEARCH_BALL, THROW, SEARCH_BASKET = (False, False, False, False)

class ROBOT_WITH_BALL:
    SEEN_BALL, HAS_BALL, THROW_BALL, FOLLOW_BALL = (False, False, False, False)

class RESET_STATE_VALUES:
    def all(self):
        ROBOT_STATE.STOP = False
        ROBOT_STATE.SEARCH_BALL = False
        ROBOT_STATE.THROW = False
        ROBOT_STATE.SEARCH_BASKET = False