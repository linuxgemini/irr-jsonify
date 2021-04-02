#!/usr/bin/env python3

import_file = "./irr.db"
export_file = "./irrdb.json"


import json
import os
import time

tm = int(time.time())

template = {
    "metadata": {
        "builder": "irr2json",
        "generated": tm,
        "valid": tm + 86400
    },
    "roas": [
    ]
}


def asdot_to_asplain(str):
    split = str.split(".")
    if len(split) == 2:
        dot = int(split[0] or "0")
        add = int(split[1] or "0")
        return (dot * 65536) + add
    else:
        return None


if os.path.exists(export_file):
    os.remove(export_file)

with open(import_file, "r") as f:
    line = f.readline()
    ip = None
    originator = None
    next_proc_item = "route"
    cnt = 0
    while line:
        variables = line.split(":")
        
        attrib = variables[0].strip().lower() or ""
        val = (":".join(variables[1:])).strip().split()[0].upper() or ""

        if attrib.startswith(next_proc_item) and len(val) > 0:
            if attrib.startswith("route"):
                ip = val
                next_proc_item = "origin"

            if attrib.startswith("origin"):
                val = val.replace("AS", "")
                if "." not in val:
                    originator = f"AS{val}"
                else:
                    originator = f"AS{asdot_to_asplain(val)}"

        if ip and originator:
            if "." in ip:
                maxlen = 24
                prefixlen = 32
            elif ":" in ip:
                maxlen = 48
                prefixlen = 128
            else:
                maxlen = 1
                prefixlen = 32

            if "/" in ip:
                prefixlen = int(ip.split("/")[1])

            if prefixlen <= maxlen:
                template["roas"].append({
                    "asn": originator,
                    "prefix": ip,
                    "maxLength": maxlen,
                    "ta": "irr-jsonify"
                })
                cnt += 1

            ip = None
            originator = None
            next_proc_item = "route"
        line = f.readline()
    print(f"Processed {cnt} object(s)")
    template["metadata"]["counts"] = cnt


with open(export_file, "w") as f_out:
    with open(f"{export_file}.lock", "w") as f_out_lock:
        f_out_lock.write("")
        print("Lockfile written, don't touch the export file!")
    json.dump(template, f_out)


os.remove(f"{export_file}.lock")

print(f"Written everything to {export_file}, lockfile removed")

os._exit(0)
