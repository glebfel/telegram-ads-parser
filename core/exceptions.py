class BasicParserException(Exception):
    """Base class for all parser errors"""

    def __str__(self):
        return "Something goes wrong with parser"


class CampaignNotExistsError(BasicParserException):
    def __init__(self, campaign_id: str):
        self.campaign_id = campaign_id

    def __str__(self):
        return f"Ads campaign with '{self.campaign_id}' id is not exists!"

