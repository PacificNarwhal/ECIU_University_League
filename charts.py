import flet as ft

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
