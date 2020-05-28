import csv
import json
from datetime import datetime


class Record:
    def __init__(self):
        self.mood = 0
        self.stress = 0
        self.stationary_count = 0
        self.walking_count = 0
        self.running_count = 0
        self.conversation_count = 0
        self.total_conversation_duration = 0
        self.average_conversation_duration = 0
        self.phone_lock_count = 0
        self.total_phone_lock_duration = 0
        self.average_phone_lock_duration = 0
        self.dark_environment_count = 0
        self.total_dark_environment_duration = 0
        self.average_dark_environment_duration = 0
        self.unique_wifi_networks = 0
        self.unique_bluetooth_devices = 0
        self.unique_positions = 0
        self.wifiNetworks = set()
        self.bluetooth = set()
        self.position = set()

    def add_walking(self):
        self.walking_count = self.walking_count + 1

    def add_stationary(self):
        self.stationary_count = self.stationary_count + 1

    def add_running(self):
        self.running_count = self.running_count + 1

    def add_conversation(self, conversation_duration):
        self.conversation_count = self.conversation_count + 1
        self.total_conversation_duration = self.total_conversation_duration + conversation_duration
        self.average_conversation_duration = self.total_conversation_duration / self.conversation_count

    def add_phone_lock(self, lock_duration):
        self.phone_lock_count = self.phone_lock_count + 1
        self.total_phone_lock_duration = self.total_phone_lock_duration + lock_duration
        self.average_phone_lock_duration = self.total_phone_lock_duration / self.phone_lock_count

    def add_dark_environment(self, dark_duration):
        self.dark_environment_count = self.dark_environment_count + 1
        self.total_dark_environment_duration = self.total_dark_environment_duration + dark_duration
        self.average_dark_environment_duration = self.total_dark_environment_duration / self.dark_environment_count

    def add_wifi(self, ssid):
        self.wifiNetworks.add(ssid)
        self.unique_wifi_networks = len(self.wifiNetworks)

    def add_bluetooth(self, mac):
        self.bluetooth.add(mac)
        self.unique_bluetooth_devices = len(self.bluetooth)

    def add_position(self, latLon):
        self.position.add(latLon)
        self.unique_positions = len(self.position)

    def add_mood(self, mood):
        self.mood = mood

    def add_stress(self, stress):
        self.stress = stress

    def to_list(self, date):
        return [date, self.stationary_count, self.walking_count, self.running_count, self.total_conversation_duration,
                self.average_conversation_duration, self.phone_lock_count, self.total_phone_lock_duration,
                self.average_phone_lock_duration, self.dark_environment_count, self.total_dark_environment_duration,
                self.average_dark_environment_duration, self.unique_wifi_networks, self.unique_bluetooth_devices,
                self.unique_positions, self.mood, self.stress]


class Test:
    def __init__(self, date, happy):
        self.date = date
        self.happy = happy


def process_activity(record, participant):
    firstLine = True
    with open('../dataset/dataset/sensing/activity/activity_u' + participant + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if firstLine:
                firstLine = False
            else:
                timestamp = datetime.fromtimestamp(int(row[0]))
                infered_activity = int(row[1])
                date = timestamp.strftime('%Y-%m-%d %H')
                if date in record:
                    entry = record[date]
                else:
                    entry = Record()
                if infered_activity == 0:
                    entry.add_stationary()
                elif infered_activity == 1:
                    entry.add_walking()
                elif infered_activity == 2:
                    entry.add_running()
                record[date] = entry


def process_wifi(record, participant):
    firstLine = True
    with open('../dataset/dataset/sensing/wifi/wifi_u' + participant + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if firstLine:
                firstLine = False
            else:
                timestamp = datetime.fromtimestamp(int(row[0]))
                bssid = row[1]
                date = timestamp.strftime('%Y-%m-%d %H')
                if date in record:
                    entry = record[date]
                else:
                    entry = Record()
                entry.add_wifi(bssid)
                record[date] = entry


def process_bluetooth(record, participant):
    firstLine = True
    with open('../dataset/dataset/sensing/bluetooth/bt_u' + participant + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if firstLine:
                firstLine = False
            else:
                timestamp = datetime.fromtimestamp(int(row[0]))
                mac = row[1]
                date = timestamp.strftime('%Y-%m-%d %H')
                if date in record:
                    entry = record[date]
                else:
                    entry = Record()
                entry.add_bluetooth(mac)
                record[date] = entry


def process_gps(record, participant):
    firstLine = True
    with open('../dataset/dataset/sensing/gps/gps_u' + participant + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if firstLine:
                firstLine = False
            else:
                timestamp = datetime.fromtimestamp(int(row[0]))
                latLon = (float("{:.2f}".format(float(row[4]))), float("{:.2f}".format(float(row[5]))))
                date = timestamp.strftime('%Y-%m-%d %H')
                if date in record:
                    entry = record[date]
                else:
                    entry = Record()
                entry.add_position(latLon)
                record[date] = entry


def process_conversation(record, participant):
    firstLine = True
    with open('../dataset/dataset/sensing/conversation/conversation_u' + participant + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if firstLine:
                firstLine = False
            else:
                start_time = datetime.fromtimestamp(int(row[0]))
                end_time = datetime.fromtimestamp(int(row[1]))
                date = start_time.strftime('%Y-%m-%d %H')
                if date in record:
                    entry = record[date]
                else:
                    entry = Record()
                entry.add_conversation((end_time - start_time).seconds)
                record[date] = entry


def process_phone_lock(record, participant):
    firstLine = True
    with open('../dataset/dataset/sensing/phonelock/phonelock_u' + participant + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if firstLine:
                firstLine = False
            else:
                start_time = datetime.fromtimestamp(int(row[0]))
                end_time = datetime.fromtimestamp(int(row[1]))
                date = start_time.strftime('%Y-%m-%d %H')
                if date in record:
                    entry = record[date]
                else:
                    entry = Record()
                entry.add_phone_lock((end_time - start_time).seconds)
                record[date] = entry


def process_dark(record, participant):
    firstLine = True
    with open('../dataset/dataset/sensing/dark/dark_u' + participant + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if firstLine:
                firstLine = False
            else:
                start_time = datetime.fromtimestamp(int(row[0]))
                end_time = datetime.fromtimestamp(int(row[1]))
                date = start_time.strftime('%Y-%m-%d %H')
                if date in record:
                    entry = record[date]
                else:
                    entry = Record()
                entry.add_dark_environment((end_time - start_time).seconds)
                record[date] = entry


def process_mood(entries, participant):
    with open('../dataset/dataset/EMA/response/Mood/Mood_u' + participant + '.json') as json_file:
        reader = json.load(json_file)
        for row in reader:
            timstamp = datetime.fromtimestamp(int(row['resp_time']))
            date = timstamp.strftime('%Y-%m-%d %H')
            try:
                entry = Test(date, int(row['happyornot']))
                entries.append(entry)
            except:
                return


def process_mood2(record, participant):
    with open('../dataset/dataset/EMA/response/Mood/Mood_u' + participant + '.json') as json_file:
        reader = json.load(json_file)
        for row in reader:
            timstamp = datetime.fromtimestamp(int(row['resp_time']))
            date = timstamp.strftime('%Y-%m-%d %H')
            if date in record:
                entry = record[date]
            else:
                entry = Record()
            try:
                entry.add_mood(int(row['happyornot']))
                record[date] = entry
            except:
                continue


def process_stress(record, participant):
    with open('../dataset/dataset/EMA/response/Stress/Stress_u' + participant + '.json') as json_file:
        reader = json.load(json_file)
        for row in reader:
            timstamp = datetime.fromtimestamp(int(row['resp_time']))
            date = timstamp.strftime('%Y-%m-%d %H')
            if date in record:
                entry = record[date]
            else:
                entry = Record()
            try:
                entry.add_stress(int(row['level']))
                record[date] = entry
            except:
                continue


if __name__ == "__main__":
    files = ['00', '05', '12', '17', '23', '31', '36', '44', '50', '56',
             '01', '07', '13', '18', '24', '32', '39', '45', '51', '57',
             '02', '08', '14', '19', '25', '33', '41', '46', '52', '58',
             '03', '09', '15', '20', '27', '34', '42', '47', '53', '59',
             '04', '10', '16', '22', '30', '35', '43', '49', '54']
    record = {}
    mood_entries = []

    '''
    for user in files:
        process_mood(mood_entries, user)
        with open('test/u' + user + '.csv', 'w', newline='') as csvfile:
            record_writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            record_writer.writerow(
                ['date', 'is_happy'])
            for entry in mood_entries:
                record_writer.writerow([entry.date, entry.happy])
        print("done with u" + user)
    '''
    for user in files:
        record = {}
        process_activity(record, user)
        process_wifi(record, user)
        process_bluetooth(record, user)
        process_gps(record, user)
        process_conversation(record, user)
        process_phone_lock(record, user)
        process_dark(record, user)
        process_mood2(record, user)
        process_stress(record, user)
        with open('resources_hours/u' + user + '.csv', 'w', newline='') as csvfile:
            record_writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            record_writer.writerow(
                ['date', 'stationary_count', 'walking_count', 'running_count', 'total_conversation_duration',
                 'average_conversation_duration', 'phone_lock_count', 'total_phone_lock_duration',
                 'average_phone_lock_duration', 'dark_environment_count', 'total_dark_environment_duration',
                 'average_dark_environment_duration', 'unique_wifi_networks', 'unique_bluetooth_devices',
                 'unique_positions', 'mood', 'stress'])
            for key in record.keys():
                record_writer.writerow(record[key].to_list(key))
        print("done with u" + user)
