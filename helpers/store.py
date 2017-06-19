class Store:
    def __init__(self, config):
        self.version = config["app"]["version"]
        self.verbose = False


class WorkerStore(Store):
    def __init__(self, config):
        Store.__init__(self, config)
        self.seconds_sleep_on_error = config["worker"]["seconds-sleep-on-error"]
        self.dict_target = config["worker"]["target"]
        self.arr_of_dict_match = config["worker"]["match"]


class SlackStore(Store):
    def __init__(self, config):
        Store.__init__(self, config)
        self.dict_slack_channels = {}
        self.slack_client = None
        self.slack_token = config["slack"]["token"]
        self.slack_url_webhook = config["slack"]["webhook-url"]
        self.request_header = {'Content-Type': 'application/json'}
        self.slack_channel_name = config["slack"]["channel-name"]
        self.slack_bot_name = config["slack"]["bot-name"]
