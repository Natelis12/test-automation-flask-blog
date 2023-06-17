from unittest.mock import MagicMock

from forms import commentForm


def test_comment_form():
    fake_form = MagicMock()
    fake_comment = commentForm(fake_form)
    assert hasattr(fake_comment, 'comment')
