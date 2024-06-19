import flet as ft
import random


class ColoredBar(ft.BarChartRod):
    def __init__(self, y: float, hovered: bool = False, width: int = 30):
        super().__init__()
        self.hovered = hovered
        self.y = y
        self.width = width

    def _before_build_command(self):
        self.to_y = self.y  if self.hovered else self.y
        self.color = ft.colors.GREEN_200 if self.hovered else ft.colors.GREEN_200 #ft.colors.GREEN_50
        self.border_side = (
            ft.BorderSide(width=1, color=ft.colors.GREEN_400)
            if self.hovered
            else ft.BorderSide(width=1, color=ft.colors.WHITE)
        )
        super()._before_build_command()

    def _build(self):
        self.tooltip = str(self.y)
        self.width = 22
        self.color = ft.colors.WHITE
        self.bg_to_y = 20
        self.bg_color = ft.colors.GREEN_300

class DataVisualization:
    def __init__(self, page: ft.Page):
        self.page = page
        self.standings_data = [
            {"university": "Group 1", "total_km": 1500},
            {"university": "Group 2", "total_km": 1400},
            {"university": "Group 3", "total_km": 1300},
            {"university": "Group 4", "total_km": 1200},
            {"university": "Group 5", "total_km": 1100},
        ]
        self.chart_container = ft.Column()
        self.table_container = ft.Column()
        self.init_ui()

    def init_ui(self):
        self.page.add(
            ft.Text("University League", size=35, weight=ft.FontWeight.BOLD),
            ft.Text("Current Standings", size=24, weight=ft.FontWeight.BOLD),
            self.chart_container,
            ft.Text("Table", size=24, weight=ft.FontWeight.BOLD),
            self.table_container,
            ft.ElevatedButton(text="Generate Random Data", on_click=self.generate_random_data)
        )
        self.update_chart()
        self.update_table()

    def update_chart(self):
        chart = self.create_chart()
        self.chart_container.controls.clear()
        self.chart_container.controls.append(chart)
        self.chart_container.update()

    def create_chart(self):
        chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=index,
                    bar_rods=[ColoredBar(data["total_km"])],
                
                ) for index, data in enumerate(self.standings_data)
            ],
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=index, label=ft.Text(data["university"])) for index, data in enumerate(self.standings_data)
                ]
            ),
            #on_chart_event=on_chart_event,
            interactive=True,
            
        )
        return chart
    


    def update_table(self):
        table = self.create_standings_table()
        self.table_container.controls.clear()
        self.table_container.controls.append(table)
        self.table_container.update()

    def create_standings_table(self):
        rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(data["university"])), ft.DataCell(ft.Text(str(data["total_km"])))]) for data in self.standings_data]
        columns = [ft.DataColumn(ft.Text("University")), ft.DataColumn(ft.Text("Total KM"))]
        return ft.DataTable(columns=columns, rows=rows)

    def generate_random_data(self, event):
        index = random.randint(0, len(self.standings_data) - 1)
        self.standings_data[index]["total_km"] += random.randint(1, 42)
        self.update_chart()
        self.update_table()
        

class FileUploader:
    def __init__(self, page: ft.Page):
        self.page = page
        self.init_ui()

    def init_ui(self):
        self.files = ft.Column()
        select_files_button = ft.ElevatedButton("Select files...", icon=ft.icons.FOLDER_OPEN, on_click=self.pick_files)
        self.upload_button = ft.ElevatedButton("Upload", icon=ft.icons.UPLOAD, on_click=self.upload_files, disabled=True)
        self.page.add(select_files_button, self.files, self.upload_button)

    def pick_files(self, e):
        file_picker = ft.FilePicker(allow_multiple=True, on_result=self.on_file_selection, on_upload=self.on_upload_progress)
        self.page.overlay.append(file_picker)

    def on_file_selection(self, event: ft.FilePickerResultEvent):
        self.upload_button.disabled = not event.files
        self.files.controls.clear()
        for file in event.files:
            progress = ft.ProgressRing(value=0)
            self.files.controls.append(ft.Row([progress, ft.Text(file.name)]))

    def on_upload_progress(self, event: ft.FilePickerUploadEvent):
        # Update progress bar logic here
        pass

    def upload_files(self, e):
        # Upload files logic here
        pass
    

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # Create instances of the functionalities
    data_visualization = DataVisualization(page)
    file_uploader = FileUploader(page)

ft.app(main)
