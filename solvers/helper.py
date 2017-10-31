def _edges(pages):
    for page in pages:
        for edge in page.getAllEdges():
            yield edge