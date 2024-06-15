from typing import Dict
from image_analysis import ImageAnalyzer
import flet
from flet import (
    Column,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilePickerUploadEvent,
    FilePickerUploadFile,
    Page,
    ProgressRing,
    Ref,
    Row,
    Text,
    icons,
)

class FileUploader:
    def __init__(self, page: Page):
        self.page = page
        self.prog_bars: Dict[str, ProgressRing] = {}
        self.files = Ref[Column]()
        self.upload_button = Ref[ElevatedButton]()

        self.file_picker = FilePicker(
            on_result=self.file_picker_result, on_upload=self.on_upload_progress
        )

        self.page.overlay.append(self.file_picker)
        self.page.add(
            ElevatedButton(
                "Select files...",
                icon=icons.FOLDER_OPEN,
                on_click=lambda _: self.file_picker.pick_files(allow_multiple=True),
            ),
            Column(ref=self.files),
            ElevatedButton(
                "Upload",
                ref=self.upload_button,
                icon=icons.UPLOAD,
                on_click=self.upload_files,
                disabled=True,
            ),
        )

    def file_picker_result(self, e: FilePickerResultEvent):
        self.upload_button.current.disabled = True if not e.files else False
        self.prog_bars.clear()
        self.files.current.controls.clear()
        if e.files:
            for f in e.files:
                prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                self.prog_bars[f.name] = prog
                file_row = Row([prog, Text(f.name)])
                self.files.current.controls.append(file_row)
                if f.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.analyze_image(f)
            self.page.update()

    def analyze_image(self, file):
        # Placeholder for image analysis function call
        print(f"Analyzing image: {file.name}")

    def on_upload_progress(self, e: FilePickerUploadEvent):
        self.prog_bars[e.file_name].value = e.progress
        self.prog_bars[e.file_name].update()

    def upload_files(self, e):
        uf = []
        if self.file_picker.result is not None and self.file_picker.result.files is not None:
            for f in self.file_picker.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=self.page.get_upload_url(f.name, 600),
                    )
                )
            self.file_picker.upload(uf)
