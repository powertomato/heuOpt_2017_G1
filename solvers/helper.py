def _edges(pages):
    for pageIdx in pages:
        for edge in pages[pageIdx]:
            yield edge