import argparse
from file_manager import actions


def build_parser():
    parser = argparse.ArgumentParser(
        description="File Manager CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    copy_parser = subparsers.add_parser("copy", help="Copy file")
    copy_parser.add_argument("path")

    delete_parser = subparsers.add_parser("delete", help="Delete file/folder")
    delete_parser.add_argument("path")

    count_parser = subparsers.add_parser("count", help="Count files recursively")
    count_parser.add_argument("path")

    find_parser = subparsers.add_parser("find", help="Find files by regex")
    find_parser.add_argument("path")
    find_parser.add_argument("--pattern", required=True)

    date_parser = subparsers.add_parser("add-date", help="Add creation date")
    date_parser.add_argument("path")
    date_parser.add_argument("--recursive", action="store_true")

    analyse_parser = subparsers.add_parser("analyse", help="Analyse folder")
    analyse_parser.add_argument("path")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "copy":
            result = actions.copy_file(args.path)
            print(f"Copied to: {result}")

        elif args.command == "delete":
            actions.delete_path(args.path)
            print("Deleted successfully")

        elif args.command == "count":
            total = actions.count_files(args.path)
            print(f"Total files: {total}")

        elif args.command == "find":
            files = actions.find_files(args.path, args.pattern)
            for f in files:
                print(f)

        elif args.command == "add-date":
            renamed = actions.add_creation_date(args.path, args.recursive)
            print("Renamed files:")
            for r in renamed:
                print(r)

        elif args.command == "analyse":
            total, data = actions.analyse_folder(args.path)
            print(f"Full size: {total} bytes")
            for name, size in data.items():
                print(f"- {name}: {size} bytes")

    except Exception as e:
        print(f"Error: {e}")
