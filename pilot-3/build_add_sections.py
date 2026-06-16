"""Attach section headings to cmp_coding_sample.json unit records.

Headings come from the coding manual's printed exercise (Werner & Volkens 2010,
section 5 / Klingemann et al. 2006, Appendix II) and are matched to units by text
anchor. Coders saw the unitised text with these headings; Decision Rules 2 and 11
make the surrounding paragraph and the section heading coding cues, so they are
carried per-unit for the in-context condition.

Re-runnable: it only sets fields, so running twice is a no-op.
"""
import json
import pathlib

p = pathlib.Path("pilot-3/cmp_coding_sample.json")
data = json.loads(p.read_text())

# (manifesto, start_seq, end_seq, per-unit section string)
spans = [
    ("GB", 1, 22, "Working together for Britain"),
    ("GB", 23, 44, "THE IMMEDIATE CRISIS: JOBS AND PRICES"),
    ("GB", 45, 58, "STRATEGY FOR INDUSTRIAL SUCCESS"),
    ("GB", 59, 63, "PARTNERSHIP IN INDUSTRY"),
    ("GB", 64, 70, "PARTICIPATION AT WORK"),
    ("GB", 71, 81, "GOVERNMENT AND INDUSTRY — Priority for Industry"),
    ("GB", 82, 91, "GOVERNMENT AND INDUSTRY — New and Small Business"),
    ("GB", 92, 98, "GOVERNMENT AND INDUSTRY — Agriculture and Fisheries"),
    ("GB", 99, 107, "Education and training"),
    ("NZ", 1, 21, "THE ECONOMY"),
    ("NZ", 22, 45, "SUPERANNUATION"),
    ("NZ", 46, 72, "WOMEN'S RIGHTS"),
]


def section_for(man, seq):
    for m, a, b, s in spans:
        if m == man and a <= seq <= b:
            return s
    raise ValueError(f"no section for {man}-{seq}")


for u in data["units"]:
    u["section"] = section_for(u["manifesto"], u["sequence"])

gb_sections = [
    {"heading": "Working together for Britain", "level": "title",
     "first_unit": "GB-001", "last_unit": "GB-022"},
    {"heading": "THE IMMEDIATE CRISIS: JOBS AND PRICES", "level": "section",
     "first_unit": "GB-023", "last_unit": "GB-044"},
    {"heading": "STRATEGY FOR INDUSTRIAL SUCCESS", "level": "section",
     "first_unit": "GB-045", "last_unit": "GB-058"},
    {"heading": "PARTNERSHIP IN INDUSTRY", "level": "section",
     "first_unit": "GB-059", "last_unit": "GB-063"},
    {"heading": "PARTICIPATION AT WORK", "level": "section",
     "first_unit": "GB-064", "last_unit": "GB-070"},
    {"heading": "GOVERNMENT AND INDUSTRY", "level": "section",
     "first_unit": "GB-071", "last_unit": "GB-098",
     "subsections": [
         {"heading": "Priority for Industry", "first_unit": "GB-071", "last_unit": "GB-081"},
         {"heading": "New and Small Business", "first_unit": "GB-082", "last_unit": "GB-091"},
         {"heading": "Agriculture and Fisheries", "first_unit": "GB-092", "last_unit": "GB-098"},
     ]},
    {"heading": "Education and training", "level": "section",
     "first_unit": "GB-099", "last_unit": "GB-107"},
]
nz_sections = [
    {"heading": "THE ECONOMY", "level": "section",
     "first_unit": "NZ-001", "last_unit": "NZ-021"},
    {"heading": "SUPERANNUATION", "level": "section",
     "first_unit": "NZ-022", "last_unit": "NZ-045"},
    {"heading": "WOMEN'S RIGHTS", "level": "section",
     "first_unit": "NZ-046", "last_unit": "NZ-072"},
]
for m in data["metadata"]["manifestos"]:
    if m["id"] == "GB":
        m["sections"] = gb_sections
    elif m["id"] == "NZ":
        m["sections"] = nz_sections

data["metadata"]["section_note"] = (
    "Section headings come from the coding manual's printed exercise (Werner & "
    "Volkens 2010, section 5; Klingemann et al. 2006, Appendix II), matched to "
    "units by text anchor and carried for the in-context condition (Decision "
    "Rules 2 and 11 make the surrounding paragraph and section heading coding "
    "cues). NOTE: the GB unit sequence — which matches the master-coder files "
    "and the codes.log columns, i.e. the order coders actually coded in — places "
    "THE IMMEDIATE CRISIS (GB-023..044) before STRATEGY FOR INDUSTRIAL SUCCESS "
    "(GB-045..058), the reverse of the manual's print order. The 'Working "
    "together for Britain' span is the untitled introduction (the document "
    "title is its only heading)."
)
data["metadata"]["category_scheme_note"] = (
    "The inline 'categories' object lists only codes present in the master/gold "
    "coding, as a coverage aid. The full instruction-parity option space — all "
    "56 standard categories + 000 uncoded, with handbook definitions and rile "
    "mapping — lives in categories.json and is what both the human coders and "
    "the models are offered."
)

p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("units updated:", len(data["units"]))
print("sample:", data["units"][22]["unit_id"], "->", data["units"][22]["section"])
print("sample:", data["units"][44]["unit_id"], "->", data["units"][44]["section"])
