import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays all contacts with functional Edit/Delete and Light/Dark mode."""
    contacts_list_view.controls.clear()

    # Set colors depending on theme
    if page.theme_mode == ft.ThemeMode.LIGHT:
        card_bg = "#FFFFFF"
        text_color = "#6A1B9A"
        icon_color = "#6A1B9A"
    else:
        card_bg = "#1E1E1E"
        text_color = "#D1C4E9"
        icon_color = "#D1C4E9"

    contacts = get_all_contacts_db(db_conn, search_term)
    for contact in contacts:
        contact_id, name, phone, email = contact
        contacts_list_view.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=12,
                    border_radius=12,
                    bgcolor=card_bg,
                    shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color="#00000012"),
                    content=ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Column(
                                [
                                    ft.Text(name, size=18, weight="bold", color=text_color),
                                    ft.Row([ft.Icon("phone", color=icon_color), ft.Text(phone, color=text_color)]),
                                    ft.Row([ft.Icon("email", color=icon_color), ft.Text(email, color=text_color)]),
                                ],
                                expand=True,
                            ),
                            ft.PopupMenuButton(
                                icon="more_vert",
                                icon_color=icon_color,
                                items=[
                                    ft.PopupMenuItem(
                                        text="Edit",
                                        on_click=lambda e, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view)
                                    ),
                                    ft.PopupMenuItem(
                                        text="Delete",
                                        on_click=lambda e, cid=contact_id: confirm_delete(page, cid, db_conn, contacts_list_view)
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        )
    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn):
    name_input, phone_input, email_input = inputs
    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value)
    for field in inputs:
        field.value = ""
    display_contacts(page, contacts_list_view, db_conn)
    page.update()


def confirm_delete(page, contact_id, db_conn, contacts_list_view):
    def yes_delete(e):
        delete_contact_db(db_conn, contact_id)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete", color="#6A1B9A"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, "open", False) or page.update()),
            ft.TextButton("Yes", on_click=yes_delete),
        ],
    )
    page.open(dialog)


def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    contact_id, name, phone, email = contact

    edit_name = ft.TextField(label="Name", value=name, border_radius=8)
    edit_phone = ft.TextField(label="Phone", value=phone, border_radius=8)
    edit_email = ft.TextField(label="Email", value=email, border_radius=8)

    def save_and_close(e):
        update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    # Set dialog colors based on theme
    dlg_bg = "#FFFFFF" if page.theme_mode == ft.ThemeMode.LIGHT else "#1E1E1E"

    dialog_content = ft.Column([edit_name, edit_phone, edit_email], tight=True, spacing=10)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact", color="#6A1B9A"),
        content=ft.Container(
            content=dialog_content,
            padding=15,
            border_radius=12,
            bgcolor=dlg_bg,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="#00000012")
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, "open", False) or page.update()),
            ft.TextButton("Save", on_click=save_and_close),
        ],
    )
    page.open(dialog)
