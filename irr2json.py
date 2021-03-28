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
        "valid": tm + 7200
    },
    "roas": [
    ]
}

if os.path.exists(export_file):
    os.remove(export_file)

with open(import_file, "r") as f:
    line = f.readline()
    ip = None
    originator = None
    cnt = 0
    while line:
        variables = line.split()
        if len(variables) == 2:
            attrib = variables[0].lower()
            val = variables[1].upper()

            if (attrib == "route:" or attrib == "route6:") and len(val) > 0:
                ip = val
            
            if attrib == "origin:" and len(val) > 0:
                if not val.startswith("AS"):
                    val = f"AS{val}"
                originator = val

            if ip and originator:
                if "." in ip:
                    maxlen = 24
                else:
                    maxlen = 48

                template["roas"].append({
                    "asn": originator,
                    "prefix": ip,
                    "maxLength": maxlen,
                    "ta": "irr-jsonify"
                })
                cnt += 1

                ip = None
                originator = None
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