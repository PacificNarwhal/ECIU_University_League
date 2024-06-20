import flet as ft
import random
from typing import Dict
from get_health_records import extract_running_record


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
        self.prog_bars: Dict[str, ft.ProgressRing] = {}
        self.files = ft.Ref[ft.Column]()
        self.upload_button = ft.Ref[ft.ElevatedButton]()

        self.file_picker = ft.FilePicker(
            on_result=self.file_picker_result, on_upload=self.on_upload_progress
        )

        self.page.overlay.append(self.file_picker)
        self.page.add(
            ft.ElevatedButton(
                "Select files...",
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: self.file_picker.pick_files(allow_multiple=True),
            ),
            ft.Column(ref=self.files),
            ft.ElevatedButton(
                "Upload",
                ref=self.upload_button,
                icon=ft.icons.UPLOAD,
                on_click=self.upload_files,
                disabled=True,
            ),
        )

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        self.upload_button.current.disabled = True if not e.files else False
        self.prog_bars.clear()
        self.files.current.controls.clear()
        if e.files:
            for f in e.files:
                prog = ft.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                self.prog_bars[f.name] = prog
                file_row = ft.Row([prog, ft.Text(f.name)])
                self.files.current.controls.append(file_row)
                if f.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.analyze_image(f)
            self.page.update()

    def analyze_image(self, file):
        print(f"Analyzing image: {file.name}")
        
        running_record=extract_running_record(file.name)
        print("Running Record: ", running_record)
        

    def on_upload_progress(self, e: ft.FilePickerUploadEvent):
        self.prog_bars[e.file_name].value = e.progress
        self.prog_bars[e.file_name].update()

    def upload_files(self, e):
        uf = []
        if self.file_picker.result is not None and self.file_picker.result.files is not None:
            for f in self.file_picker.result.files:
                uf.append(
                    f.name
                    #For online version
                    # ft.FilePickerUploadFile(
                    #     f.name,
                    #     upload_url=self.page.get_upload_url(f.name, 600),
                    # )
                )
            self.file_picker.upload(uf)
            print(uf)

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # Create instances of the functionalities
    data_visualization = DataVisualization(page)
    file_uploader = FileUploader(page)

ft.app(main)
