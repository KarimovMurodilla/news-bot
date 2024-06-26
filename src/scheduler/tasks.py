import pytz
from datetime import datetime

# from src.scraper.parsers.kun_uz import KunUzParser
# from src.scraper.parsers.daryo import DaryoUzParser
from src.scraper.parsers.uza_uz import UzaUzParser
from src.scraper.parsers.zamon_uz import ZamonUzParser
from src.scraper.parsers.dunyo_info import DunyoInfoParser
from src.scraper.parsers.darakchi_uz import DarakchiUzParser
from src.scraper.parsers.yuz_uz import YuzUzParser
from src.scraper.parsers.zamin_uz import ZaminUzParser
from src.scraper.parsers.aniq_uz import AniqUzParser
from src.scraper.parsers.xs_uz import XsUzParser
from src.scraper.parsers.xabar_uz import XabarUzParser
from src.scraper.parsers.qalampir_uz import QalampirUzParser
from src.scraper.parsers.gov_uz import GovUzParser
from src.scraper.parsers.innovation_gov_uz import InnovationGovUzParser
from src.scraper.parsers.it_park_uz import ItparkUzParser
from src.scraper.parsers.tuit_uz import TuitUzParser
from src.scraper.parsers.president_uz import PresidentUzParser
from src.scraper.parsers.texnopark_uz import TexnoparkUzParser
from src.scraper.parsers.kapital_uz import KapitalUzParser

from src.bot.utils.broadcaster import Broadcaster


async def parse_and_save_db():
    # kun_uz = KunUzParser() # No permission
    # daryo_uz = DaryoUzParser() # No permission
    timezone = pytz.timezone('Asia/Tashkent')
    now = datetime.now(timezone)
    hour = int(now.strftime("%H"))

    if hour >= 6 and hour <= 23:
        uza_uz = UzaUzParser()
        zamon_uz = ZamonUzParser()
        dunyo_info = DunyoInfoParser()
        darakchi_uz = DarakchiUzParser()
        yuz_uz = YuzUzParser()
        zamin_uz = ZaminUzParser()
        aniq_uz = AniqUzParser()
        xs_uz = XsUzParser()
        xabar_uz = XabarUzParser()
        qalampir_uz = QalampirUzParser()
        gov_uz = GovUzParser()
        innovation_gov_uz = InnovationGovUzParser()
        it_park_uz = ItparkUzParser()
        tuit_uz = TuitUzParser()
        president_uz = PresidentUzParser()
        texnopark_uz = TexnoparkUzParser()
        kapital_uz = KapitalUzParser()

        # await kun_uz.parse_all_and_save()
        # await daryo_uz.parse_all_and_save()

        await uza_uz.parse_all_and_save()
        await zamon_uz.parse_all_and_save()
        await dunyo_info.parse_all_and_save()
        await darakchi_uz.parse_all_and_save()
        await yuz_uz.parse_all_and_save()
        await zamin_uz.parse_all_and_save()
        await aniq_uz.parse_all_and_save()
        await xs_uz.parse_all_and_save()
        await xabar_uz.parse_all_and_save()
        await qalampir_uz.parse_all_and_save()
        await gov_uz.parse_all_and_save()
        await innovation_gov_uz.parse_all_and_save()
        await it_park_uz.parse_all_and_save()
        await tuit_uz.parse_all_and_save()
        await president_uz.parse_all_and_save()
        await texnopark_uz.parse_all_and_save()
        await kapital_uz.parse_all_and_save()

        broadcaster = Broadcaster()
        await broadcaster.broadcast()
