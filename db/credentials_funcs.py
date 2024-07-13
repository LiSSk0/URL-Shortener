def get_credentials(file_name):
    with open(file_name) as file:
        try:
            login = file.readline().strip()
            password = file.readline().strip()
        except Exception as e:
            print("ERROR: db/credentials_funcs.py - get_credentials:", e)
            return None
    return login, password


# checking if credentials are valid
def check_credentials(login, password):
    flag_login = False
    flag_password = True  # always true because password may be empty
    if login is not None and len(login) > 0:
        flag_login = True

    return flag_login * flag_password
