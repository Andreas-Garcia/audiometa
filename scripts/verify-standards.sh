#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [path-to-consumer-repo]"
  echo "  With no arguments, uses git root or current directory (for pre-commit)."
  exit 2
}

[[ $# -gt 1 ]] && usage

if [[ $# -eq 0 ]]; then
  if repo_path=$(git rev-parse --show-toplevel 2>/dev/null); then
    :
  else
    repo_path=$PWD
  fi
else
  repo_path=$1
fi

repo_path=$(cd "$repo_path" && pwd)

if [[ ! -d "$repo_path" ]]; then
  echo "Error: repo path not found: $repo_path"
  exit 2
fi

if [[ ! -f "$repo_path/pyproject.toml" ]] && [[ -d "$repo_path/templates/pyproject" ]]; then
  echo "Skipping standards verification (python-project-standards repository has no root pyproject.toml)."
  exit 0
fi

file_contains() {
  local file=$1
  local pattern=$2
  local label=$3

  if [[ ! -f "$file" ]]; then
    echo "Missing file: $label ($file)"
    return 1
  fi
  if command -v rg >/dev/null 2>&1; then
    if ! rg --quiet --fixed-strings "$pattern" "$file"; then
      echo "Missing required snippet in $label: $pattern"
      return 1
    fi
  else
    if ! grep -F -q "$pattern" "$file"; then
      echo "Missing required snippet in $label: $pattern"
      return 1
    fi
  fi
}

required_paths=(
  ".pre-commit-config.yaml"
  "pyproject.toml"
)

missing=0
for rel in "${required_paths[@]}"; do
  if [[ ! -f "$repo_path/$rel" ]]; then
    echo "Missing required file: $rel"
    missing=1
  fi
done

if [[ $missing -ne 0 ]]; then
  echo "Standards verification failed."
  exit 1
fi

snippet_fail=0

file_contains "$repo_path/.pre-commit-config.yaml" "https://github.com/pre-commit/pre-commit-hooks" ".pre-commit-config.yaml" || snippet_fail=1

if command -v rg >/dev/null 2>&1; then
  has_remote_ruff=$(rg --quiet "https://github.com/astral-sh/ruff-pre-commit" "$repo_path/.pre-commit-config.yaml" && echo y || true)
  has_local_ruff=$(
    rg --quiet -e 'id:\s*ruff\s*(#|$)' -e 'id:\s*ruff-check\s*(#|$)' -e 'entry:.*\bruff\s+check\b' "$repo_path/.pre-commit-config.yaml" && echo y || true
  )
else
  has_remote_ruff=$(grep -F "https://github.com/astral-sh/ruff-pre-commit" "$repo_path/.pre-commit-config.yaml" >/dev/null 2>&1 && echo y || true)
  has_local_ruff=$(
    grep -E '(id:[[:space:]]+ruff[[:space:]]*(#|$))|(id:[[:space:]]+ruff-check[[:space:]]*(#|$))|(entry:.*ruff[[:space:]]+check)' "$repo_path/.pre-commit-config.yaml" >/dev/null 2>&1 && echo y || true
  )
fi

if [[ -z "${has_remote_ruff:-}" ]] && [[ -z "${has_local_ruff:-}" ]]; then
  echo "Missing ruff check in .pre-commit-config.yaml (use astral-sh/ruff-pre-commit or a local hook with id ruff / ruff-check or entry running ruff check)."
  snippet_fail=1
fi

if command -v rg >/dev/null 2>&1; then
  has_remote_mypy=$(rg --quiet "(https://github.com/pre-commit/mirrors-mypy|pre-commit.*mypy)" "$repo_path/.pre-commit-config.yaml" && echo y || true)
  has_local_mypy=$(rg --quiet "(^\\s*entry:.*\\bmypy\\b|id:\\s*mypy)" "$repo_path/.pre-commit-config.yaml" && echo y || true)
else
  has_remote_mypy=$(grep -E "(https://github.com/pre-commit/mirrors-mypy|pre-commit.*mypy)" "$repo_path/.pre-commit-config.yaml" >/dev/null 2>&1 && echo y || true)
  has_local_mypy=$(grep -E "(^\\s*entry:.*mypy|id:[[:space:]]*mypy)" "$repo_path/.pre-commit-config.yaml" >/dev/null 2>&1 && echo y || true)
fi

if [[ -z "${has_remote_mypy:-}" ]] && [[ -z "${has_local_mypy:-}" ]]; then
  echo "Missing mypy in .pre-commit-config.yaml (use mirrors-mypy or a local hook running mypy)."
  snippet_fail=1
fi

file_contains "$repo_path/pyproject.toml" "[tool.ruff]" "pyproject.toml" || snippet_fail=1
file_contains "$repo_path/pyproject.toml" "[tool.mypy]" "pyproject.toml" || snippet_fail=1

if ! grep -Fq "[tool.pytest.ini_options]" "$repo_path/pyproject.toml" && [[ ! -f "$repo_path/pytest.ini" ]]; then
  echo "Need [tool.pytest.ini_options] in pyproject.toml or a pytest.ini file."
  snippet_fail=1
fi

has_ci_pre_commit=false
shopt -s nullglob
for wf in "$repo_path/.github/workflows"/*.yml "$repo_path/.github/workflows"/*.yaml; do
  [[ -f "$wf" ]] || continue
  if grep -Fq "pre-commit run" "$wf" || grep -Fq "python-project-standards" "$wf"; then
    has_ci_pre_commit=true
    break
  fi
done
shopt -u nullglob

if [[ ! -d "$repo_path/.github/workflows" ]]; then
  echo "Missing directory: .github/workflows"
  snippet_fail=1
elif [[ "$has_ci_pre_commit" != true ]]; then
  echo "No GitHub workflow references pre-commit (e.g. pre-commit run) or org python-project-standards reusables."
  snippet_fail=1
fi

if [[ $snippet_fail -ne 0 ]]; then
  echo "Standards verification failed due to missing required layout or snippets."
  exit 1
fi

if [[ "${VERIFY_STANDARDS_SKIP_LINT_BASELINE:-}" != "1" ]]; then
  checker="$repo_path/scripts/check_lint_baseline.py"
  if [[ ! -f "$checker" ]]; then
    echo "Missing scripts/check_lint_baseline.py (copy from python-project-standards templates/scripts)."
    exit 1
  fi
  python3 "$checker" "$repo_path"
fi

if [[ ! -f "$repo_path/STANDARDS_VERSION" ]]; then
  echo "Warning: missing STANDARDS_VERSION (recommended when using org python-project-standards)."
else
  echo "Found STANDARDS_VERSION: $(tr -d '[:space:]' <"$repo_path/STANDARDS_VERSION")"
  if [[ "${VERIFY_STANDARDS_SKIP_PIN_CHECK:-}" != "1" ]] && [[ -d "$repo_path/.github/workflows" ]]; then
    ver=$(tr -d '[:space:]' <"$repo_path/STANDARDS_VERSION")
    ver_esc=${ver//./\\.}
    uses_org_std=false
    pin_ok=false
    shopt -s nullglob
    for wf in "$repo_path/.github/workflows"/*.yml "$repo_path/.github/workflows"/*.yaml; do
      [[ -f "$wf" ]] || continue
      if grep -Fq "python-project-standards" "$wf"; then
        uses_org_std=true
      fi
      if grep -F "python-project-standards" "$wf" | grep -qE "@v${ver_esc}([^A-Za-z0-9_.-]|$)"; then
        pin_ok=true
        break
      fi
    done
    shopt -u nullglob
    if [[ "$uses_org_std" == true ]] && [[ "$pin_ok" != true ]]; then
      echo "Error: STANDARDS_VERSION is '${ver}' but no workflow pins python-project-standards to @v${ver}"
      exit 1
    fi
  fi
fi

echo "Standards verification passed."
