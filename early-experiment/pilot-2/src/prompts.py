"""Prompt construction for each condition.

Pilot-2 holds the codebook block constant -- every condition shows the HIER1
"categories grouped by domain" block and asks for the same answer schema
({"code": ...}). The only thing that changes across conditions is how much
document context surrounds the target sentence:

    BASE     no surrounding text -- the target sentence alone.
    WINDOW   the +/- config.WINDOW_RADIUS neighbouring quasi-sentences.
    FULLDOC  the entire manifesto.

Context, when shown, is rendered as `pos: text` lines (document order) so the
model can locate the target, which is also quoted in the question. Because the
context block does not change with the question, the manifesto prefix is
identical across a manifesto's target sentences (cache-friendly for FULLDOC).
Keeping framing and schema constant is what lets a difference in results be
attributed to the context manipulation rather than to incidental wording.
"""

import config

SYSTEM = (
    "You are an expert annotator applying the Manifesto Project (MARPOR) coding "
    "scheme. You classify a single quasi-sentence from a party election manifesto "
    "into exactly one category. Base your decision only on the category definitions "
    "provided. Respond with a single JSON object and nothing else."
)

_ANSWER = ('Respond with JSON of the form {{"code": "<category code>"}} where '
           "<category code> is exactly one of the codes listed above.")

# Shared instruction for picking within the by-domain codebook block.
_HIER_INTRO = (
    "The categories are organized into policy domains. First decide which domain "
    "the quasi-sentence belongs to, then choose the single best category within "
    "that domain. Each entry is `code: title` followed by its definition."
)


def _messages(user_content):
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_content},
    ]


def build_base_messages(item, cb):
    """BASE: the target sentence alone, no surrounding context (== pilot-1 HIER1)."""
    user = (f"{_HIER_INTRO}\n\nCATEGORIES BY DOMAIN:\n{cb.render_hier1()}\n\n"
            f'QUASI-SENTENCE:\n"{item.text}"\n\n{_ANSWER}')
    return _messages(user)


def _render_lines(lines):
    """lines: list of (pos, text) -> 'pos: text' one per line, document order."""
    return "\n".join(f"{pos}: {text}" for pos, text in lines)


def _context_messages(item, cb, context_block, context_label):
    user = (
        f"{_HIER_INTRO}\n\nCATEGORIES BY DOMAIN:\n{cb.render_hier1()}\n\n"
        f"{context_label} (each line is `pos: text`, in document order):\n"
        f"{context_block}\n\n"
        f"Classify ONLY the quasi-sentence at position {item.pos}, shown again here:\n"
        f'"{item.text}"\n\n'
        "Use the surrounding text only as context to disambiguate; assign exactly "
        f"one code to this sentence. {_ANSWER}"
    )
    return _messages(user)


def build_window_messages(item, cb):
    """WINDOW: target sentence plus +/- config.WINDOW_RADIUS neighbours."""
    r = config.WINDOW_RADIUS
    i = item.target_idx
    window = item.lines[max(0, i - r): i + r + 1]
    return _context_messages(item, cb, _render_lines(window),
                             f"SURROUNDING PASSAGE (the {len(window)} sentences "
                             "nearest the target)")


def build_fulldoc_messages(item, cb):
    """FULLDOC: the entire manifesto as context."""
    return _context_messages(item, cb, _render_lines(item.lines),
                             "FULL MANIFESTO")


# condition -> builder; run_experiment dispatches through this.
BUILDERS = {
    "BASE": build_base_messages,
    "WINDOW": build_window_messages,
    "FULLDOC": build_fulldoc_messages,
}
