# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

# Python imports
import mimetypes

# Text formats that Python's mimetypes table does not map, or maps differently across hosts
# (it also reads the system's mime.types files, e.g. .sql is application/x-sql on macOS).
# Checked first so the result does not depend on the host.
_TEXT_EXTENSION_TYPES = {
    "log": "text/plain",
    "yaml": "text/plain",
    "yml": "text/plain",
    "sql": "text/plain",
    "md": "text/markdown",
    "markdown": "text/markdown",
}


def resolve_attachment_mime_type(mime_type, name):
    """Return the client-sent MIME type, or one guessed from the file name when it is empty.

    The web app detects an upload's type from its leading bytes (the ``file-type`` library).
    Plain-text formats (.txt, .csv, .md, .json, .log, ...) have no such signature, so it sends an
    empty type and the attachment endpoints reject the file with "Invalid file type.".

    A non-empty type is returned unchanged, so a file whose content was recognised keeps that type
    whatever its extension. The result must still pass the ``ATTACHMENT_MIME_TYPES`` check.
    """
    if mime_type or not name:
        return mime_type

    extension = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    guessed = _TEXT_EXTENSION_TYPES.get(extension) or mimetypes.guess_type(name)[0]
    if guessed == "application/octet-stream":
        guessed = None  # a generic binary guess says nothing about the content
    return guessed or mime_type
