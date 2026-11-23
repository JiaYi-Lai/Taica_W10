"""Deterministic citation checks and LLM-assisted support review."""


def validate_structure(draft: dict, evidence: list[dict]) -> list[dict]:
    """Check schema and every citation locator before asking a reviewer to spend a call."""
    issues = []
    if not isinstance(draft, dict):
        return [{"type": "schema", "severity": "error", "claim": "", "source_id": "",
                 "suggested_action": "草稿必須是 JSON 物件。"}]
    claims = draft.get("claims")
    if not isinstance(draft.get("title"), str) or not draft["title"].strip():
        issues.append({"type": "schema", "severity": "error", "claim": "", "source_id": "",
                       "suggested_action": "補上文章標題。"})
    if not isinstance(draft.get("summary"), str) or not draft["summary"].strip():
        issues.append({"type": "schema", "severity": "error", "claim": "", "source_id": "",
                       "suggested_action": "補上文章摘要。"})
    summary_refs = draft.get("summary_refs")
    if not isinstance(summary_refs, list) or not summary_refs:
        issues.append({"type": "missing_citation", "severity": "error",
                       "claim": draft.get("summary", ""), "source_id": "",
                       "suggested_action": "為摘要附上來源段落引用。"})
        summary_refs = []
    if not isinstance(claims, list) or not claims:
        issues.append({"type": "schema", "severity": "error", "claim": "", "source_id": "",
                       "suggested_action": "至少需要一項有引用的主張。"})
        claims = []
    evidence_by_ref = {(item["source_id"], item["paragraph_id"]): item for item in evidence}

    def check_refs(refs, claim_text):
        for ref in refs:
            key = (ref.get("source_id"), ref.get("paragraph_id")) if isinstance(ref, dict) else (None, None)
            if key not in evidence_by_ref:
                issues.append({"type": "invalid_citation", "severity": "error", "claim": claim_text,
                               "source_id": str(key[0] or ""),
                               "suggested_action": "引用須指向本次來源中存在的 source_id 與 paragraph_id。"})

    check_refs(summary_refs, draft.get("summary", ""))
    for claim in claims:
        text = claim.get("text", "") if isinstance(claim, dict) else ""
        refs = claim.get("source_refs", []) if isinstance(claim, dict) else []
        if not isinstance(text, str) or not text.strip():
            issues.append({"type": "schema", "severity": "error", "claim": str(text), "source_id": "",
                           "suggested_action": "主張文字不可空白。"})
        if not isinstance(refs, list) or not refs:
            issues.append({"type": "missing_citation", "severity": "error", "claim": str(text),
                           "source_id": "", "suggested_action": "為主張附上來源段落引用。"})
        else:
            check_refs(refs, str(text))
    return issues


def validate_draft(draft: dict, evidence: list[dict], reviews: dict | None = None) -> dict:
    issues = validate_structure(draft, evidence)
    if reviews is None:
        issues.append({"type": "review_missing", "severity": "error", "claim": "", "source_id": "",
                       "suggested_action": "執行 LLM 來源支持度審查。"})
    else:
        review_rows = reviews.get("reviews") if isinstance(reviews, dict) else None
        if not isinstance(review_rows, list):
            issues.append({"type": "review_schema", "severity": "error", "claim": "", "source_id": "",
                           "suggested_action": "要求審查器依 schema 回傳逐項審查。"})
        else:
            if reviews.get("summary_supported") is not True:
                issues.append({"type": "unsupported_summary", "severity": "error",
                               "claim": draft.get("summary", "") if isinstance(draft, dict) else "",
                               "source_id": "", "suggested_action": reviews.get(
                                   "summary_reason", "請根據來源修訂摘要。")})
            claims = draft.get("claims", []) if isinstance(draft, dict) else []
            by_index = {row.get("claim_index"): row for row in review_rows if isinstance(row, dict)}
            for index, claim in enumerate(claims if isinstance(claims, list) else []):
                row = by_index.get(index)
                if row is None or row.get("supported") is not True:
                    text = claim.get("text", "") if isinstance(claim, dict) else ""
                    issues.append({"type": "unsupported_claim", "severity": "error", "claim": text,
                                   "source_id": "", "suggested_action": (row or {}).get(
                                       "reason", "請刪除或根據來源修訂此主張。")})
    return {"status": "passed" if not issues else "needs_review", "issues": issues}
