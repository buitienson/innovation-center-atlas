"""Reverse-geocode a (lon, lat) point to a country name matching ROSTER's
existing naming convention, using Natural Earth's public 1:50m admin-0
country polygons (no API key, no rate limit, ~3MB).

Point-in-polygon is plain ray-casting (no shapely/numpy dependency - PyPI
installs have been unreliably slow/hanging on this machine across several
ROSTER-growth sessions), with bounding-box pre-filtering per country for
speed and hole support (so enclaves like Lesotho-in-South Africa resolve
correctly). Confirmed accurate down to small countries (Monaco, Singapore,
Malta, Liechtenstein) at 50m resolution.

Recreated at checkpoint 28 (office=research batch) because the identical
logic from checkpoint 27 (leisure=hackerspace batch) was only ever written
inline in a scratchpad script and lost when that session ended - keep this
version in the repo so the next batch that has lots of raw lat/lon (OSM
Overpass, or any other geo source) doesn't have to redo it a third time.

Usage:
    from country_from_latlon import CountryLookup
    lookup = CountryLookup()  # downloads/caches ne50.geojson next to this file
    country = lookup.country_for(lon, lat)  # -> ROSTER-style name or None

NAME_OVERRIDE below maps Natural Earth's NAME field (often abbreviated, e.g.
"Bosnia and Herz.", or using a different convention than ROSTER, e.g.
"Czechia") to the string ROSTER actually uses - checked against ROSTER's
existing distribution before each batch that uses this (majority variant
wins when ROSTER already has more than one spelling, e.g. "Russian
Federation" over "Russia", "Turkey" over "Turkiye"). Add to this dict rather
than editing the raw Natural Earth data if a new mismatch turns up.
"""
import json
import os
import urllib.request

NE_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_ne50_countries_cache.geojson")

NAME_OVERRIDE = {
    "United States of America": "United States",
    "Czechia": "Czech Republic",
    "Russia": "Russian Federation",
    "Côte d'Ivoire": "Ivory Coast",
    "Dem. Rep. Congo": "DR Congo",
    "Bosnia and Herz.": "Bosnia and Herzegovina",
    "Central African Rep.": "Central African Republic",
    "Dominican Rep.": "Dominican Republic",
    "Antigua and Barb.": "Antigua and Barbuda",
    "Eq. Guinea": "Equatorial Guinea",
    "St. Kitts and Nevis": "Saint Kitts and Nevis",
    "St. Vin. and Gren.": "Saint Vincent and the Grenadines",
    "Solomon Is.": "Solomon Islands",
    "Marshall Is.": "Marshall Islands",
    "Cayman Is.": "Cayman Islands",
    "Turks and Caicos Is.": "Turks and Caicos Islands",
    "Faeroe Is.": "Faroe Islands",
    "Falkland Is.": "Falkland Islands",
    "Fr. Polynesia": "French Polynesia",
    "W. Sahara": "Western Sahara",
    "U.S. Virgin Is.": "U.S. Virgin Islands",
    "British Virgin Is.": "British Virgin Islands",
    "N. Mariana Is.": "Northern Mariana Islands",
    "S. Sudan": "South Sudan",
}


def _point_in_ring(x, y, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-15) + xi):
            inside = not inside
        j = i
    return inside


def _point_in_polys(x, y, polys):
    for poly in polys:
        if not poly:
            continue
        if _point_in_ring(x, y, poly[0]):
            if not any(_point_in_ring(x, y, hole) for hole in poly[1:]):
                return True
    return False


class CountryLookup:
    def __init__(self, geojson_path=None):
        path = geojson_path or CACHE_PATH
        if not os.path.exists(path):
            req = urllib.request.Request(NE_URL, headers={"User-Agent": "Mozilla/5.0 (roster-tools)"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            with open(path, "wb") as f:
                f.write(data)
        with open(path, encoding="utf-8") as f:
            geo = json.load(f)
        self._features = []
        for feat in geo["features"]:
            name = feat["properties"].get("NAME")
            if not name:
                continue
            rname = NAME_OVERRIDE.get(name, name)
            geom = feat["geometry"]
            if geom["type"] == "Polygon":
                polys = [geom["coordinates"]]
            elif geom["type"] == "MultiPolygon":
                polys = geom["coordinates"]
            else:
                continue
            xs, ys = [], []
            for poly in polys:
                for ring in poly:
                    for x, y in ring:
                        xs.append(x)
                        ys.append(y)
            if not xs:
                continue
            self._features.append((rname, polys, (min(xs), min(ys), max(xs), max(ys))))

    def country_for(self, lon, lat):
        for rname, polys, (minx, miny, maxx, maxy) in self._features:
            if lon < minx or lon > maxx or lat < miny or lat > maxy:
                continue
            if _point_in_polys(lon, lat, polys):
                return rname
        return None
