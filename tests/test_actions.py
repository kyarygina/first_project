import os
import unittest
import tempfile
from file_manager import actions


class TestCopyFile(unittest.TestCase):

    def test_copy_file_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_path = os.path.join(tmp, "test.txt")
            with open(file_path, "w") as f:
                f.write("hello")

            new_path = actions.copy_file(file_path)

            self.assertTrue(os.path.exists(new_path))
            self.assertNotEqual(file_path, new_path)

    def test_copy_file_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_path = os.path.join(tmp, "data.txt")
            with open(file_path, "w") as f:
                f.write("12345")

            new_path = actions.copy_file(file_path)

            with open(new_path, "r") as f:
                content = f.read()

            self.assertEqual(content, "12345")

    def test_copy_file_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            actions.copy_file("nonexistent.txt")


class TestDeletePath(unittest.TestCase):

    def test_delete_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_path = os.path.join(tmp, "file.txt")
            open(file_path, "w").close()

            actions.delete_path(file_path)
            self.assertFalse(os.path.exists(file_path))

    def test_delete_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = os.path.join(tmp, "folder")
            os.mkdir(folder)

            actions.delete_path(folder)
            self.assertFalse(os.path.exists(folder))

    def test_delete_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            actions.delete_path("fake_path")


class TestCountFiles(unittest.TestCase):

    def test_count_empty_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(actions.count_files(tmp), 0)

    def test_count_files_simple(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "a.txt"), "w").close()
            open(os.path.join(tmp, "b.txt"), "w").close()

            self.assertEqual(actions.count_files(tmp), 2)

    def test_count_files_nested(self):
        with tempfile.TemporaryDirectory() as tmp:
            sub = os.path.join(tmp, "sub")
            os.mkdir(sub)

            open(os.path.join(sub, "a.txt"), "w").close()
            open(os.path.join(tmp, "b.txt"), "w").close()

            self.assertEqual(actions.count_files(tmp), 2)

    def test_count_not_directory(self):
        with tempfile.NamedTemporaryFile() as tmp:
            with self.assertRaises(NotADirectoryError):
                actions.count_files(tmp.name)


class TestFindFiles(unittest.TestCase):

    def test_find_by_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "a.py"), "w").close()
            open(os.path.join(tmp, "b.txt"), "w").close()

            result = actions.find_files(tmp, r".*\.py")
            self.assertEqual(len(result), 1)

    def test_find_nested(self):
        with tempfile.TemporaryDirectory() as tmp:
            sub = os.path.join(tmp, "sub")
            os.mkdir(sub)

            open(os.path.join(sub, "file.py"), "w").close()

            result = actions.find_files(tmp, r".*\.py")
            self.assertEqual(len(result), 1)

    def test_find_no_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "a.txt"), "w").close()

            result = actions.find_files(tmp, r".*\.py")
            self.assertEqual(result, [])

    def test_find_not_directory(self):
        with tempfile.NamedTemporaryFile() as tmp:
            with self.assertRaises(NotADirectoryError):
                actions.find_files(tmp.name, r".*")


class TestAddCreationDate(unittest.TestCase):

    def test_add_date_single_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_path = os.path.join(tmp, "file.txt")
            open(file_path, "w").close()

            renamed = actions.add_creation_date(file_path)

            self.assertEqual(len(renamed), 1)
            self.assertTrue(os.path.exists(renamed[0]))

    def test_add_date_folder_non_recursive(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "a.txt"), "w").close()

            renamed = actions.add_creation_date(tmp)

            self.assertEqual(len(renamed), 1)

    def test_add_date_recursive(self):
        with tempfile.TemporaryDirectory() as tmp:
            sub = os.path.join(tmp, "sub")
            os.mkdir(sub)

            open(os.path.join(sub, "a.txt"), "w").close()

            renamed = actions.add_creation_date(tmp, recursive=True)
            self.assertEqual(len(renamed), 1)

    def test_add_date_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            actions.add_creation_date("fake_path")


class TestAnalyseFolder(unittest.TestCase):

    def test_analyse_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            total, data = actions.analyse_folder(tmp)

            self.assertEqual(total, 0)
            self.assertEqual(data, {})

    def test_analyse_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            file1 = os.path.join(tmp, "a.txt")
            with open(file1, "w") as f:
                f.write("1234")

            total, data = actions.analyse_folder(tmp)

            self.assertTrue(total > 0)
            self.assertIn("a.txt", data)

    def test_analyse_nested(self):
        with tempfile.TemporaryDirectory() as tmp:
            sub = os.path.join(tmp, "sub")
            os.mkdir(sub)

            file1 = os.path.join(sub, "a.txt")
            with open(file1, "w") as f:
                f.write("1234")

            total, data = actions.analyse_folder(tmp)

            self.assertIn("sub", data)

    def test_analyse_not_directory(self):
        with tempfile.NamedTemporaryFile() as tmp:
            with self.assertRaises(NotADirectoryError):
                actions.analyse_folder(tmp.name)
