from pathlib import Path


def find_sql_dir():
    candidates = []
    try:
        candidates.append(Path(__file__).resolve().parent / "sql")
    except NameError:
        pass

    cwd = Path.cwd()
    candidates += [
        cwd / "src" / "sql",
        cwd / "sql",
        cwd.parent / "src" / "sql",
    ]

    for candidate in candidates:
        if candidate.is_dir():
            return candidate

    matches = list(cwd.rglob("01_infrastructure.sql"))
    if matches:
        return matches[0].parent

    raise FileNotFoundError("Dossier src/sql introuvable")


def run_sql_file(session, filename, show_results=False):
    path = find_sql_dir() / filename
    print(f">> {filename}")

    for statement in path.read_text(encoding="utf-8").split(";"):
        statement = statement.strip()
        if not statement:
            continue

        rows = session.sql(statement).collect()

        if show_results and statement.upper().startswith("SELECT"):
            for row in rows:
                print("  ", row.as_dict())
