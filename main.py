import logging
from configurator import config, check_config_file
from bot import FishingBot

# logging
logging.basicConfig(level=logging.INFO)

# Config
if not check_config_file("config.ini"):
    exit("Config file parse error! Exiting!")

# initialize bot
bot = FishingBot(config)

if __name__ == "__main__":
    bot.start()
