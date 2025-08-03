import pytest
from core.reviews import ReviewGenerator

def test_review_generation(review_generator):
    reviews = review_generator.generate("Test Product", count=5, suspiciousness="medium")
    
    assert len(reviews) == 5
    for review in reviews:
        assert isinstance(review, dict)
        assert "id" in review
        assert "product" in review
        assert review["product"] == "Test Product"
        assert "rating" in review
        assert 4 <= review["rating"] <= 5
        assert "text" in review
        assert len(review["text"]) > 20
        assert "author" in review
        assert "date" in review
        assert "suspiciousness" in review
        assert review["suspiciousness"] == "medium"

def test_suspiciousness_levels(review_generator):
    for level in ["low", "medium", "high"]:
        reviews = review_generator.generate("Test Product", suspiciousness=level)
        assert reviews[0]["suspiciousness"] == level
        
        if level == "high":
            assert "!" in reviews[0]["text"]  # High suspiciousness tends to have exclamations
        elif level == "low":
            assert "wish" in reviews[0]["text"].lower() or "but" in reviews[0]["text"].lower()

def test_invalid_suspiciousness(review_generator):
    with pytest.raises(ValueError):
        review_generator.generate("Test Product", suspiciousness="invalid_level")

def test_review_structure(review_generator):
    review = review_generator.generate("Test Product")[0]
    assert isinstance(review["id"], str)
    assert isinstance(review["rating"], int)
    assert isinstance(review["text"], str)
    assert isinstance(review["author"], str)
    assert isinstance(review["date"], str)