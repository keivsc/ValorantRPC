import time

opt = {
    "selected":"SELECT",
    "locked":"LOCKED"
}

class PreGame:
    def __init__(self, client, rpc, config):
        self.queue_time = None
        self.client = client
        self.rpc = rpc
        self.Config = config
        self.config = self.Config.fetch_config()
        self.state = "PREGAME"

    def start_presence(self):
        while self.state == "PREGAME":
            presence = self.client.get_presence()
            if presence == None:
                self.state = None
                break
            self.state = presence['sessionLoopState']
            data = self.client.get_pregame(presence)
            if data == None:
                break
            
            rpc_data = {}
            rpc_data['end'] = data['time_left']
            rpc_data['details'] = f"{data['queue'].upper()} | PREGAME"
            rpc_data['large_image'] = data['map']['assetName']
            rpc_data['large_text'] = data['map']['displayName']
            rpc_data['small_image'] = data['agent']['assetName']
            rpc_data['small_text'] = data['agent']['displayName']
            if data['agent']['state'] != '':
                rpc_data['small_text'] += f" | {opt[data['agent']['state']]}"
            if self.config['presence']['show_party_count']:
                rpc_data['state'] = f"{presence['partyAccessibility'].capitalize()} Party | {presence['partySize']}/{presence['maxPartySize']}"

            self.rpc.set_activity(rpc_data)
            time.sleep(self.config['presence']['refreshRate'])
            self.config = self.Config.fetch_config()