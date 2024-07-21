#!/usr/bin/python
# python program to analyze shelly4hass usage
# 2024 by jens martin schlatter, germany

import os
import json
import pprint
try:
    import yaml
except ImportError:
    print("please install python package pyyaml")
    quit(8)

# Opening JSON file
base = "/home/nuc/.homeassistant"

f = open(os.path.join(base,'.storage','core.config_entries'))
# returns JSON object as 
# a dictionary
config = json.load(f)

# get all shelly devices
f = open(os.path.join(base,'.storage','core.device_registry'))
# returns JSON object as a dictionary
devices = json.load(f)

# get all shelly entities
f = open(os.path.join(base,'.storage','core.entity_registry'))
# returns JSON object as a dictionary
entities = json.load(f)

# get all areas
f = open(os.path.join(base,'.storage','core.area_registry'))
# returns JSON object as a dictionary
areas = json.load(f)
areadict = {}
for a in areas["data"]["areas"]:
    key = a["id"]
    val = a["name"]
    areadict[key] = val

# get GUI usage of entities
f = open(os.path.join(base,'.storage','lovelace'))
views = json.load(f)["data"]["config"]["views"]

# try to read the automations
with open(os.path.join(base,'automations.yaml'), 'r') as yfile:
    automations = yaml.safe_load(yfile)

#pprint.pprint(automations)
#quit()

# find shelly4hass config entry (I hope this is not the native shelly integration)
for e in config["data"]["entries"]:
    if e["domain"] == "shelly" and e.get("version","")==1 and e.get("minor_version","")==1:
        entry_id = e["entry_id"]

#print("shelly entry_id:",entry_id)


# loop over all shelly devices
for d in devices["data"]["devices"]:
    if d["config_entries"][0] == entry_id:
        print("--------------------------")
        device_name = d["name"]
        device_id = d["id"]
        device_model = d["model"]
        device_area  = d["area_id"]
        print("Device '"+device_name+"',",device_model,",",areadict[device_area])
        # loop over all entities in one device
        for entity in entities["data"]["entities"]:
            if entity["device_id"] == device_id:
                #print("------------ entity:")
                #pprint.pprint(entity)
                eid = entity["entity_id"]
                print("-",eid)
                for v in views:
                    # check if the entity is used in badges
                    if "badges" in v:
                      for be in v["badges"]:
                        if eid == be:
                            print("  -> used as badge in view '"+v["title"]+"'")
                    # check if the entity is used in cards
                    if "cards" in v: 
                      for c in v["cards"]:
                        #print("c==>",c)
                        entities_in_card = c.get("entities")
                        if entities_in_card:
                          for xe in entities_in_card:
                            # print("xe=>>",xe)
                            if isinstance(xe,dict):
                              if eid == xe["entity"]:
                                print("  -> used in card in view '"+v["title"]+"'")
                            else:
                              if eid == xe:
                                print("  -> used in card in view '"+v["title"]+"'")
                # check if the entity is used in automations
                for au in automations:
                    au_str = json.dumps(au)
                    if eid in au_str:
                        #pprint.pprint(au)
                        print("  -> used in automation",au["id"])
