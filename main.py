import flet as ft
from file_uploader import FileUploader
from sample_rod import SampleRod
import random

def main(page: ft.Page):
    
    standings_data = [
        {"university": "Group 1", "total_km": 1500},
        {"university": "Group 2", "total_km": 1400},
        {"university": "Group 3", "total_km": 1300},
        {"university": "Group 4", "total_km": 1200},
        {"university": "Group 5", "total_km": 1100},
    ]
    def on_chart_event(e: ft.BarChartEvent):
        for group_index, group in enumerate(chart.bar_groups):
            for rod_index, rod in enumerate(group.bar_rods):
                rod.hovered = e.group_index == group_index and e.rod_index == rod_index
        chart.update()

    chart = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=0,
                bar_rods=[SampleRod(standings_data[0]["total_km"])],
            ),
            ft.BarChartGroup(
                x=1,
                bar_rods=[SampleRod(standings_data[1]["total_km"])],
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[SampleRod(standings_data[2]["total_km"])],
            ),
            ft.BarChartGroup(
                x=3,
                bar_rods=[SampleRod(standings_data[3]["total_km"])],
            ),
            ft.BarChartGroup(
                x=4,
                bar_rods=[SampleRod(standings_data[4]["total_km"])],
            ),

        ],
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=0, label=ft.Text(standings_data[0]["university"])),
                ft.ChartAxisLabel(value=1, label=ft.Text(standings_data[1]["university"])),
                ft.ChartAxisLabel(value=2, label=ft.Text(standings_data[2]["university"])),
                ft.ChartAxisLabel(value=3, label=ft.Text(standings_data[3]["university"])),
                ft.ChartAxisLabel(value=4, label=ft.Text(standings_data[4]["university"])),
                
            ],
        ),
        on_chart_event=on_chart_event,
        interactive=True,
    )
    
    
    def generateRandomData(e):
        # increase a random universities km in standings data by a random number
        random_index = random.randint(0, len(standings_data) - 1)
        random_km = random.randint(1, 42)
        standings_data[random_index]["total_km"] += random_km
        chart.bar_groups[random_index].bar_rods[0].value = standings_data[random_index]["total_km"]
        chart.update()
    

        
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
    
    txt_university = ft.TextField(label="University", width=200)
    txt_km = ft.TextField(label="KM Ran", width=200)

    standings_table = create_standings_table(standings_data)
    
    
    def upload_activity(e):
        print("Activity uploaded:", txt_university.value, txt_km.value)
        txt_university.value = ""
        txt_km.value = ""
        page.update()
    
    # Make sure that the page layout and parent elements are sized correctly
    page.add(
        ft.Text("Current Standings", size=24, weight=ft.FontWeight.BOLD),
        
        ft.Container(
            chart, bgcolor=ft.colors.GREEN_200, padding=10, border_radius=50, expand=True, 
        ),
        
        ft.Column(
            [
                ft.Text("Table", size=24, weight=ft.FontWeight.BOLD),
                standings_table,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )       
    )
    
    file_uploader = FileUploader(page)

# Start the app
ft.app(main)
