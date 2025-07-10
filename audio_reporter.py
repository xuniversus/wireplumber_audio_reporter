#!/usr/bin/env python
from subprocess import run, check_output, PIPE
from re import sub, split


def parse_wpctl_status():
    # Execute the wpctl status command and store the output in a variable.
    output = str(check_output("wpctl status", shell=True, encoding='utf-8'))
    # remove the ascii tree characters and return a list of lines
    output = sub(r"[├─│└]", "", output)

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


#if there's only 2 outputs then action just switch and return the next id, if there's more, show wofi for selection
def get_selected_id(devices):
    smask = int(f"{len(devices["sinks"])}{len(devices["sources"])}")
    dmask = {21: "sinks", 12: "sources", \
             "sinks": "", "sources": "", \
             "": "sinks", "": "sources"}

    match smask:
        case 11:
            return None
        case 21 | 12:
            for siso in devices[dmask[smask]]:
                if not siso["default"]:
                    return siso["id"]
        case _:
            # get the list of sinks ready to put into wofi - highlight the current default sink
            output = ''
            for key in devices:
                for siso in devices[key]:
                    output += f"{dmask[key]} {siso["name"]}\n"

            # Call wofi and show the list. take the selected sink name and set it as the default sink
            #tofi_command = f"echo '{output}' | tofi --prompt-text=\"Sound: \" --anchor=\"top-right\" --margin-top=40 --margin-right=2"
            tofi_command = f"echo '{output}' | tofi --prompt-text=\" \" --anchor=\"top-right\" --margin-top=40 --margin-right=2"
            tofi_process = run(tofi_command, shell=True, encoding='utf-8', stdout=PIPE, stderr=PIPE)

            if tofi_process.returncode != 0:
                print("User cancelled the operation.")
                exit(0)

            selected_id = tofi_process.stdout.strip()
            if not selected_id:
                return None
            stype = selected_id[0]
            selected_id = selected_id[2:]
            match stype:
                case "" | "":
                    selected_siso = next(siso["id"] for siso in devices[dmask[stype]] if siso["name"] == selected_id)
                case _:
                    return Exception("Neither sink nor source chosen, should not happen!")
            return selected_siso

selected_id = get_selected_id(parse_wpctl_status())
if selected_id is not None:
    run(f"wpctl set-default {selected_id}", shell=True)
