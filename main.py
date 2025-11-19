"""
Main entry point for the Project KnowledgeBase application.

This module is responsible for parsing command‑line arguments and
dispatching to the appropriate sub‑commands.  It should coordinate
ingestion of projects, searching the knowledge base, and any other
top‑level operations.  For now it contains placeholder logic.
"""

def main() -> None:
    """Entry function for the CLI dispatcher."""
import argparse
    from ingest.ingestion_pipeline import ingest_project
    from query.search import run_query
    from ingest.python_ast import generate_ast_report
    
    parser = argparse.ArgumentParser(description="Project KnowledgeBase CLI")
subparsers = parser.add_subparsers(dest="command")

# Ingest command
ingest_parser = subparsers.add_parser("ingest", help="Ingest a project directory")
ingest_parser.add_argument("--db", required=True, help="Path to the SQLite DB file")
ingest_parser.add_argument("--path", required=True, help="Path to the project root")

# Search command
search_parser = subparsers.add_parser("search", help="Run semantic + graph query")
search_parser.add_argument("--db", required=True, help="Path to the SQLite DB file")
search_parser.add_argument("--query", required=True, help="Natural language query")

# Report command
report_parser = subparsers.add_parser("report", help="Generate symbol/AST report")
report_parser.add_argument("--file", required=True, help="Path to Python file to report on")

args = parser.parse_args()

if args.command == "ingest":
ingest_project(args.db, args.path)
elif args.command == "search":
run_query(args.db, args.query)
elif args.command == "report":
generate_ast_report(args.file)
else:
parser.print_help()


if __name__ == "__main__":
    main()


