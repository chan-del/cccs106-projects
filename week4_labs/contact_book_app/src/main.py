import flet as ft

class TodoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.new_task_input = ft.TextField(
            hint_text="What needs to be done?",
            bgcolor=ft.colors.WHITE,
            expand=True,
            on_submit=self.add_task_from_event
        )
        self.tasks_list = ft.Column()
        self.progress_text = ft.Text("No tasks yet", color=ft.colors.GREY)
        self.progress_bar = ft.ProgressBar(width=600, value=0)

        self.view = ft.Column(
            width=600,
            spacing=20,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task_input,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD_TASK,
                            bgcolor=ft.colors.GREEN,
                            on_click=self.add_clicked
                        )
                    ]
                ),
                ft.Column(
                    spacing=6,
                    controls=[self.progress_text, self.progress_bar]
                ),
                self.tasks_list
            ]
        )

    def add_task_from_event(self, e):
        self.add_task(self.new_task_input.value)

    def add_clicked(self, e):
        self.add_task(self.new_task_input.value)

    def add_task(self, task_name):
        task_name = task_name.strip()
        if not task_name:
            return
        self.tasks_list.controls.append(self.create_task_row(task_name))
        self.new_task_input.value = ""
        self.new_task_input.focus()
        self.update_progress()
        self.page.update()

    def create_task_row(self, task_name):
        task_text = ft.Text(task_name)
        task_container = ft.Container(
            content=task_text,
            bgcolor=ft.colors.YELLOW_100,
            padding=ft.padding.symmetric(horizontal=6, vertical=4),
            border_radius=4
        )

        checkbox = ft.Checkbox(value=False)
        def toggle_checkbox(e):
            if checkbox.value:
                task_text.text_decoration = ft.TextDecoration.LINE_THROUGH
                task_container.bgcolor = ft.colors.LIGHT_GREEN_100
            else:
                task_text.text_decoration = ft.TextDecoration.NONE
                task_container.bgcolor = ft.colors.YELLOW_100
            self.update_progress()
            self.page.update()

        checkbox.on_change = toggle_checkbox

        delete_button = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_color=ft.colors.RED,
            bgcolor=ft.colors.RED_100,
            tooltip="Delete Task"
        )

        def confirm_delete(e):
            def delete_confirmed(e):
                self.tasks_list.controls.remove(task_row)
                self.page.dialog.open = False
                self.update_progress()
                self.page.update()

            def cancel_delete(e):
                self.page.dialog.open = False
                self.page.update()

            self.page.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirm Deletion"),
                content=ft.Text(f"Are you sure you want to delete this task?\n\n{task_name}"),
                actions=[
                    ft.TextButton("Cancel", on_click=cancel_delete),
                    ft.TextButton("Delete", on_click=delete_confirmed)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            self.page.dialog.open = True
            self.page.update()

        delete_button.on_click = confirm_delete

        task_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(spacing=10, controls=[checkbox, task_container]),
                ft.Row(spacing=0, controls=[delete_button])
            ]
        )
        return task_row

    def update_progress(self):
        total = len(self.tasks_list.controls)
        completed = sum(1 for row in self.tasks_list.controls if row.controls[0].controls[0].value)
        if total == 0:
            self.progress_text.value = "No tasks yet"
            self.progress_bar.value = 0
        else:
            self.progress_text.value = f"{completed} of {total} tasks completed"
            self.progress_bar.value = completed / total

def main(page: ft.Page):
    page.title = "Lastname Task Tracker"
    page.window_width = 400
    page.window_height = 700
    page.window_resizable = False
    page.bgcolor = ft.colors.LIGHT_BLUE_50
    page.scroll = "auto"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Manually center the window
    screen_width = page.window.screen.width
    screen_height = page.window.screen.height
    page.window.left = (screen_width - page.window_width) // 2
    page.window.top = (screen_height - page.window_height) // 2

    app = TodoApp(page)
    page.add(app.view)

if __name__ == "__main__":
    ft.app(target=main)
