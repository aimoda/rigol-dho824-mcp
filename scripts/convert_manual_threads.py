#!/usr/bin/env python3
"""Convert saved EEVblog forum print pages into structured JSON."""

from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional


@dataclass
class Post:
    """Represents a single forum post."""

    title: str
    author: str
    posted_at: str
    content_html: str
    content_text: str


class ThreadHTMLParser(HTMLParser):
    """Minimal HTML parser tailored to the forum print page layout."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.thread_title: Optional[str] = None
        self.linktree: Optional[str] = None
        self.canonical_url: Optional[str] = None
        self.posts: List[Post] = []

        self._capture: Optional[str] = None
        self._buffer: List[str] = []
        self._body_parts: List[str] = []
        self._current_post: Optional[dict] = None

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        attr_map = {name: value for name, value in attrs}

        if tag == "h1" and attr_map.get("id") == "title":
            self._start_capture("thread_title")
            return

        if tag == "h2" and attr_map.get("id") == "linktree":
            self._start_capture("linktree")
            return

        if tag == "link" and attr_map.get("rel") == "canonical":
            self.canonical_url = attr_map.get("href")
            return

        if tag == "dt" and attr_map.get("class") == "postheader":
            self._start_capture("postheader")
            self._current_post = {}
            return

        if tag == "dd" and attr_map.get("class") == "postbody":
            self._start_capture("postbody")
            self._body_parts = []
            return

        if self._capture == "postbody":
            self._body_parts.append(self.get_starttag_text() or f"<{tag}>")
        elif self._capture == "postheader" and tag == "br":
            self._buffer.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1" and self._capture == "thread_title":
            self.thread_title = self._finish_capture()
            return

        if tag == "h2" and self._capture == "linktree":
            self.linktree = self._finish_capture()
            return

        if tag == "dt" and self._capture == "postheader":
            header_text = self._finish_capture()
            if self._current_post is not None:
                self._populate_post_header(header_text)
            return

        if tag == "dd" and self._capture == "postbody":
            body_html = self._finish_capture()
            if self._current_post is not None:
                body_html = body_html.strip()
                content_text = html_fragment_to_text(body_html)
                self.posts.append(
                    Post(
                        title=self._current_post.get("title", ""),
                        author=self._current_post.get("author", ""),
                        posted_at=self._current_post.get("posted_at", ""),
                        content_html=body_html,
                        content_text=content_text,
                    )
                )
                self._current_post = None
            self._body_parts = []
            return

        if self._capture == "postbody":
            self._body_parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if not data:
            return

        if self._capture == "postbody":
            self._body_parts.append(data)
        elif self._capture in {"thread_title", "linktree", "postheader"}:
            self._buffer.append(data)

    def handle_entityref(self, name: str) -> None:
        text = f"&{name};"
        if self._capture == "postbody":
            self._body_parts.append(text)
        elif self._capture in {"thread_title", "linktree", "postheader"}:
            self._buffer.append(unescape(text))

    def handle_charref(self, name: str) -> None:
        text = f"&#{name};"
        if self._capture == "postbody":
            self._body_parts.append(text)
        elif self._capture in {"thread_title", "linktree", "postheader"}:
            self._buffer.append(unescape(text))

    def handle_startendtag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        if tag == "link":
            attr_map = {name: value for name, value in attrs}
            if attr_map.get("rel") == "canonical":
                self.canonical_url = attr_map.get("href")
            return

        if tag == "br":
            if self._capture == "postbody":
                self._body_parts.append(self.get_starttag_text() or "<br/>")
            elif self._capture in {"thread_title", "linktree", "postheader"}:
                self._buffer.append("\n")
            return

        if self._capture == "postbody":
            self._body_parts.append(self.get_starttag_text() or f"<{tag} />")

    def _start_capture(self, label: str) -> None:
        self._capture = label
        self._buffer = []

    def _finish_capture(self) -> str:
        text = "".join(self._body_parts if self._capture == "postbody" else self._buffer)
        self._capture = None
        self._buffer = []
        return text.strip()

    def _populate_post_header(self, header_text: str) -> None:
        cleaned = re.sub(r"\s+", " ", header_text).strip()
        title = author = posted_at = ""

        match = re.search(r"Title:\s*(.*?)\s*Post by:\s*(.*?)\s+on\s+(.*)", cleaned, re.IGNORECASE)
        if match:
            title, author, posted_at = match.groups()
        else:
            title = cleaned

        if self._current_post is not None:
            self._current_post["title"] = title.strip()
            self._current_post["author"] = author.strip()
            self._current_post["posted_at"] = posted_at.strip()


class PlainTextExtractor(HTMLParser):
    """Utility parser to reduce forum post HTML to readable plain text."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        if tag in {"br"}:
            self.parts.append("\n")
        elif tag in {"p", "div", "blockquote"}:
            if not self.parts or not self.parts[-1].endswith("\n"):
                self.parts.append("\n")
        elif tag == "li":
            if not self.parts or not self.parts[-1].endswith("\n"):
                self.parts.append("\n")
            self.parts.append("- ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"p", "div", "blockquote"}:
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if data:
            self.parts.append(data)


def html_fragment_to_text(fragment: str) -> str:
    """Best-effort conversion from HTML to readable plain text."""
    parser = PlainTextExtractor()
    parser.feed(fragment)
    parser.close()
    text = "".join(parser.parts)
    text = text.replace("\r", "")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def convert_thread(html_path: Path) -> dict:
    """Parse the given HTML file and return a JSON serialisable thread dict."""
    parser = ThreadHTMLParser()
    parser.feed(html_path.read_text(encoding="utf-8"))
    parser.close()

    generated_at = datetime.now(timezone.utc).isoformat()
    return {
        "source_path": str(html_path),
        "generated_at": generated_at,
        "canonical_url": parser.canonical_url,
        "thread_title": parser.thread_title,
        "linktree": parser.linktree,
        "post_count": len(parser.posts),
        "posts": [post.__dict__ for post in parser.posts],
    }


def write_thread_json(html_path: Path, json_path: Path) -> None:
    thread = convert_thread(html_path)
    json_path.write_text(json.dumps(thread, indent=2), encoding="utf-8")


def download_url(url: str, output_path: Path) -> None:
    """Download a URL to a local file."""
    print(f"Downloading {url} to {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Identify ourselves with repo URL
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'rigol-dho824-mcp (https://github.com/aimoda/rigol-dho824-mcp)'}
    )

    with urllib.request.urlopen(req) as response:
        content = response.read()
        output_path.write_bytes(content)

    print(f"Downloaded {len(content):,} bytes")


def main() -> None:
    conversions = [
        (
            "https://www.eevblog.com/forum/index.php?action=printpage;topic=393928.0",
            Path("manuals/hacking-the-rigol-dho800900-scope.html"),
            Path("manuals/hacking-the-rigol-dho800900-scope.json"),
        ),
        (
            "https://www.eevblog.com/forum/index.php?action=printpage;topic=393754.0",
            Path("manuals/rigol-dho804-test-and-compare-thread.html"),
            Path("manuals/rigol-dho804-test-and-compare-thread.json"),
        ),
    ]

    for url, html_path, json_path in conversions:
        # Download HTML if it doesn't exist
        if not html_path.exists():
            download_url(url, html_path)
        else:
            print(f"Using existing {html_path}")

        write_thread_json(html_path, json_path)
        print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
