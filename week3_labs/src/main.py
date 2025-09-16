import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    page.title = "User Login"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.height = 350
    page.window.width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT
    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # -------- USERNAME & PASSWORD FIELDS WITH OUTSIDE ICONS -------- #
    username = ft.TextField(
        label="User name",
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
        border_radius=5,
        border_color=ft.Colors.BLACK,
        helper_text="This is your unique identifier",
        width=250
    )

    password = ft.TextField(
        label="Password",
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
        border_radius=5,
        border_color=ft.Colors.BLACK,
        password=True,
        can_reveal_password=True,
        helper_text="This is your secret key",
        width=250
    )

    username_row = ft.Row(
        [ft.Icon(name="person", color="blue"), username],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    password_row = ft.Row(
        [ft.Icon(name="lock", color="blue"), password],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    # -------- LOGIN LOGIC -------- #
    def login_click(e):
        # Invalid Input Check
        if username.value.strip() == "" or password.value.strip() == "":
            invalid_input_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Row([ft.Icon(name="info", color="blue"), ft.Text("Input Error")]),
                content=ft.Text("Please enter username and password", text_align=ft.TextAlign.CENTER),
                actions=[ft.TextButton("OK", on_click=lambda e: page.close(invalid_input_dialog))],
            )
            page.open(invalid_input_dialog)
            return

        try:
            db = connect_db()
            cursor = db.cursor()

            # Query user from database
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username.value, password.value)
            )
            result = cursor.fetchone()

            if result:
                success_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Row([ft.Icon(name="check_circle", color="green"), ft.Text("Login Successful")]),
                    content=ft.Text(f"Welcome, {username.value}!", text_align=ft.TextAlign.CENTER),
                    actions=[ft.TextButton("OK", on_click=lambda e: page.close(success_dialog))],
                )
                page.open(success_dialog)
            else:
                failure_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Row([ft.Icon(name="error", color="red"), ft.Text("Login Failed")]),
                    content=ft.Text("Invalid username or password", text_align=ft.TextAlign.CENTER),
                    actions=[ft.TextButton("OK", on_click=lambda e: page.close(failure_dialog))],
                )
                page.open(failure_dialog)

            cursor.close()
            db.close()

        except Exception as ex:
            database_error_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Row([ft.Icon(name="warning", color="orange"), ft.Text("Database Error")]),
                content=ft.Text(f"An error occurred while connecting to the database:\n{ex}", text_align=ft.TextAlign.CENTER),
                actions=[ft.TextButton("OK", on_click=lambda e: page.close(database_error_dialog))],
            )
            page.open(database_error_dialog)

    # -------- LOGIN BUTTON -------- #
    login_btn = ft.ElevatedButton(
        text="Login",
        icon="login",
        icon_color="black",
        on_click=login_click
    )

    # -------- PAGE LAYOUT -------- #
    page.add(
        ft.Column(
            [
                ft.Text("User Login", size=20, weight=ft.FontWeight.BOLD),
                username_row,
                password_row,
                ft.Row([login_btn], alignment=ft.MainAxisAlignment.END),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(main)
