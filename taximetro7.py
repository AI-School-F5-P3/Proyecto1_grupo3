# El programa usa un interfaz amigable haciendo uso de la librería tkinter y mejorando los estilos de la versión 7
import time
import logging
import argparse
import tkinter as tk
from tkinter import messagebox, simpledialog

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("taximetro.log"), 
    logging.StreamHandler()  
])

class Taximetro:
    def __init__(self, contraseña):
        self.tarifa_parado = 0.02
        self.tarifa_movimiento = 0.05
        self.tiempo_total = 0
        self.total_euros = 0
        self.en_movimiento = False
        self.tiempo_ultimo_cambio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.contraseña = contraseña
        self.autenticado = False
        logging.info("Taxímetro iniciado con tarifas por defecto y contraseña establecida.")

    def iniciar_carrera(self, root):
        self.autenticar(root)
        if not self.autenticado:
            return
        
        self.root = root
        self.root.title("Taxímetro Digital")
        self.root.geometry("400x300")
        self.root.configure(bg="black")

        self.estado_label = tk.Label(root, text="Taxi en parado.", font=("Helvetica", 18), fg="white", bg="black")
        self.estado_label.pack(pady=10)

        self.tarifa_parado_label = tk.Label(root, text=f"Tarifa en parado: {self.tarifa_parado:.2f} €/minuto", font=("Helvetica", 14), fg="white", bg="black")
        self.tarifa_parado_label.pack()

        self.tarifa_movimiento_label = tk.Label(root, text=f"Tarifa en movimiento: {self.tarifa_movimiento:.2f} €/minuto", font=("Helvetica", 14), fg="white", bg="black")
        self.tarifa_movimiento_label.pack()

        self.total_label = tk.Label(root, text="Total a cobrar: 0.00 euros", font=("Helvetica", 16), fg="white", bg="black")
        self.total_label.pack(pady=10)

        button_frame = tk.Frame(root, bg="black")
        button_frame.pack(pady=10)

        self.boton_marcha = tk.Button(button_frame, text="Marcha", font=("Helvetica", 14, "bold"), command=self.iniciar_movimiento, width=12, bg="grey", fg="black")
        self.boton_marcha.grid(row=0, column=0, padx=5)

        self.boton_parada = tk.Button(button_frame, text="Parada", font=("Helvetica", 14, "bold"), command=self.detener_movimiento, width=12, bg="white", fg="black")
        self.boton_parada.grid(row=0, column=1, padx=5)

        self.boton_fin = tk.Button(button_frame, text="Fin", font=("Helvetica", 14, "bold"), command=self.finalizar_carrera, width=12, bg="yellow", fg="black")
        self.boton_fin.grid(row=1, column=0, padx=5, pady=5)

        self.boton_configurar = tk.Button(button_frame, text="Configurar tarifas", font=("Helvetica", 14, "bold"), command=self.configurar_tarifas, width=18, bg="white", fg="black")
        self.boton_configurar.grid(row=1, column=1, padx=5, pady=5)

        self.boton_cambiar_contraseña = tk.Button(button_frame, text="Cambiar contraseña", font=("Helvetica", 14, "bold"), command=self.cambiar_contraseña, width=18, bg="white", fg="black")
        self.boton_cambiar_contraseña.grid(row=2, column=0, columnspan=2, pady=5)

    def autenticar(self, root):
        intentos = 3
        while intentos > 0:
            if not self.autenticado:
                contraseña_ingresada = simpledialog.askstring("Autenticación", "Ingresa la contraseña para continuar:", show='*')
                if contraseña_ingresada == self.contraseña:
                    self.autenticado = True
                    logging.info("Contraseña correcta. Acceso concedido.")
                else:
                    messagebox.showerror("Error", "Contraseña incorrecta. Inténtalo de nuevo.")
                    logging.warning("Intento de acceso con contraseña incorrecta.")
                    intentos -= 1
            else:
                break

        if intentos == 0:
            logging.error("Número máximo de intentos alcanzado. Cierre del programa.")
            messagebox.showerror("Error", "Número máximo de intentos alcanzado. Cierre del programa.")
            root.destroy()

    def configurar_tarifas(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para configurar las tarifas.")
            messagebox.showerror("Error", "No se ha autenticado. Debes autenticarte para configurar las tarifas.")
            return

        try:
            nueva_tarifa_parado = float(simpledialog.askstring("Configurar tarifas", "Introduce la nueva tarifa en parado (€/minuto):"))
            nueva_tarifa_movimiento = float(simpledialog.askstring("Configurar tarifas", "Introduce la nueva tarifa en movimiento (€/minuto):"))
            self.tarifa_parado = nueva_tarifa_parado
            self.tarifa_movimiento = nueva_tarifa_movimiento
            logging.info("Tarifas actualizadas a parado: %.2f, movimiento: %.2f", self.tarifa_parado, self.tarifa_movimiento)
            self.tarifa_parado_label.config(text=f"Tarifa en parado: {self.tarifa_parado:.2f} €/minuto")
            self.tarifa_movimiento_label.config(text=f"Tarifa en movimiento: {self.tarifa_movimiento:.2f} €/minuto")
            messagebox.showinfo("Éxito", "Tarifas actualizadas.")
        except ValueError:
            logging.error("Error al introducir tarifas. Valores no numéricos.")
            messagebox.showerror("Error", "Introduce valores numéricos válidos.")

    def cambiar_contraseña(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para cambiar la contraseña.")
            messagebox.showerror("Error", "No se ha autenticado. Debes autenticarte para cambiar la contraseña.")
            return

        nueva_contraseña = simpledialog.askstring("Cambiar contraseña", "Introduce la nueva contraseña:", show='*')
        confirmacion_contraseña = simpledialog.askstring("Cambiar contraseña", "Confirma la nueva contraseña:", show='*')

        if nueva_contraseña == confirmacion_contraseña:
            self.contraseña = nueva_contraseña
            logging.info("Contraseña cambiada exitosamente.")
            messagebox.showinfo("Éxito", "Contraseña cambiada exitosamente.")
        else:
            logging.warning("La nueva contraseña no coincide con la confirmación.")
            messagebox.showerror("Error", "La nueva contraseña no coincide con la confirmación.")
        
    def _cambiar_estado(self, tiempo_actual, en_movimiento):
        tiempo_transcurrido = tiempo_actual - self.tiempo_ultimo_cambio
        if self.en_movimiento:
            self.tiempo_movimiento += tiempo_transcurrido
        else:
            self.tiempo_parado += tiempo_transcurrido

        self.en_movimiento = en_movimiento
        self.tiempo_ultimo_cambio = tiempo_actual
        estado = "movimiento" if en_movimiento else "parado"
        self.estado_label.config(text=f"Taxi en {estado}.")
        logging.info(f"Taxi en {estado}.")

    def iniciar_movimiento(self):
        self._cambiar_estado(time.time(), True)

    def detener_movimiento(self):
        self._cambiar_estado(time.time(), False)

    def finalizar_carrera(self):
        tiempo_actual = time.time()
        self._cambiar_estado(tiempo_actual, self.en_movimiento)
        self.total_euros = (self.tiempo_movimiento * self.tarifa_movimiento) + (self.tiempo_parado * self.tarifa_parado)
        self.total_label.config(text=f"Total a cobrar: {self.total_euros:.2f} euros")
        messagebox.showinfo("Carrera finalizada", f"Total a cobrar: {self.total_euros:.2f} euros")
        self.resetear_valores()

    def resetear_valores(self):
        self.tiempo_total = 0
        self.total_euros = 0
        self.en_movimiento = False
        self.tiempo_ultimo_cambio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0

def parse_args():
    parser = argparse.ArgumentParser(description='Taxímetro digital - Aplicación GUI')
    parser.add_argument('--contraseña', type=str, default='1234', help='Contraseña para configurar tarifas (por defecto: "1234")')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    root = tk.Tk()
    taximetro = Taximetro(contraseña=args.contraseña)
    taximetro.iniciar_carrera(root)
    root.mainloop()
