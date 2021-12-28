import iso8601
import time

def iso8601_to_epoch(Time):
    if Time == "0001.01.01-00.00.00":
        return None
    split = Time.split("-")
    split[0] = split[0].replace(".","-")
    split[1] = split[1].replace(".",":")
    split = "T".join(i for i in split)
    split = iso8601.parse_date(split).timestamp() #converts iso8601 to epoch
    return split


class Menus:
    def __init__(self, client, rpc, config):
        self.queue_time = None
        self.client = client
        self.rpc = rpc
        self.Config = config
        self.config = self.Config.fetch_config()
        self.state = "MENUS"
        self.rank = None
        self.level = None

    def start_presence(self):
        while self.state == "MENUS":
            presence = self.client.get_presence()
            if presence == None:
                break
            if self.rank == None:
                self.rank = self.client.get_rank()

            self.state = presence['sessionLoopState']
            rpc_data = {}

            if presence['partyState'] == "MATCHMAKING":
                rpc_data['details'] = "In Queue | "
                if not self.queue_time:
                    self.queue_time = iso8601_to_epoch(presence["queueEntryTime"])
                
            else:
                rpc_data['details'] = "Menus | "
                if self.queue_time:
                    self.queue_time = None
            rpc_data['start'] = self.queue_time
                
            rpc_data['details'] += f"{self.client.parse_gamemode(presence['queueId'])}"
            if self.config['presence']['show_party_count']:
                rpc_data['state'] = f"{presence['partyAccessibility'].capitalize()} Party | {presence['partySize']}/{presence['maxPartySize']}"
            try:
                self.level = self.client.get_level()
            except:
                pass
            rpc_data['large_image'] = "game_icon"
            rpc_data['large_text'] = f"Level {self.level}"

            if presence['isIdle']:
                rpc_data['small_image'] = "away"
                rpc_data['small_text'] = "Idle"
            
            elif self.config['presence']['show_rank']:
                rpc_data['small_image'] = self.rank['assetName']
                rpc_data['small_text'] = self.rank['displayName']

            self.rpc.set_activity(rpc_data)
            time.sleep(self.config['presence']['refreshRate'])
            self.config = self.Config.fetch_config()

