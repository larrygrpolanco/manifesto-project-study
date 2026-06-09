"""Prompt construction for each condition.

Every condition shares the same task framing and the same final answer schema
({"code": ...}); they differ only in which codebook block is shown and, for
HIER2, in whether the decision is split across two calls. Keeping the framing and
schema constant is what lets a difference in results be attributed to the
information/structure manipulation rather than to incidental prompt wording.
"""

SYSTEM = (
    "You are an expert annotator applying the Manifesto Project (MARPOR) coding "
    "scheme. You classify a single quasi-sentence from a party election manifesto "
    "into exactly one category. Base your decision only on the category definitions "
    "provided. Respond with a single JSON object and nothing else."
)

_ANSWER = ('Respond with JSON of the form {{"code": "<category code>"}} where '
           "<category code> is exactly one of the codes listed above.")


def _user(intro, block, text, answer=_ANSWER):
    return (f"{intro}\n\n{block}\n\n"
            f'QUASI-SENTENCE:\n"{text}"\n\n{answer}')


def build_single_messages(condition, item, cb):
    """Messages for the single-call conditions: LABELS, FULL, HIER1."""
    if condition == "LABELS":
        intro = ("Classify the following quasi-sentence into exactly one of these "
                 "categories (shown as `code: title`).\n\nCATEGORIES:")
        block = cb.render_labels()
    elif condition == "FULL":
        intro = ("Classify the following quasi-sentence into exactly one of these "
                 "categories. Each entry is `code: title` followed by its definition; "
                 "attend to the definitions and any exclusion criteria.\n\nCATEGORIES:")
        block = cb.render_full()
    elif condition == "HIER1":
        intro = ("The categories are organized into policy domains. First decide "
                 "which domain the quasi-sentence belongs to, then choose the single "
                 "best category within that domain. Each entry is `code: title` "
                 "followed by its definition.\n\nCATEGORIES BY DOMAIN:")
        block = cb.render_hier1()
    else:
        raise ValueError(f"not a single-call condition: {condition}")
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": _user(intro, block, item.text)},
    ]


def build_hier2_stage1_messages(item, cb):
    """HIER2 stage 1: pick a domain."""
    intro = ("Below are the policy domains of the coding scheme, each followed by "
             "the categories it contains. Decide which single domain best fits the "
             "quasi-sentence.\n\nDOMAINS:")
    answer = ('Respond with JSON of the form {{"domain": <domain number>}} using one '
              "of the domain numbers listed above.")
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": _user(intro, cb.render_domain_menu(), item.text, answer)},
    ]


def build_hier2_stage2_messages(item, cb, domain_code):
    """HIER2 stage 2: pick a category within the chosen domain."""
    name = cb.domain_name(domain_code)
    intro = (f"The quasi-sentence has been assigned to the domain '{name}'. Choose "
             "the single best category within this domain. Each entry is "
             "`code: title` followed by its definition.\n\nCATEGORIES:")
    block = cb.render_domain_categories(domain_code)
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": _user(intro, block, item.text)},
    ]
