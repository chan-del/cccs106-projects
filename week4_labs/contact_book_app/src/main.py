import flet as ft
import database
import app_logic

def main(page: ft.Page):
    page.title = "Contact Book App"
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT

    # Set default font globally via Theme
    page.theme = ft.Theme(font_family="Poppins")

    # Initialize database connection
    db_conn = database.init_db()

    # Title
    title = ft.Text("Enter Contact Details:", size=24, weight="bold")

    # Contact list view
    contacts_list = ft.ListView(expand=True, spacing=10, padding=10)

    # Input fields
    name_field = ft.TextField(label="Name", width=300)
    phone_field = ft.TextField(label="Phone", width=300)
    email_field = ft.TextField(label="Email", width=300)

    # Search field
    search_field = ft.TextField(
        label="Search",
        width=300,
        on_change=lambda e: app_logic.display_contacts(
            page, contacts_list, db_conn, search_field.value
        ),
    )

    # Add button event
    def add_contact_handler(e):
        if not name_field.value.strip():
            name_field.error_text = "Name cannot be empty"
            page.update()
            return

        if phone_field.value.strip() and email_field.value.strip():
            name_field.error_text = None
            app_logic.add_contact(
                page,
                (name_field, phone_field, email_field),
                contacts_list,
                db_conn,
            )
        else:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Please fill all fields"))
            page.snack_bar.open = True
            page.update()

    add_button = ft.ElevatedButton("Add Contact", on_click=add_contact_handler)

    # Dark mode toggle
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if theme_switch.value else ft.ThemeMode.LIGHT
        app_logic.display_contacts(page, contacts_list, db_conn)
        page.update()

    theme_switch = ft.Switch(
        label="Dark Mode",
        value=False,  
        on_change=toggle_theme,
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Contact Book"),
        actions=[theme_switch],
        bgcolor="#D1B3FF",
    )

    # Layout
    page.add(
        title,
        name_field,
        phone_field,
        email_field,
        add_button,
        search_field,
        contacts_list,
    )

    # Load existing contacts at start
    app_logic.display_contacts(page, contacts_list, db_conn)

ft.app(target=main)
