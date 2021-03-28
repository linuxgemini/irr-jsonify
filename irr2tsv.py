#!/usr/bin/env python3

import_file = "./irr.db"
export_file = "./irrdb.tsv"


import os


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


with open(export_file, "w") as f_out:
    with open(import_file, "r") as f_in:
        print(f"Started to process {import_file}")
        line = f_in.readline()
        ip = None
        originator = None
        cnt = 0
        while line:
            variables = line.split()
            if len(variables) == 2:
                attrib = variables[0].lower()
                val = variables[1].upper()

                if (attrib == "route:" or attrib == "route6:") and len(val) > 0:
                    ip = val.lower()

                if attrib == "origin:" and len(val) > 0:
                    val = val.replace("AS", "")
                    if "." not in val:
                        originator = f"AS{val}"
                    else:
                        originator = f"AS{asdot_to_asplain(val)}"

                if ip and originator:
                    f_out.write(f"{ip}\t\t{originator}\n")
                    cnt += 1

                    ip = None
                    originator = None
            line = f_in.readline()
        print(f"Processed a total of {cnt} object(s)")
    # remove final empty newline
    f_out.seek(0, os.SEEK_END)
    pos = f_out.tell() - 1
    f_out.seek(pos, os.SEEK_SET)
    f_out.truncate()


print(f"Written everything to {export_file}")


os._exit(0)
