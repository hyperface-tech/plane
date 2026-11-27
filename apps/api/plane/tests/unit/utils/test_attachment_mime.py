# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

"""The web app sends an empty MIME type for files it cannot identify by content (.txt, .csv,
.md, ...), and the attachment endpoints rejected them with "Invalid file type."."""

import pytest
from django.conf import settings

from plane.utils.attachment_mime import resolve_attachment_mime_type


@pytest.mark.unit
@pytest.mark.parametrize(
    "name, expected",
    [
        ("notes.txt", "text/plain"),
        ("report.csv", "text/csv"),
        ("payload.json", "application/json"),
        ("README.md", "text/markdown"),
        ("server.LOG", "text/plain"),
        ("config.yaml", "text/plain"),
        ("dump.sql", "text/plain"),
    ],
)
def test_empty_type_is_guessed_from_extension(name, expected):
    assert resolve_attachment_mime_type("", name) == expected
    assert resolve_attachment_mime_type(False, name) == expected
    assert expected in settings.ATTACHMENT_MIME_TYPES


@pytest.mark.unit
def test_client_type_is_kept():
    # Content-based detection wins over the extension: a PE binary renamed to .txt stays rejected.
    assert resolve_attachment_mime_type("application/x-msdownload", "setup.txt") == "application/x-msdownload"
    assert resolve_attachment_mime_type("image/png", "photo.png") == "image/png"


@pytest.mark.unit
@pytest.mark.parametrize("name", ["blob.bin", "noextension", "archive.unknownext", "", None])
def test_unknown_or_binary_extension_stays_empty(name):
    assert not resolve_attachment_mime_type("", name)
