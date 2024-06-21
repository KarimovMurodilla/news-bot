from src.scraper.parsers.kun_uz import KunUzParser
from src.scraper.parsers.daryo import DaryoUzParser
from src.scraper.parsers.uza_uz import UzaUzParser
from src.scraper.parsers.zamon_uz import ZamonUzParser
from src.scraper.parsers.dunyo_info import DunyoInfoParser
from src.scraper.parsers.darakchi_uz import DarakchiUzParser
from src.scraper.parsers.yuz_uz import YuzUzParser
from src.scraper.parsers.zamin_uz import ZaminUzParser

from src.bot.utils.broadcaster import Broadcast


async def parse_and_save_db():
    kun_uz = KunUzParser() # No permission
    daryo_uz = DaryoUzParser() # No permission

    uza_uz = UzaUzParser()
    zamon_uz = ZamonUzParser()
    dunyo_info = DunyoInfoParser()
    darakchi_uz = DarakchiUzParser()
    yuz_uz = YuzUzParser()
    zamin_uz = ZaminUzParser()

    # # await kun_uz.parse_all_and_save()
    # # await daryo_uz.parse_all_and_save()

    # await uza_uz.parse_all_and_save()
    # await zamon_uz.parse_all_and_save()
    # await dunyo_info.parse_all_and_save()
    # await darakchi_uz.parse_all_and_save()
    # await yuz_uz.parse_all_and_save()
    # await zamin_uz.parse_all_and_save()

    broadcaster = Broadcast()
    await broadcaster.broadcast()

    