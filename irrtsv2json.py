#!/usr/bin/env python3

import_file = "./irrdb.tsv"
export_file = "./irrdb.json"


import json
import os
import time


tm = int(time.time())


def file_len(fname):
    i = 0
    with open(fname) as f:
        for line in f:
            if line.strip() != "":
                i += 1
    return i


with open(export_file, "w") as f_out:
    print(f"{export_file} is opened, getting non-empty line length of {import_file}")
    obj_cnt = file_len(import_file)
    print(f"{obj_cnt} object(s)")

    f_out.writelines([
        "{\n",
        "    \"metadata\": {\n",
        "        \"builder\": \"irr2json\",\n",
        f"        \"generated\": {tm},\n",
        f"        \"valid\": {tm + 7200}\n",
        f"        \"counts\": {obj_cnt}\n",
        "    },\n",
        "    \"roas\": ["
    ])

    with open(import_file, "r") as f_in:
        print(f"{import_file} is properly opened, processing")
        proc_cnt = 0
        for line in f_in:
            strp_line = line.strip()

            if strp_line == "":
                continue

            objs = strp_line.split()
            if len(objs) == 2:
                prefix = objs[0]
                asn = objs[1]

                if "." in prefix:
                    maxlen = 24
                elif ":" in prefix:
                    maxlen = 48
                else:
                    maxlen = 1

                f_out.write(f"\n        {{\"asn\": \"{asn}\", \"prefix\": \"{prefix}\", \"maxLength\": {maxlen}, \"ta\": \"irr-jsonify\"}}")

                proc_cnt += 1
                if proc_cnt < obj_cnt:
                    f_out.write(",")

    f_out.writelines([
        "\n    ]\n",
        "}"
    ])


print(f"{export_file} written")