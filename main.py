import flet as ft
from file_uploader import FileUploader
from charts import ColoredBar
import random

def main(page: ft.Page):
    global chart
    
    standings_data = [
        {"university": "Group 1", "total_km": 1500},
        {"university": "Group 2", "total_km": 1400},
        {"university": "Group 3", "total_km": 1300},
        {"university": "Group 4", "total_km": 1200},
        {"university": "Group 5", "total_km": 1100},
    ]

    # Doesnt work anymore for some reason - doesnt contribute to functionality     
    # def on_chart_event(e: ft.BarChartEvent):
    #     for group_index, group in enumerate(chart.bar_groups):
    #         for rod_index, rod in enumerate(group.bar_rods):
    #             rod.hovered = e.group_index == group_index and e.rod_index == rod_index
    #     chart.update()

    def create_chart(standings_data):
        chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=index,
                    bar_rods=[ColoredBar(data["total_km"])],
                ) for index, data in enumerate(standings_data)
            ],
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=index, label=ft.Text(data["university"])) for index, data in enumerate(standings_data)
                ],
            ),
            #on_chart_event=on_chart_event,
            interactive=True,
        )
        return chart

    # chart = create_chart(standings_data)
    chart_container = ft.Column([create_chart(standings_data)])

    def generateRandomData(e):
        random_index = random.randint(0, len(standings_data) - 1)
        random_km = random.randint(1, 42)
        standings_data[random_index]["total_km"] += random_km
        #chart.bar_groups[random_index].bar_rods[0].value = standings_data[random_index]["total_km"]

        # Doesnt work
        #chart.update()
        
        # REcreate the chart with new data
        updated_chart = create_chart(standings_data)
        # Replace the old chart with the new one
        chart_container.controls.clear()
        chart_container.controls.append(updated_chart)
        chart_container.update()
        

        # Recreate the table with updated data
        updated_table = create_standings_table(standings_data)
        # Replace the old table with the new one
        table_container.controls.clear()
        table_container.controls.append(updated_table)
        table_container.update()
        
        



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

    # Create a container for the table
    table_container = ft.Column([create_standings_table(standings_data)])


    #chart = create_chart(standings_data)
    page.add(
        
        # ft.Text("University League", size=35, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER), # for some reason doesnt center
        # ft.Text("Current Standings", size=24, weight=ft.FontWeight.BOLD),
        # ft.Container(
        #     chart, 
        #     bgcolor=ft.colors.GREEN_200, 
        #     padding=10, 
        #     border_radius=50, 
        #     expand=True, 
        #     shadow=ft.BoxShadow(blur_radius=10, spread_radius=5, color=ft.colors.BLACK12),
        # ),
        
        ft.Column(
            [
                ft.Text("University League", size=35, weight=ft.FontWeight.BOLD), 
                ft.Text("Current Standings", size=24, weight=ft.FontWeight.BOLD),
                chart_container,
                ft.Text("Table", size=24, weight=ft.FontWeight.BOLD),
                table_container,
                ft.ElevatedButton(text="Generate Random Data", on_click=generateRandomData),
            ],
            alignment=ft.MainAxisAlignment.CENTER, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )       
    )

    #file_uploader = FileUploader(page)

# Start the app
ft.app(main)
