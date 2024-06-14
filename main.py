import flet as ft


def main(page: ft.Page):
    page.title = "University League"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Example standings data
    standings_data = [
        {"university": "University A", "total_km": 1500},
        {"university": "University B", "total_km": 1400},
        {"university": "University C", "total_km": 1300},
    ]

    def create_standings_table(data):
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(university["university"])),
                    ft.DataCell(ft.Text(str(university["total_km"])))
                ]
            ) for university in data
        ]

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("University")),
                ft.DataColumn(ft.Text("Total KM")),
            ],
            rows=rows,
        )
        return table

    def upload_activity(e):
        # Here you would handle the logic to upload and process the activity
        # For now, just print to console
        print("Activity uploaded:", txt_university.value, txt_km.value)
        # Clear the input fields after submission
        txt_university.value = ""
        txt_km.value = ""
        page.update()

    txt_university = ft.TextField(label="University", width=200)
    txt_km = ft.TextField(label="KM Ran", width=200)

    page.add(
        ft.Column(
            [
                ft.Text("Current Standings", size=24, weight=ft.FontWeight.BOLD),
                create_standings_table(standings_data),
                ft.Text("Upload Activity", size=24, weight=ft.FontWeight.BOLD),
                txt_university,
                txt_km,
                ft.ElevatedButton(text="Upload", on_click=upload_activity),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )


ft.app(main)
