#!/usr/bin/env bash
# Shared helpers for article demo scripts.

resolve_article_context_from_script() {
  local script_dir="$1"
  if [[ -z "$script_dir" ]]; then
    echo "Error: resolve_article_context_from_script requires script_dir" >&2
    return 1
  fi

  SCRIPT_DIR="$script_dir"
  ARTICLE_ABS="$(cd "$SCRIPT_DIR/.." && pwd)"
  ARTICLE_NAME="$(basename "$ARTICLE_ABS")"
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
  ARTICLE_REL="content/articles/$ARTICLE_NAME"
  OUT_DIR="$ARTICLE_REL/output"
  WORK_DIR="$OUT_DIR/work"
  FINAL_DIR="$OUT_DIR/final"
}

ensure_article_output_dirs() {
  mkdir -p "$REPO_ROOT/$OUT_DIR" "$REPO_ROOT/$WORK_DIR" "$REPO_ROOT/$FINAL_DIR"
}
