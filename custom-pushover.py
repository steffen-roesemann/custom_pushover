""" Send custom alert messages from Wazuh manager via Pushover.net API to your smartphone. """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json

try:
    import requests
except ImportError:
    print("Importing module failed. Please install with pip install -r requirements.txt")
    sys.exit(1)

class CustomPushover():
    """
    Custom class for sending alert messages from the Open Source
    Security Information and Event Management (SIEM) platform Wazuh
    via the Pushover.net API to your smartphone application.

    First, copy the slack shellscript and rename it custom-pushover:
    # cp /var/ossec/integrations/slack /var/ossec/integrations/custom-pushover

    Copy this script to the following folder of your Wazuh manager
    and adjust file settings and ownership:
    
    # cp ./custom-pushover.py /var/ossec/integrations/
    # chmod 750 /var/ossec/integrations/custom-pushover.py
    # chown root:wazuh /var/ossec/integrations/custom-pushover.py

    Afterwards copy this XML block in the Wazuh managers 
    configuration file in /var/ossec/etc/ossec.conf
    within the <ossec_config> section:

    <integration>
      <name>custom-pushover</name>
      <api_key>token:user</api_key> <!-- Replace with your Pushovers API token and/or user/group key -->
      <alert_format>json</alert_format>
    </integration>

    Afterwards, don't forget to restart the Wazuh manager
    # systemctl restart wazuh-manager
    """
    def __init__(self, token, user) -> None:
        self.pushover_api = "https://api.pushover.net/1/messages.json"
        self.token = token
        self.user = user
        self.alert_level = 12

    def compile_message(self, alert_json) -> dict:
        """
            Compiles the message from the Wazuh alert json to be sent via Pushover API.
        """
        title = alert_json['rule']['description'] if 'description' in alert_json['rule'] else 'N/A'
        description = alert_json['full_log'] if 'full_log' in alert_json else 'N/A'
        description.replace("\\n", "\n")
        alert_level = alert_json['rule']['level'] if 'level' in alert_json['rule'] else '0'
        agent_name = alert_json['agent']['name'] if 'name' in alert_json['agent'] else 'N/A'
        agent_id = alert_json['agent']['id'] if 'id' in alert_json['agent'] else 'N/A'

        message = {}
        if int(alert_level) >= self.alert_level:
            message['title'] = f'{title}(Level: {alert_level})\n\n'
            message['message'] = f'{description}\nAgent: {agent_name} ({agent_id})\n'
            message['token'] = self.token
            message['user'] = self.user

            # Debug information
            with open("/var/ossec/logs/integrations.log", "a", encoding="utf-8") as fd:
                fd.write(f'Message to Pushover: {message["message"]}\n')

        return message
    
    def send_pushover_msg(self, message):
        """
            Send a message to the Pushover API.
        """
        response = requests.post(self.pushover_api, data=message)

        # Debug information
        with open("/var/ossec/logs/integrations.log", "a", encoding="utf-8") as fd:
            fd.write(f'Pushover Response: {response.text}\n')
        
if __name__ == "__main__":
    with open(sys.argv[1], "r", encoding="utf-8") as fd:
        alert_json = json.loads(fd.read())

    token = sys.argv[2].split(':')[0]
    user = sys.argv[2].split(':')[1]

    custom_pushover = CustomPushover(token, user)

    msg = custom_pushover.compile_message(alert_json)
    if msg:
        custom_pushover.send_pushover_msg(msg)

    sys.exit(0)
