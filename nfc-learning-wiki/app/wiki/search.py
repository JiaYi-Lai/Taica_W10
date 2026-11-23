"""SQLite FTS5 article index with a LIKE-based fallback."""
import json
import re
import sqlite3
from pathlib import Path


def _article_rows(wiki_dir: Path):
    for metadata_path in sorted(wiki_dir.glob("*.json")):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("validation_status") != "passed":
            continue
        markdown_path = wiki_dir / f"{metadata['article_id']}.md"
        if markdown_path.is_file():
            yield metadata, markdown_path.read_text(encoding="utf-8")


def rebuild_index(wiki_dir: Path = Path("data/wiki"),
                  db_path: Path = Path("data/index/wiki.sqlite")) -> str:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        try:
            connection.execute("CREATE VIRTUAL TABLE IF NOT EXISTS articles USING fts5("
                               "article_id UNINDEXED, title, summary, body, source_ids UNINDEXED)")
            mode = "fts5"
        except sqlite3.OperationalError:
            connection.execute("CREATE TABLE IF NOT EXISTS articles (article_id TEXT PRIMARY KEY, "
                               "title TEXT, summary TEXT, body TEXT, source_ids TEXT)")
            mode = "like"
        connection.execute("DELETE FROM articles")
        for metadata, body in _article_rows(wiki_dir):
            connection.execute("INSERT INTO articles VALUES (?, ?, ?, ?, ?)", (
                metadata["article_id"], metadata["title"], metadata["summary"], body,
                json.dumps(metadata["source_ids"], ensure_ascii=False)))
        connection.commit()
        return mode
    finally:
        connection.close()


def search_articles(query: str, *, db_path: Path = Path("data/index/wiki.sqlite"),
                    limit: int = 10) -> list[dict]:
    if not query.strip() or not db_path.is_file():
        return []
    terms = re.findall(r"[\w-]+", query, flags=re.UNICODE)
    if not terms:
        return []
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        schema = connection.execute("SELECT sql FROM sqlite_master WHERE name='articles'").fetchone()
        if not schema:
            return []
        is_fts = "VIRTUAL TABLE" in (schema[0] or "").upper()
        if is_fts:
            match_query = " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)
            try:
                rows = connection.execute("SELECT article_id,title,summary,source_ids FROM articles "
                    "WHERE articles MATCH ? ORDER BY rank LIMIT ?", (match_query, limit)).fetchall()
            except sqlite3.OperationalError:
                rows = []
        else:
            is_fts = False
            clauses = " OR ".join("title LIKE ? OR summary LIKE ? OR body LIKE ?" for _ in terms)
            params = [pattern for term in terms for pattern in (f"%{term}%",) * 3]
            rows = connection.execute(f"SELECT article_id,title,summary,source_ids FROM articles "
                f"WHERE {clauses} LIMIT ?", (*params, limit)).fetchall()
        if is_fts and not rows:
            clauses = " OR ".join("title LIKE ? OR summary LIKE ? OR body LIKE ?" for _ in terms)
            params = [pattern for term in terms for pattern in (f"%{term}%",) * 3]
            rows = connection.execute(f"SELECT article_id,title,summary,source_ids FROM articles "
                f"WHERE {clauses} LIMIT ?", (*params, limit)).fetchall()
        return [{"article_id": row["article_id"], "title": row["title"],
                 "summary": row["summary"],
                 "source_ids": json.loads(row["source_ids"])} for row in rows]
    finally:
        connection.close()
