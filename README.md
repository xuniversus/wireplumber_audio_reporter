# wireplumber audio reporter
A script that uses wpctl to list audio sinks and sources, returns a JSON string.

# How to Install
copy the ```audio_reporter.py``` file to your ```$PATH```.
Then: ```chmod +x audio_reporter.py```

Example output:
```shell
$ python audio_changer.py | jq '.'
```
```json
{
  "sinks": [
    {
      "default": false,
      "volume": 100,
      "id": 59,
      "name": "Loopback Estéreo analógico"
    },
    {
      "default": false,
      "volume": 100,
      "id": 60,
      "name": "Starship/Matisse HD Audio Controller Estéreo digital (IEC958)"
    },
    {
      "default": true,
      "volume": 100,
      "id": 62,
      "name": "Navi 21/23 HDMI/DP Audio Controller Estéreo digital (HDMI)"
    },
    {
      "default": false,
      "volume": 100,
      "id": 70,
      "name": "UMC202HD 192k Line A"
    }
  ],
  "sources": [
    {
      "default": false,
      "volume": 100,
      "id": 61,
      "name": "Starship/Matisse HD Audio Controller Estéreo analógico"
    },
    {
      "default": false,
      "volume": 100,
      "id": 66,
      "name": "Loopback Estéreo analógico"
    },
    {
      "default": false,
      "volume": 100,
      "id": 69,
      "name": "UMC202HD 192k Input 2"
    },
    {
      "default": true,
      "volume": 100,
      "id": 71,
      "name": "UMC202HD 192k Input 1"
    }
  ]
}
```
