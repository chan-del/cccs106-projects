import flet as ft
from db_connection import connect_db
import mysql.connector

def main(page: ft.Page):
    # Page configuration
    page.title = "User Login"
    page.window_width = 400
    page.window_height = 350
    page.window_center()
    page.window_frameless = True
    page.bgcolor = ft.Colors.AMBER_ACCENT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # UI Controls
    title = ft.Text("User Login", size=20, weight=ft.FontWeight.BOLD, font_family="Arial", text_align=ft.TextAlign.CENTER)

    username_field = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=300,
        autofocus=True,
        icon=ft.icons.PERSON,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
    )

    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=300,
        password=True,
        can_reveal_password=True,
        icon=ft.icons.LOCK,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
    )

    # Login logic
    async def login_click(e):
        success_dialog = ft.AlertDialog(
            title=ft.Text("Login Successful"),
            content=ft.Text(f"Welcome, {username_field.value}!"),
            actions=[ft.TextButton("OK", on_click=lambda e: page.dialog.close())],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            icon=ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.Colors.GREEN)
        )

        failure_dialog = ft.AlertDialog(
            title=ft.Text("Login Failed"),
            content=ft.Text("Invalid username or password"),
            actions=[ft.TextButton("OK", on_click=lambda e: page.dialog.close())],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            icon=ft.Icon(ft.icons.ERROR, color=ft.Colors.RED)
        )

        invalid_input_dialog = ft.AlertDialog(
            title=ft.Text("Input Error"),
            content=ft.Text("Please enter username and password"),
            actions=[ft.TextButton("OK", on_click=lambda e: page.dialog.close())],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            icon=ft.Icon(ft.icons.INFO, color=ft.Colors.BLUE)
        )

        database_error_dialog = ft.AlertDialog(
            title=ft.Text("Database Error"),
            content=ft.Text("An error occurred while connecting to the database"),
            actions=[ft.TextButton("OK", on_click=lambda e: page.dialog.close())]
        )

        # Input validation
        if not username_field.value or not password_field.value:
            page.dialog = invalid_input_dialog
            page.dialog.open = True
            page.update()
            return

        # Database authentication
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username_field.value, password_field.value))
            result = cursor.fetchone()
            conn.close()

            if result:
                page.dialog = success_dialog
            else:
                page.dialog = failure_dialog

            page.dialog.open = True
            page.update()
        except mysql.connector.Error:
            page.dialog = database_error_dialog
            page.dialog.open = True
            page.update()

    login_button = ft.ElevatedButton(
        "Login",
        on_click=login_click,
        width=100,
        icon=ft.icons.LOGIN
    )

    # Layout
    page.add(
        title,
        ft.Container(
            content=ft.Column(
                [username_field, password_field],
                spacing=20
            ),
        ),
        ft.Container(
            content=login_button,
            alignment=ft.alignment.top_right,
            margin=ft.margin.only(top=0, right=20, bottom=40, left=0)
        )
    )

ft.app(target=main)

