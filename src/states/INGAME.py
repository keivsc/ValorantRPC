import time

class InGame:
    def __init__(self, client, rpc, config):
        self.client = client
        self.rpc = rpc
        self.Config = config
        self.config = self.Config.fetch_config()
        self.gameTime = time.time()
        self.state = "INGAME"
        self.rank = None
        self.show_rank = False

    def start_presence(self):
        while self.state == "INGAME":
            presence = self.client.get_presence()
            if presence == None:
                break
            if self.rank == None:
                self.rank = self.client.get_rank()
            self.state = presence['sessionLoopState']

            data = self.client.get_coregame(presence)
            if data == None:
                break
            rpc_data = {}
            rpc_data['start'] = self.gameTime
            if data['practice'] == True:
                rpc_data['details'] = "Practice Range"
                self.show_rank = True
            else:
                rpc_data['details'] = f"{data['queue'].upper()} | {data['allyScore']}:{data['enemyScore']}"
            rpc_data['large_image'] = data['map']['assetName']
            rpc_data['large_text'] = data['map']['displayName']
            rpc_data['small_image'] = data['agent']['assetName']
            rpc_data['small_text'] = data['agent']['displayName']
            if self.config['presence']['show_party_count']:
                rpc_data['state'] = f"{presence['partyAccessibility'].capitalize()} Party | {presence['partySize']}/{presence['maxPartySize']}"

            if self.config['presence']['show_rank']:
                if self.show_rank:
                    rpc_data['small_image'] = self.rank['assetName']
                    rpc_data['small_text'] = self.rank['displayName']
                    self.show_rank = False
                else:
                    rpc_data['small_image'] = data['agent']['assetName']
                    rpc_data['small_text'] = data['agent']['displayName']
                    self.show_rank = True

            self.rpc.set_activity(rpc_data)
            time.sleep(self.config['presence']['refreshRate'])
            self.config = self.Config.fetch_config()