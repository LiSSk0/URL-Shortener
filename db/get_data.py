def get_credentials(file_name):
    with open(file_name) as file:
        try:
            login = file.readline().strip()
            password = file.readline().strip()
        except Exception:
            print("!ERROR getting log/pass: db/get_data.py - get_credentials.")
            return None

    return login, password
