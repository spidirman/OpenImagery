from PyQt6.QtWidgets import (QWidget, QMessageBox, QApplication, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QHBoxLayout, QTextEdit, QFormLayout, QComboBox, QSplashScreen)
from PyQt6.QtGui import QPixmap, QIntValidator, QFont, QPainter, QColor, QIcon, QPainterPath
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
import requests
import sys
import time
import threading
import queue



def samplers():
    r = requests.get("https://api.sitius.ir/v1/samplers/")
    return r.json()

def models():
    r = requests.get("https://api.sitius.ir/v1/models/")
    return r.json()

def generate_image(prompt, negative_prompt, model, cfg_scale, steps, sampler, result_queue, log_queue, parent):
    counter = 0
    start_time = time.time()
    
    api_url = "https://api.sitius.ir/"
    data = {
        "model": model,
        "prompt": prompt,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "sampler": sampler,
        "negative_prompt": negative_prompt
    }
    headers = {"auth": "test"}

    with requests.Session() as session:
        
        log_queue.put("Sending request to generate image...")
        
        with session.post(f"{api_url}v1/generate/", json=data, headers=headers) as response:
            job_id = response.json()
            
        log_queue.put(f"Job ID received: {job_id}")

        while counter < start_time+600:
            with session.get(api_url + f"v1/image/{job_id}/") as r:
                if r.status_code == 200:
                    url = r.json()
                    
                    result_queue.put(url)
                    
                    log_queue.put(f"Image generated successfully: {url}")
                    end_time = time.time()
                    
                    time_res = str(round(end_time-start_time,3))
                    
                    log_queue.put(f"generated in {time_res} seconds")
                    log_queue.put(f"INFO : the image may take a little time to display")
                    log_queue.put("-"*20)
                    parent.enable_generate_button()
                    return

                end_time = time.time()
                counter = end_time
                time_res = str(round(end_time-start_time,3))
                
                log_queue.put(f"Waiting for image... {time_res}s elapsed")
                time.sleep(0.2)
                
        result_queue.put(None)
        log_queue.put("Failed to generate image or timeout occurred")
        parent.enable_generate_button()

class MainApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('OpenImagery - AI Image Generator')
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, 'logo.ico')
        else:
            icon_path = 'logo.ico'

        self.setWindowIcon(QIcon(icon_path))


        
        screen_geometry = self.screen().availableGeometry()
        
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        
        self.setGeometry(x, y-100, self.width() , self.height()+200)

        
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        input_layout = QFormLayout()
        right_layout = QVBoxLayout()

        self.prompt_input = QTextEdit(self)
        self.prompt_input.setPlaceholderText('Enter your prompt here...')
        input_layout.addRow('Prompt:', self.prompt_input)

        self.negative_prompt_input = QTextEdit(self)
        self.negative_prompt_input.setPlaceholderText('Enter your negative prompt here...\n(there is one by default)')
        input_layout.addRow('Negative Prompt:', self.negative_prompt_input)

        self.cfg_scale_input = QLineEdit(self)
        self.cfg_scale_input.setPlaceholderText('Enter CFG scale (default: 7)')
        self.cfg_scale_input.setValidator(QIntValidator(1, 20))
        input_layout.addRow('CFG Scale:', self.cfg_scale_input)

        self.steps_input = QLineEdit(self)
        self.steps_input.setPlaceholderText('Enter steps (default: 30)')
        self.steps_input.setValidator(QIntValidator(1, 100))
        input_layout.addRow('Steps:', self.steps_input)

        self.sampler_combo = QComboBox(self)
        self.sampler_combo.addItems(samplers())
        input_layout.addRow('Sampler:', self.sampler_combo)

        self.model_combo = QComboBox(self)
        self.model_combo.addItems(models())
        input_layout.addRow('Model:', self.model_combo)

        self.generate_button = QPushButton('Generate Image', self)
        self.generate_button.clicked.connect(self.generate_image)
        input_layout.addRow(self.generate_button)

        top_layout.addLayout(input_layout)

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(500, 500)
        self.image_label.setStyleSheet("border: 2px solid #3b3b3b; border-radius: 15px;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.image_label)

        top_layout.addLayout(right_layout)

        self.log_display = QTextEdit(self)
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText('Logs will be shown here...')



        
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.log_display)

        self.log_display.textChanged.connect(self.on_text_changed)

        self.setLayout(main_layout)
        self.show()

    @pyqtSlot()
    def on_text_changed(self):
        self.log_display.verticalScrollBar().setValue(self.log_display.verticalScrollBar().maximum())


    def generate_image(self):
        prompt = self.prompt_input.toPlainText()
        negative_prompt = self.negative_prompt_input.toPlainText()
        cfg_scale = self.cfg_scale_input.text()
        steps = self.steps_input.text()
        sampler = self.sampler_combo.currentText()
        model = self.model_combo.currentText()

        if not prompt:
            QMessageBox.warning(self, 'Input Error', 'Please enter a prompt.')
            return

        if not negative_prompt:
            negative_prompt = "canvas frame, cartoon, 3d, ((disfigured)), ((bad art)), ((deformed)), ((extra limbs)), ((close up)), ((b&w)), weird colors, blurry, (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), ((ugly)), (((bad proportions))), (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), (fused fingers), (too many fingers), (((long neck))), Photoshop, video game, tiling, poorly drawn feet, body out of frame, nsfw"

        if not cfg_scale:
            cfg_scale = "7"

        if not steps:
            steps = "30"

      
        if int(cfg_scale) > 30 :
            QMessageBox.warning(self, 'Input Error', 'CFG scale cannot be higher than 30.')
            return
        if int(steps) > 100 :
            QMessageBox.warning(self, 'Input Error', 'steps cannot be higher than 100.')
            return

        self.disable_generate_button()

        cfg_scale = int(cfg_scale)
        steps = int(steps)

        result_queue = queue.Queue()
        log_queue = queue.Queue()

        def log_updater():
            while True:
                log_message = log_queue.get()
                if log_message is None:
                    break
                self.log_display.append(log_message)

        threading.Thread(target=log_updater, daemon=True).start()

        threading.Thread(target=self.generate_image_threaded, args=(prompt, negative_prompt, model, cfg_scale, steps, sampler, result_queue, log_queue)).start()

    def generate_image_threaded(self, prompt, negative_prompt, model, cfg_scale, steps, sampler, result_queue, log_queue):
        try:
            generate_image(prompt, negative_prompt, model, cfg_scale, steps, sampler, result_queue, log_queue, self)
        except Exception as e:
            log_queue.put(f"Error occurred: {str(e)}")

        log_queue.put(None)

        url = result_queue.get()
        if url:
            self.display_image(url)
        else:
            QMessageBox.warning(self, 'Error', 'Failed to generate image or timeout occurred.')

    def display_image(self, url):
        try:
            image_data = requests.get(url).content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.image_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load image: {str(e)}')

    def disable_generate_button(self):
        self.generate_button.setEnabled(False)

    def enable_generate_button(self):
        self.generate_button.setEnabled(True)


class LoadingScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, 'logo.ico')
        else:
            icon_path = 'logo.ico'
        
        pixmap_logo = QPixmap(icon_path)
        pixmap_text = QPixmap(300, 300)
        pixmap_text.fill(Qt.GlobalColor.transparent)
        
        padding = 20
        border_radius = 20
        
        pixmap_width = pixmap_logo.width() + 2 * padding
        pixmap_height = pixmap_logo.height() + pixmap_text.height() + 3 * padding
        pixmap_height -= 175
        
        combined_pixmap = QPixmap(pixmap_width, pixmap_height)
        combined_pixmap.fill(Qt.GlobalColor.transparent)  # Fill with a transparent background
        
        painter = QPainter(combined_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rounded_rect = QPainterPath()
        rounded_rect.addRoundedRect(0, 0, pixmap_width, pixmap_height, border_radius, border_radius)
        painter.fillPath(rounded_rect, Qt.GlobalColor.black)
        
        painter.drawPixmap(padding, padding, pixmap_logo)
        
        painter.drawPixmap(padding, pixmap_logo.height() + 2 * padding, pixmap_text)
        
        painter.end()

        self.setPixmap(combined_pixmap)
        
        self.showMessage('Copyright (c) 2024 spidirman', 
                         Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom, 
                         Qt.GlobalColor.white)
        
    def drawContents(self, painter):
        super().drawContents(painter)
        painter.setPen(QColor(Qt.GlobalColor.white))
        
        painter.setFont(QFont('Arial', 30, QFont.Weight.Bold))
        rect = self.rect().adjusted(0, 0, 0, -100)  
        painter.drawText(rect,  Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, 'OpenImagery')
        
        painter.setFont(QFont('Arial', 10, QFont.Weight.Normal))
        rect = self.rect().adjusted(0, 0, 0, -80)  
        painter.drawText(rect, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, 'Loading required datas...')



def main():
    app = QApplication(sys.argv)
        splash = LoadingScreen()
    splash.show()

    time.sleep(2)

    main_app = MainApp()
    
    splash.finish(main_app)
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
