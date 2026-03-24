import unittest
from unittest.mock import patch
from io import StringIO

from file_manager.cli import build_parser, main


class TestCLIParser(unittest.TestCase):

    def test_copy_parser(self):
        parser = build_parser()
        args = parser.parse_args(["copy", "file.txt"])

        self.assertEqual(args.command, "copy")
        self.assertEqual(args.path, "file.txt")

    def test_find_parser(self):
        parser = build_parser()
        args = parser.parse_args(["find", "folder", "--pattern", ".*"])

        self.assertEqual(args.command, "find")
        self.assertEqual(args.path, "folder")
        self.assertEqual(args.pattern, ".*")

    def test_add_date_parser_recursive(self):
        parser = build_parser()
        args = parser.parse_args(["add-date", "folder", "--recursive"])

        self.assertTrue(args.recursive)

    def test_missing_command(self):
        parser = build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args([])


class TestCLIExecution(unittest.TestCase):

    @patch("file_manager.actions.copy_file")
    def test_copy_execution(self, mock_copy):
        mock_copy.return_value = "new_file.txt"

        with patch("sys.argv", ["prog", "copy", "file.txt"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()

        mock_copy.assert_called_once_with("file.txt")
        self.assertIn("Copied to: new_file.txt", fake_out.getvalue())


    @patch("file_manager.actions.delete_path")
    def test_delete_execution(self, mock_delete):
        with patch("sys.argv", ["prog", "delete", "file.txt"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()

        mock_delete.assert_called_once_with("file.txt")
        self.assertIn("Deleted successfully", fake_out.getvalue())


    @patch("file_manager.actions.count_files")
    def test_count_execution(self, mock_count):
        mock_count.return_value = 5

        with patch("sys.argv", ["prog", "count", "folder"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()

        mock_count.assert_called_once_with("folder")
        self.assertIn("Total files: 5", fake_out.getvalue())


    @patch("file_manager.actions.find_files")
    def test_find_execution(self, mock_find):
        mock_find.return_value = ["a.py", "b.py"]

        with patch("sys.argv", ["prog", "find", "folder", "--pattern", ".*"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()

        mock_find.assert_called_once_with("folder", ".*")
        output = fake_out.getvalue()

        self.assertIn("a.py", output)
        self.assertIn("b.py", output)


    @patch("file_manager.actions.add_creation_date")
    def test_add_date_execution(self, mock_add_date):
        mock_add_date.return_value = ["2025-01-01_file.txt"]

        with patch("sys.argv", ["prog", "add-date", "file.txt"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()

        mock_add_date.assert_called_once_with("file.txt", False)
        self.assertIn("Renamed files:", fake_out.getvalue())


    @patch("file_manager.actions.analyse_folder")
    def test_analyse_execution(self, mock_analyse):
        mock_analyse.return_value = (1000, {"file.txt": 1000})

        with patch("sys.argv", ["prog", "analyse", "folder"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()

        mock_analyse.assert_called_once_with("folder")

        output = fake_out.getvalue()
        self.assertIn("Full size: 1000 bytes", output)
        self.assertIn("file.txt: 1000 bytes", output)


    @patch("file_manager.actions.count_files")
    def test_error_handling(self, mock_count):
        mock_count.side_effect = Exception("Test error")

        with patch("sys.argv", ["prog", "count", "folder"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()

        self.assertIn("Error: Test error", fake_out.getvalue())
