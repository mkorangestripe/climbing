#!/usr/bin/env python3
"""Extract routes of interest and update csv files"""

import sys
import pandas

EXCLUDE_ROUTES_TXT = "exclude_routes.txt"
EXCLUDED_ROUTES = "Porsche 917K route placeholder"
WI4_CSV = "WI4.csv"
M5_CSV = "M5.csv"
FIVE_9PLUS_TRAD_CSV = "5.9plus-trad.csv"
FIVE_12_CSV = "5.12.csv"

if len(sys.argv) == 1:
    print("Usage 1, print filtered routes: ./filter_routes.py mountainproject-ticks.csv")
    print("Usage 2, write to csv files: ./filter_routes.py mountainproject-ticks.csv -w")
    print("Add routes to exclude to", EXCLUDE_ROUTES_TXT)
    sys.exit(1)

MNTPROJ_TICKS_CSV = sys.argv[1]

try:
    with open(EXCLUDE_ROUTES_TXT, "r", encoding="utf-8") as exclude_routes_data:
        for route in exclude_routes_data:
            EXCLUDED_ROUTES = EXCLUDED_ROUTES + '|' + route.strip()
except:
    pass

print("Excluded routes:", EXCLUDED_ROUTES)
print()

mp_df = pandas.read_csv(MNTPROJ_TICKS_CSV, dtype=str)

print("WI3-4 or harder, send")
WI4 = mp_df[(mp_df.Rating.str.contains("WI3-4|WI4|WI4-5|WI5") | mp_df["Your Rating"].str.contains("WI3-4|WI4|WI4-5|WI5")) &
            mp_df["Lead Style"].str.contains("Onsight|Flash|Redpoint") &
           (mp_df.Route.str.contains(EXCLUDED_ROUTES)==False)]
print(WI4)
print()

print("M5 or harder, send")
M5 = mp_df[(mp_df.Rating.str.contains("M[5-9]") | mp_df["Your Rating"].str.contains("M[5-9]"))&
          mp_df["Lead Style"].str.contains("Onsight|Flash|Redpoint") &
          (mp_df.Route.str.contains(EXCLUDED_ROUTES)==False)]
print(M5)
print()

print("5.9+ or harder, trad, send:")
FIVE_9PLUS_TRAD = mp_df[(mp_df.Rating.str.contains(r"5.9\+|5.1[0-13]") | mp_df["Your Rating"].str.contains(r"5.9\+|5.1[0-13]")) &
                         mp_df["Lead Style"].str.contains("Onsight|Flash|Redpoint") &
                        (mp_df["Route Type"].str.contains("Trad") | mp_df.Notes.str.contains("on gear", case=False)) &
                        (mp_df.Route.str.contains(EXCLUDED_ROUTES)==False)]
print(FIVE_9PLUS_TRAD)
print()

print("5.12 or harder, send:")
FIVE_12 = mp_df[(mp_df.Rating.str.contains("5.12|5.13") | mp_df["Your Rating"].str.contains("5.12|5.13")) &
                 mp_df["Lead Style"].str.contains("Onsight|Flash|Redpoint") &
                (mp_df.Route.str.contains(EXCLUDED_ROUTES)==False)]
print(FIVE_12)

if len(sys.argv) == 3:
    if sys.argv[2] == "-w":
        WI4.to_csv(WI4_CSV, index=False)
        M5.to_csv(M5_CSV, index=False)
        FIVE_9PLUS_TRAD.to_csv(FIVE_9PLUS_TRAD_CSV, index=False)
        FIVE_12.to_csv(FIVE_12_CSV, index=False)
