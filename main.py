import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import obd
from obd import commands

class ScannerInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        # Título principal
        self.add_widget(Label(text="El Socio - Escáner de Diagnóstico IA", font_size='24sp', size_hint_y=0.1))
        
        # Usamos un ScrollView para que quepa la lista gigante de datos en la pantalla del teléfono
        self.scroll = ScrollView(size_hint_y=0.6)
        self.data_label = Label(
            text="Sistema Listo.\nPresione 'Diagnóstico Completo con IA' para iniciar el escaneo total.", 
            font_size='16sp',
            halign='center',
            valign='top',
            size_hint_y=None
        )
        self.data_label.bind(texture_size=self.data_label.setter('size'))
        self.scroll.add_widget(self.data_label)
        self.add_widget(self.scroll)
        
        # Botón 1: Escaneo Absoluto e Integración IA
        self.scan_btn = Button(text="Diagnóstico Completo con IA", size_hint_y=0.15, background_color=(0, 0.5, 0.9, 1))
        self.scan_btn.bind(on_press=self.diagnostico_total_ia)
        self.add_widget(self.scan_btn)

        # Botón 2: Reset de la Computadora (Borrado de fallas)
        self.reset_btn = Button(text="Resetear Computadora (Borrar DTC)", size_hint_y=0.15, background_color=(0.9, 0.2, 0.2, 1))
        self.reset_btn.bind(on_press=self.reset_computadora)
        self.add_widget(self.reset_btn)

    def diagnostico_total_ia(self, instance):
        self.data_label.text = "Iniciando escaneo absoluto del vehículo...\nInterrogando todos los sensores de la ECU..."
        
        try:
            connection = obd.OBD()
            
            if connection.status() == obd.OBDStatus.CAR_CONNECTED:
                # 1. ESCANEO ABSOLUTO DE SENSORES DISPONIBLES
                datos_vehiculo = {}
                # Recorremos todos los comandos que soporta el carro de forma automática
                for cmd in connection.supported_commands:
                    if cmd.mode == 1: # Modo 1 son los datos en tiempo real (todos los sensores)
                        response = connection.query(cmd)
                        if not response.is_null():
                            datos_vehiculo[cmd.name] = response.value

                # 2. LECTURA COMPLETA DE FALLAS (Códigos DTC - Modo 03)
                response_dtc = connection.query(commands.GET_DTC)
                fallas = response_dtc.value if not response_dtc.is_null() else []
                
                # Estructuramos el reporte masivo para enviarlo a la API de la IA
                reporte_crudo = {
                    "sensores": datos_vehiculo,
                    "codigos_falla": fallas
                }
                
                # Aquí simulamos el envío del reporte_crudo a la IA
                # La IA analizará los sensores fallando + los DTC y devolverá la solución exacta
                self.data_label.text = (
                    f"¡Escaneo Completo Exitoso!\n\n"
                    f"[DATOS ENVIADOS A LA IA]:\n"
                    f"- Códigos de Falla Detectados: {fallas}\n"
                    f"- Total Sensores Monitoreados: {len(datos_vehiculo)}\n\n"
                    f"[PROCESANDO DIAGNÓSTICO IA...]\n"
                    f"Aquí la IA desplegará la causa raíz del problema, "
                    f"los componentes a revisar en el taller y los pasos detallados para la solución."
                )
            else:
                self.data_label.text = "Error: El adaptador está conectado, pero el vehículo no responde (¿Switch apagado?)."
        except Exception as e:
            self.data_label.text = "Error Crítico: No hay comunicación con el hardware OBD-II."

    def reset_computadora(self, instance):
        self.data_label.text = "Enviando comando de reinicio a la ECU..."
        
        try:
            connection = obd.OBD()
            if connection.status() == obd.OBDStatus.CAR_CONNECTED:
                # MODO 04: Comando oficial OBD-II para borrar códigos de falla y resetear valores
                response_reset = connection.query(commands.CLEAR_DTC)
                
                if response_reset.status == "OK" or not response_reset.is_null():
                    self.data_label.text = (
                        "¡RESET EXITOSO!\n\n"
                        "Se han borrado todos los códigos de falla (DTC) de la memoria.\n"
                        "La luz de 'Check Engine' en el tablero debería apagarse.\n"
                        "Nota: Se recomienda apagar y encender el carro."
                    )
                else:
                    self.data_label.text = "La computadora rechazó el comando de reset. Verifique el estado del motor."
            else:
                self.data_label.text = "Error: Conecte el escáner para poder ejecutar el reset."
        except Exception as e:
            self.data_label.text = "Error al intentar borrar los códigos de falla de la ECU."

class ElSocioScannerApp(App):
    def build(self):
        return ScannerInterface()

if __name__ == "__main__":
    ElSocioScannerApp().run()
