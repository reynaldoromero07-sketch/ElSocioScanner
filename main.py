import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import obd

class ScannerInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        # Título principal de la aplicación
        self.add_widget(Label(text="El Socio - Diagnóstico Automotriz", font_size='24sp', size_hint_y=0.2))
        
        # Etiqueta para mostrar los datos en tiempo real (RPM, Velocidad, etc.)
        self.data_label = Label(text="Estado: Desconectado\nRPM: --\nVelocidad: --", font_size='18sp')
        self.add_widget(self.data_label)
        
        # Botón para iniciar el escaneo físico o simulación
        self.scan_btn = Button(text="Conectar OBD-II", size_hint_y=0.2, background_color=(0, 0.7, 0.3, 1))
        self.scan_btn.bind(on_press=self.conectar_vehiculo)
        self.add_widget(self.scan_btn)

    def conectar_vehiculo(self, instance):
        self.data_label.text = "Buscando interfaz OBD-II..."
        # Aquí irá la lógica de conexión serial/Bluetooth con el adaptador del carro
        try:
            # Conexión base (en desarrollo se puede usar obd.OBDStatus.CAR_CONNECTED para pruebas)
            connection = obd.OBD() 
            self.data_label.text = "Conectado al Vehículo\nLeyendo datos en tiempo real..."
        except Exception as e:
            self.data_label.text = "Error: No se encontró el adaptador ELM327"

class ElSocioScannerApp(App):
    def build(self):
        return ScannerInterface()

if __name__ == "__main__":
    ElSocioScannerApp().run()
