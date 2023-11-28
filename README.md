Custom class for sending alert messages from the Open Source Security Information and Event Management (SIEM) platform Wazuh via the Pushover.net API to your smartphone application.

First, ssh into your Wazuh manager, copy the slack shellscript and rename it custom-pushover:

```shell
# cp /var/ossec/integrations/slack /var/ossec/integrations/custom-pushover
```

Then copy this script to the following folder of your Wazuh manager and adjust file settings and ownership:

```shell
# git clone https://github.com/steffen-roesemann/custom_pushover
# cd custom_pushover
# pip3 install -r requirements.txt    
# cp ./custom-pushover.py /var/ossec/integrations/
# chmod 750 /var/ossec/integrations/custom-pushover.py
# chown root:wazuh /var/ossec/integrations/custom-pushover.py
```

Afterwards copy this XML block in the Wazuh managers configuration file in /var/ossec/etc/ossec.conf within the <ossec_config> section:

```shell
<integration>
  <name>custom-pushover</name>
  <api_key>token:user</api_key> <!-- Replace with your Pushovers API token and/or user/group key -->
  <alert_format>json</alert_format>
</integration>
```

Afterwards, don't forget to restart the Wazuh manager:

```shell
# systemctl restart wazuh-manager
```

People / articles that pushed me in the right direction for coding this and therefore deserve credits:
- https://www.reddit.com/r/Wazuh/comments/157iemn/wazuh_integration_with_pushover/
- https://medium.com/@henrion.frn/get-your-home-network-secured-with-raspberry-pi-wazuh-2023-edition-c7ac2044df3e

Disclaimer: You can use the script and it's instructions "as-is". I am not responsible for any problems this software causes on your machines. If you don't agree with that, please don't use this.