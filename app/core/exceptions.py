class BasicParserException(Exception):
    """Base class for all parser errors"""

    def __str__(self):
        return "Something goes wrong with parser"


class CampaignNotExistsError(BasicParserException):
    def __init__(self, promotion_id: str):
        self.promotion_id = promotion_id

    def __str__(self):
        return f"Ads promotion with '{self.promotion_id}' id is not exists!"


class NotEnoughDayDataError(BasicParserException):
    def __init__(self, promotion_id: str):
        self.promotion_id = promotion_id

    def __str__(self):
        return f"Not enough day data for the ads promotion with '{self.promotion_id}' id!"
