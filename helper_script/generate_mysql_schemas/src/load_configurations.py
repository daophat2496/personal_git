import os
import configparser

def loadConfigurations () :
    configs = {}
    config = configparser.ConfigParser()
    config.read('../config.ini')

    if os.getenv('DB_URL') == None :
        configs["db_url"] = config['MySQL']['db_url']
    else :
        configs["db_url"] = os.getenv('DB_URL')

    if os.getenv('DB_PORT') == None :
        configs["db_port"] = config['MySQL']['db_port']
    else :
        configs["db_port"] = os.getenv('DB_PORT')

    if os.getenv('DB_DBNAME') == None :
        configs["db_dbname"] = config['MySQL']['db_dbname']
    else :
        configs["db_dbname"] = os.getenv('DB_DBNAME')

    if os.getenv('DB_USERNAME') == None :
        configs["db_username"] = config['MySQL']['db_username']
    else :
        configs["db_username"] = os.getenv('DB_USERNAME')

    if os.getenv('DB_PASSWORD') == None :
        configs["db_password"] = config['MySQL']['db_password']
    else :
        configs["db_password"] = os.getenv('DB_PASSWORD')

    if os.getenv('BATCH_SIZE') == None :
        configs["batch_size"] = config['General']['batch_size']
    else :
        configs["batch_size"] = os.getenv('BATCH_SIZE')

    print(configs)

    return configs