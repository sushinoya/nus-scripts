import urllib, json, datetime

# CONSTANTS:
api_file_name = 'api_urls.json'
buildings_file_name = 'buildings.json'
save_file_name = 'records.json'

def get_all_wifi_data():
    buildings = load_json(buildings_file_name)
    for i in buildings:
        params = map(str, [buildings[i][0], buildings[i][1], buildings[i][2]])
        get_wifi_data(*params)


def get_wifi_data(building, floor_identifier, num_floors):
    with open(api_file_name, 'r') as apis_file:
        print("Collecting data for {}...".format(building))
        api_url_data = apis_file.read()
        apis = json.loads(api_url_data)
        outputs = []

    for floor in range(1, int(num_floors) + 1):
        response = urllib.urlopen(apis["wifi_url"].format(building, floor_identifier, num_str(floor)))
        try:
            devices = json.loads(response.read())
            num_of_devices = len(devices)
        except:
            devices = []
            num_of_devices = "N.A"

        for device in devices:
            record = Record(device["macAddress_hash"], str(datetime.datetime.now()), floor, building)
            record.save_record_to_json()

        outputs.append("Level {}: {}".format(num_str(floor), num_of_devices))

    for line in outputs:
        print line


# TO SAVE MAC HASH DATA
class Record:
    def __init__(self, mac_hash, timestamp, level, college):
        self.mac_hash = mac_hash
        self.timestamp = timestamp
        self.level = level
        self.college = college

    def save_record_to_json(self):
        saved_data = load_json(save_file_name)
        self.save_record_to_dict(saved_data)

        with open(save_file_name, 'w') as save_file:
            json.dump(saved_data, save_file)

    def save_record_to_dict(self, hashmap):
        mac = str(self.mac_hash)
        if mac in hashmap:
            hashmap[mac].append([self.timestamp, self.level, self.college])
        else:
            hashmap[mac] = [[self.timestamp, self.level, self.college]]

# UTILS
def num_str(n):
    if n < 10:
        return "0" + str(n)
    else:
        return str(n)

def load_json(name):
    with open(name, 'r') as file:
        data = file.read()
        hash = json.loads(data)
        return hash

def format_records():
    # Read in the file
    with open(save_file_name, 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(']], \"', ']], \n\"')

    # Write the file out again
    with open(save_file_name, 'w') as file:
      file.write(filedata)

# RUN
get_all_wifi_data()
# get_wifi_data("UTown-Cinanmon", "UTown-CNM", 21)
format_records()
