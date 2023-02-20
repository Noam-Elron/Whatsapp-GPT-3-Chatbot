from configparser import ConfigParser

#Get the configparser object
config_file = ConfigParser()

config_file["DATABASE_CREDENTIALS"] = {
    "host": "NoamElron.mysql.pythonanywhere-services.com",
    "user": "NoamElron",
    "password": "PeterPorker246E@",
}

config_file["OPENAI"] = {
    "key": "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",
    }

with open('config.ini', 'w') as file:
    config_file.write(file)