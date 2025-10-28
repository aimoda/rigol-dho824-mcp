#!/usr/bin/env python3
"""Convert Rigol forum thread JSON exports to Markdown summaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


DEFAULT_JSON_PATHS = (
    Path("manuals/hacking-the-rigol-dho800900-scope.json"),
    Path("manuals/rigol-dho804-test-and-compare-thread.json"),
)


def build_thread_markdown(data: dict, json_path: Path) -> str:
    """Create a Markdown document from the exported thread structure."""
    posts = data.get("posts") or []
    lines: list[str] = []

    title = (data.get("thread_title") or "").strip()
    if not title and posts:
        title = (posts[0].get("title") or json_path.stem).strip()
    if title:
        lines.append(f"# {title}")
        lines.append("")

    metadata_lines: list[str] = []
    canonical_url = data.get("canonical_url")
    if canonical_url:
        metadata_lines.append(f"- Source: {canonical_url}")

    linktree = data.get("linktree")
    if linktree:
        metadata_lines.append(f"- Context: {linktree}")

    generated_at = data.get("generated_at")
    if generated_at:
        metadata_lines.append(f"- Export generated at: {generated_at}")

    post_count = data.get("post_count")
    if isinstance(post_count, int):
        metadata_lines.append(f"- Post count: {post_count}")

    source_path = data.get("source_path")
    if source_path:
        metadata_lines.append(f"- Source file: {source_path}")

    if metadata_lines:
        lines.extend(metadata_lines)
        lines.append("")

    for index, post in enumerate(posts, start=1):
        heading = (post.get("title") or "").strip() or f"Post {index}"
        lines.append(f"## {heading}")

        author = (post.get("author") or "").strip()
        posted_at = (post.get("posted_at") or "").strip()

        if author:
            lines.append(f"*Author:* {author}")
        if posted_at:
            lines.append(f"*Posted:* {posted_at}")
        if author or posted_at:
            lines.append("")

        body = (post.get("content_text") or "").strip()
        if not body and post.get("content_html"):
            body = (post["content_html"] or "").strip()

        if body:
            lines.append(body)
        else:
            lines.append("_No content available for this post._")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def convert(json_path: Path, output_path: Path) -> None:
    """Load a JSON file and write the Markdown representation."""
    with json_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    markdown = build_thread_markdown(data, json_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Rigol forum thread JSON exports to Markdown."
    )
    parser.add_argument(
        "json_files",
        nargs="*",
        type=Path,
        help="Input JSON files. Defaults to known thread exports if omitted.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Optional output directory for generated Markdown files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    json_paths: Iterable[Path] = args.json_files or DEFAULT_JSON_PATHS

    for json_path in json_paths:
        if not json_path.is_file():
            raise FileNotFoundError(f"JSON file not found: {json_path}")

        output_path = (
            args.output_dir / json_path.with_suffix(".md").name
            if args.output_dir
            else json_path.with_suffix(".md")
        )

        convert(json_path, output_path)
        print(f"Converted {json_path} -> {output_path}")


if __name__ == "__main__":
    main()
