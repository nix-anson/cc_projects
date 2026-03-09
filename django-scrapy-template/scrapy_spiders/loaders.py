"""Item loaders with data cleaning processors."""
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def clean_text(value):
    """Strip whitespace from text fields."""
    return value.strip() if isinstance(value, str) else value


def to_uppercase(value):
    """Convert state codes to uppercase."""
    return value.upper() if isinstance(value, str) else value


class PoliticianLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in = MapCompose(clean_text)
    state_in = MapCompose(clean_text, to_uppercase)
    bio_in = MapCompose(clean_text)


class VoteLoader(ItemLoader):
    default_output_processor = TakeFirst()
    bill_number_in = MapCompose(clean_text)
    bill_title_in = MapCompose(clean_text)
    vote_choice_in = MapCompose(clean_text)
