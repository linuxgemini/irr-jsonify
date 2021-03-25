#!/usr/bin/env python3

export_file = "./irr.db"


import urllib.request as request
import os
import shutil
import zlib
import re

irr_sources = [
    "ftp://irr.bboi.net/bboi.db.gz",
    "ftp://rr.Level3.net/pub/rr/level3.db.gz",
    "https://ftp.lacnic.net/lacnic/irr/lacnic.db.gz",
    "https://ftp.ripe.net/ripe/dbase/split/ripe.db.route6.gz",
    "https://ftp.ripe.net/ripe/dbase/split/ripe.db.route.gz",
    "ftp://ftp.apnic.net/pub/apnic/whois/apnic.db.route6.gz",
    "ftp://ftp.apnic.net/pub/apnic/whois/apnic.db.route.gz",
    "ftp://ftp.radb.net/radb/dbase/radb.db.gz",
    "http://ftp.afrinic.net/pub/dbase/afrinic.db.gz",
    "ftp://ftp.radb.net/radb/dbase/arin-nonauth.db.gz",
    "ftp://ftp.radb.net/radb/dbase/arin.db.gz",
    "ftp://ftp.altdb.net/pub/altdb/altdb.db.gz",
    #"ftp.newaol.com/pub/aol-irr/dbase/aoltw.db.gz", # dead
    #"ftp://whois.in.bell.ca/bell/bell.db.gz", # inaccesible
    "ftp://whois.canarie.ca/dbase/canarie.db.gz",
    #"ftp://irr-mirror.idnic.net/idnic.db.gz", # times out
    "ftp://ftp.apnic.net/public/apnic/whois-data/JPIRR/jpirr.db.gz",
    "ftp://ftp.nestegg.net/irr/nestegg.db.gz",
    "ftp://rr1.ntt.net/nttcomRR/nttcom.db.gz",
    "ftp://ftp.openface.ca/pub/irr/openface.db.gz",
    "ftp://ftp.panix.com/pub/rrdb/panix.db.gz",
    "ftp://rg.net/rgnet/RGNET.db.gz",
    "ftp://ftp.ripe.net/ripe/dbase/split/ripe-nonauth.db.route6.gz",
    "ftp://ftp.ripe.net/ripe/dbase/split/ripe-nonauth.db.route.gz",
    "ftp://ftp.bgp.net.br/dbase/tc.db.gz" 
]

rx = re.compile(r"\.gz(ip)?$", re.IGNORECASE)

irr_dbs = []

if os.path.exists("./dbs"):
    shutil.rmtree("./dbs")

if os.path.exists(export_file):
    os.remove(export_file)

os.mkdir("./dbs")

for irr_source in irr_sources:
    gz_filename = irr_source.split("/")[-1]
    filename = rx.sub("", gz_filename)

    try:
        CHUNK = 16*1024
        d = zlib.decompressobj(zlib.MAX_WBITS|32)
        resp = request.urlopen(irr_source)
        with open(f"./dbs/{filename}", "wb") as f:
            while True:
                chungus = resp.read(CHUNK)
                if not chungus:
                    break
                f.write(d.decompress(chungus))

        irr_dbs.append(f"./dbs/{filename}")
        print(f"Written {filename}")
    except Exception as e:
        print(f"Error on writing {filename}, error:\n{str(e)}")
        if os.path.exists(f"./dbs/{filename}"):
            os.remove(f"./dbs/{filename}")


with open(export_file, "w") as f_out:
    for irr_db in irr_dbs:
        print(f"Processing {irr_db}")
        with open(irr_db, "rb") as f_in:
            line = f_in.readline()
            cnt = 0
            while line:
                try:
                    line_text = line.decode()
                except Exception as e:
                    pass

                if (
                    line_text.startswith("route:") or
                    line_text.startswith("route6:") or
                    line_text.startswith("origin:")
                ):
                    f_out.write(f"{line_text}")
                    cnt += 1

                line = f_in.readline()
            print(f"Processed {cnt} line(s)")

shutil.rmtree("./dbs")

print(f"Written everything to {export_file}")

os._exit(0)