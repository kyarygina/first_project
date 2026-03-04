import flet as ft
from file_manager import actions

def main(page: ft.Page):
    page.title = "File Manager GUI"
    page.window_width = 800
    page.window_height = 600
    page.scroll = "auto"

    selected_path = {"value": None}
    result_text = ft.Text()

    # ---------- FILE PICKER ----------
    def on_file_selected(e: ft.FilePickerResultEvent):
        if e.files:
            selected_path["value"] = e.files[0].path
        elif e.path:
            selected_path["value"] = e.path
        path_display.value = selected_path["value"] or ""
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)

    # ---------- UI ELEMENTS ----------
    action_dropdown = ft.Dropdown(
        label="Select action",
        options=[
            ft.dropdown.Option("copy file"),
            ft.dropdown.Option("delete path"),
            ft.dropdown.Option("count files"),
            ft.dropdown.Option("find files"),
            ft.dropdown.Option("add creation date"),
            ft.dropdown.Option("analyse folder"),
        ],
        width=300,
    )

    path_display = ft.TextField(
        label="Selected path",
        read_only=True,
        tooltip="Selected file or folder path will appear here",
        width=500
    )

    pattern_input = ft.TextField(
        label="Pattern (for Find files)",
        tooltip="Enter regex pattern, e.g., .*\\.py",
        width=300,
    )

    recursive_checkbox = ft.Checkbox(
        label="Recursive",
        tooltip="Apply to all subfolders",
    )

    execute_button = ft.ElevatedButton("Execute")

    # ---------- HELPERS ----------
    def show_message(message, color="black"):
        result_text.value = message
        result_text.color = color
        page.update()

    def clear_inputs():
        selected_path["value"] = None
        path_display.value = ""
        pattern_input.value = ""
        recursive_checkbox.value = False
        page.update()

    # ---------- ACTION HANDLER ----------
    def handle_execute(e):
        action = action_dropdown.value
        try:
            if not action:
                show_message("Please select an action.", "red")
                return

            path = selected_path["value"]

            if action == "copy file":
                if not path:
                    show_message("Please select a file to copy.", "red")
                    return
                new_path = actions.copy_file(path)
                show_message(f"Copied to: {new_path}", "green")

            elif action == "delete path":
                if not path:
                    show_message("Please select a file or folder to delete.", "red")
                    return
                actions.delete_path(path)
                show_message("Deleted successfully", "green")

            elif action == "count files":
                if not path:
                    show_message("Please select a folder.", "red")
                    return
                total = actions.count_files(path)
                show_message(f"Total files: {total}", "green")

            elif action == "find files":
                if not path:
                    show_message("Please select a folder to search in.", "red")
                    return
                pattern = pattern_input.value
                if not pattern:
                    show_message("Please enter a pattern.", "red")
                    return
                files = actions.find_files(path, pattern)
                show_message("\n".join(files) if files else "No matches found", "blue")

            elif action == "add creation date":
                if not path:
                    show_message("Please select a file or folder.", "red")
                    return
                renamed = actions.add_creation_date(path, recursive_checkbox.value)
                show_message("Renamed:\n" + "\n".join(renamed), "green")

            elif action == "analyse folder":
                if not path:
                    show_message("Please select a folder.", "red")
                    return
                total, data = actions.analyse_folder(path)
                text = f"Full size: {total} bytes\n"
                for name, size in data.items():
                    text += f"{name}: {size} bytes\n"
                show_message(text, "blue")

        except Exception as ex:
            show_message(f"Error: {str(ex)}", "red")

    execute_button.on_click = handle_execute

    # ---------- DYNAMIC UI BASED ON ACTION ----------
    input_container = ft.Column()

    def update_inputs(e):
        input_container.controls.clear()
        clear_inputs()

        action = action_dropdown.value
        if action == "copy file":
            input_container.controls.append(
                ft.ElevatedButton(
                    "Select File",
                    on_click=lambda e: file_picker.pick_files(allow_multiple=False),
                    tooltip="Choose a file to copy"
                )
            )
            input_container.controls.append(path_display)
            input_container.controls.append(execute_button)

        elif action == "delete path":
            input_container.controls.append(
                ft.Row([
                    ft.ElevatedButton(
                        "Select File",
                        on_click=lambda e: file_picker.pick_files(allow_multiple=False),
                        tooltip="Choose a file to delete"
                    ),
                    ft.ElevatedButton(
                        "Select Folder",
                        on_click=lambda e: file_picker.get_directory_path(),
                        tooltip="Choose a folder to delete"
                    ),
                ])
            )
            input_container.controls.append(path_display)
            input_container.controls.append(execute_button)

        elif action == "count files":
            input_container.controls.append(
                ft.ElevatedButton(
                    "Select Folder",
                    on_click=lambda e: file_picker.get_directory_path(),
                    tooltip="Choose a folder to count files"
                )
            )
            input_container.controls.append(path_display)
            input_container.controls.append(execute_button)

        elif action == "find files":
            input_container.controls.append(
                ft.ElevatedButton(
                    "Select Folder",
                    on_click=lambda e: file_picker.get_directory_path(),
                    tooltip="Choose a folder to search files in"
                )
            )
            input_container.controls.append(path_display)
            input_container.controls.append(pattern_input)
            input_container.controls.append(execute_button)

        elif action == "add creation date":
            input_container.controls.append(
                ft.Row([
                    ft.ElevatedButton(
                        "Select File",
                        on_click=lambda e: file_picker.pick_files(allow_multiple=False),
                        tooltip="Choose a file to rename"
                    ),
                    ft.ElevatedButton(
                        "Select Folder",
                        on_click=lambda e: file_picker.get_directory_path(),
                        tooltip="Choose a folder to rename files"
                    ),
                ])
            )
            input_container.controls.append(path_display)
            input_container.controls.append(recursive_checkbox)
            input_container.controls.append(execute_button)

        elif action == "analyse folder":
            input_container.controls.append(
                ft.ElevatedButton(
                    "Select Folder",
                    on_click=lambda e: file_picker.get_directory_path(),
                    tooltip="Choose a folder to analyse"
                )
            )
            input_container.controls.append(path_display)
            input_container.controls.append(execute_button)

        page.update()

    action_dropdown.on_change = update_inputs

    # ---------- LAYOUT ----------
    page.add(
        ft.Text("File Manager GUI", size=28, weight="bold"),
        action_dropdown,
        input_container,
        ft.Divider(),
        ft.Text("Result:", weight="bold"),
        result_text
    )

def run_gui():
    ft.app(target=main)