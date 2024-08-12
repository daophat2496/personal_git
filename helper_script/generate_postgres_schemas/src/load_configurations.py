import os
import configparser

def loadConfigurations () :
    configs = {}
    config = configparser.ConfigParser()
    config.read('../config.ini')

    if os.getenv('DB_URL') == None :
        configs["db_url"] = config['PostgreSQL']['db_url']
    else :
        configs["db_url"] = os.getenv('DB_URL')

    if os.getenv('DB_DBNAME') == None :
        configs["db_dbname"] = config['PostgreSQL']['db_dbname']
    else :
        configs["db_dbname"] = os.getenv('DB_DBNAME')

    if os.getenv('DB_USERNAME') == None :
        configs["db_username"] = config['PostgreSQL']['db_username']
    else :
        configs["db_username"] = os.getenv('DB_USERNAME')

    if os.getenv('DB_PASSWORD') == None :
        configs["db_password"] = config['PostgreSQL']['db_password']
    else :
        configs["db_password"] = os.getenv('DB_PASSWORD')

    if os.getenv('BATCH_SIZE') == None :
        configs["batch_size"] = config['General']['batch_size']
    else :
        configs["batch_size"] = os.getenv('BATCH_SIZE')

# SSH configurations

    if os.getenv('SSH_HOST') == None :
        configs["ssh_host"] = config['SSH']['host']
    else :
        configs["ssh_host"] = os.getenv('SSH_HOST')

    if os.getenv('SSH_PORT') == None :
        configs["ssh_port"] = config['SSH']['port']
    else :
        configs["ssh_port"] = os.getenv('SSH_PORT')
    
    if os.getenv('SSH_USERNAME') == None :
        configs["ssh_username"] = config['SSH']['username']
    else :
        configs["ssh_username"] = os.getenv('SSH_USERNAME')

    if os.getenv('SSH_KEY_PATH') == None :
        configs["ssh_key_path"] = config['SSH']['key_path']
    else :
        configs["ssh_key_path"] = os.getenv('SSH_KEY_PATH')

    print(configs)

    return configs