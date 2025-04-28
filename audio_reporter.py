#!/usr/bin/env python
import subprocess
import re
import json


def parse_wpctl_status():
    # Execute the wpctl status command and store the output in a variable.
    output = str(
        subprocess.check_output(
            "wpctl status", shell=True, encoding='utf-8'))
    # remove the ascii tree characters and return a list of lines
    output = output\
        .replace("├", "")\
        .replace("─", "")\
        .replace("│", "")\
        .replace("└", "")

    sinks = parse_wpctl("Sinks:", output)
    sources = parse_wpctl("Sources:", output)

    return {"sinks": sinks, "sources": sources}


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
        if not line.strip() and thing_found:
            break
        if thing_found:
            thing = {}
            line = line.strip()
            if line.startswith("*"):
                thing["default"] = True
            else:
                thing["default"] = False

            if "MUTED" in line:
                thing["mute"] = True
            else:
                thing["mute"] = False

            match = re.search(r'\[vol:\s*([0-9]+\.[0-9]+)\]', line)
            if match:
                volumen = match.group(1)
                thing["volume"] = int(float(volumen) * 100.0)

            # remove the "[vol:" from the end of the sink name
            line = line.split("[vol:")[0].strip()
            thing["id"] = int(line.split(".")[0].replace("*", ""))
            thing["name"] = line.split(".")[1].strip()

            things.append(thing)

    return things


print(json.dumps(parse_wpctl_status()))
