#!/usr/bin/env python
from subprocess import run, check_output, PIPE
from re import sub, split
from sys import argv


def parse_wpctl_status(siso: str):
    # Execute the wpctl status command and store the output in a variable.
    output = str(check_output("wpctl status", shell=True, encoding='utf-8'))
    # remove the ascii tree characters and return a list of lines
    output = sub(r"[├─│└]", "", output)

    siso = parse_wpctl(siso, output)

    return siso


def parse_wpctl(starting, output):
    if starting != "Sinks:" and starting != "Sources:":
        raise ValueError("Unexpected starting value '%s'" % starting)

    lines = output.splitlines()

    things = []
    # get the index of the Sinks line as a starting point
    thing_found = False
    for line in lines:
        if starting in line:
            thing_found = True
            continue
        line = line.strip()
        if ( not line or line[0].isalpha() ) and thing_found:
            break
        if thing_found:
            thing = {}
            if line.startswith("*"):
                thing["default"] = True
            else:
                thing["default"] = False

            if "MUTED" in line:
                thing["mute"] = True
            else:
                thing["mute"] = False

            # I don't deal in unecessary string searches, let's go full re
            splitter = split(r"\s*(\.|\[vol:|[0-9]+\.[0-9]+)\s*", line)
            if splitter:
                thing["id"] = int(splitter[0].replace("*", ""))
                thing["name"] = splitter[2]
                if len(splitter) > 3:
                    volumen = splitter[5]
                    thing["volume"] = int(float(volumen) * 100.0)

            things.append(thing)

    return things


def get_selected_id(device: str, devices: dict):

    for siso in devices:
        if siso["name"] == device and not siso["default"]:
            return siso["id"]
    return None

smask = {"sink": "Sinks:", "source": "Sources:"}

siso = argv[1]
assert siso == "sink" or siso == "source"
siso = smask[siso]

selected_id = get_selected_id(argv[2], parse_wpctl_status(siso))
if selected_id is not None:
    run(f"wpctl set-default {selected_id}", shell=True)
