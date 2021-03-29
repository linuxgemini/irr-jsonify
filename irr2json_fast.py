#!/usr/bin/env python3

import_file = "./irr.db"
export_file = "./irrdb.json"


import os


def asdot_to_asplain(str):
    split = str.split(".")
    if len(split) == 2:
        dot = int(split[0] or "0")
        add = int(split[1] or "0")
        return (dot * 65536) + add
    else:
        return None


with open(export_file, "w") as f_out:
    f_out.writelines([
        "{\n",
        "    \"roas\": ["
    ])

    with open(import_file, "r") as f_in:
        print(f"{import_file} is properly opened, processing")
        proc_cnt = 0
        line = f_in.readline()
        prefix = None
        asn = None
        cnt = 0
        while line:
            variables = line.split()

            if len(variables) == 2:
                attrib = variables[0].lower()
                val = variables[1].upper()

                if (attrib == "route:" or attrib == "route6:") and len(val) > 0:
                    prefix = val.lower()

                if attrib == "origin:" and len(val) > 0:
                    val = val.replace("AS", "")
                    if "." not in val:
                        asn = f"AS{val}"
                    else:
                        asn = f"AS{asdot_to_asplain(val)}"

                if prefix and asn:
                    if "." in prefix:
                        maxlen = 24
                    elif ":" in prefix:
                        maxlen = 48
                    else:
                        maxlen = 1

                    f_out.write(f"\n        {{\"asn\": \"{asn}\", \"prefix\": \"{prefix}\", \"maxLength\": {maxlen}, \"ta\": \"irr-jsonify\"}},")
                    proc_cnt += 1
                    prefix = None
                    asn = None

            line = f_in.readline()
        if proc_cnt > 0:
            # remove last comma
            f_out.seek(0, os.SEEK_END)
            pos = f_out.tell() - 1
            f_out.seek(pos, os.SEEK_SET)
            f_out.truncate()

    f_out.writelines([
        "\n    ],\n",
        "    \"metadata\": {\n",
        "        \"builder\": \"irr2json\",\n",
        f"        \"counts\": {proc_cnt}\n",
        "    }\n",
        "}"
    ])


print(f"{export_file} written")
