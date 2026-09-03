from document_search import Document, Index


def test_relevant_document_ranks_first():
    index = Index([Document("a", "python testing guide"), Document("b", "garden flowers")])
    assert index.search("python tests")[0].id == "a"

