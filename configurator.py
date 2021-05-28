from configparser import ConfigParser, SectionProxy

class Config:
    pass

class ConfigSection:
    def __init__(self, section: SectionProxy, items_type: str):
        for key in section:
            if items_type == "string":
                self.__setattr__(key, section[key])
            elif items_type == "int":
                try:
                    self.__setattr__(key, section.getint(key))
                except ValueError:
                    print("Could not convert to int", key)
                    raise

# global config
config = Config()

def check_config_file(filename: str) -> bool:
    required_structure = {
        "bot": ["start_after", "last_catch_interval", "box_width", "box_height"],
    }

    global config
    parser = ConfigParser()
    parser.read(filename)

    # check required sections and their values
    if len(parser.sections()) == 0:
        print("Config file missing or empty")
        return False
    
    for section in required_structure.keys():
        if section not in parser.sections():
            print(f'Missing "{section}" section in config file')
            return False
        for value in required_structure[section]:
            if value not in parser[section]:
                print(f'Missing "{value}" value in "{section}" section of config file')
                return False

    # read again, now create Config
    objects_type = {"bot": "int"}
    for section in parser.sections():
        try:
            config.__setattr__(section, ConfigSection(parser[section], items_type=objects_type[section]))
        except ValueError:
            return False
        
        return True
        