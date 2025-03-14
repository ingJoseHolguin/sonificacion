import numpy as np
import datetime
import os
import platform
from sonificacion import map_to_notes, play_notes
from divisa import get_currency_data, get_stock_data

def clear_screen():
    """Limpia la pantalla de la terminal según el sistema operativo."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')  # Para MacOS y Linux

def validate_date(date_text):
    """Valida que la fecha tenga el formato correcto y sea una fecha válida."""
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main():
    # Limpiar pantalla al iniciar
    clear_screen()
    
    while True:
        print("\n===== Bienvenido al Sonificador de Datos Financieros =====")
        print("Este programa convierte datos de divisas o acciones en sonidos,")
        print("permitiéndote percibir variaciones financieras de una forma única.")
        print("¿Qué tipo de datos deseas sonificar?")
        print("1. Divisas (ejemplo: USD a EUR)")
        print("2. Acciones de empresas (ejemplo: AAPL, TSLA)")
        print("3. Salir")
        
        option = input("Selecciona una opción: ")
        
        if option == '3':
            print("¡Gracias por usar el Sonificador de Datos Financieros!")
            break
            
        # Obtener rango de fechas
        while True:
            print("\nPor favor, ingresa un rango de fechas para analizar (formato: YYYY-MM-DD)")
            start_date = input("Fecha de inicio: ")
            end_date = input("Fecha de fin: ")
            
            if not validate_date(start_date) or not validate_date(end_date):
                print("❌ Formato de fecha incorrecto. Usa YYYY-MM-DD.")
                continue
                
            # Verificar que la fecha de inicio sea anterior a la de fin
            if start_date > end_date:
                print("❌ La fecha de inicio debe ser anterior a la fecha de fin.")
                continue
                
            break
        
        data = None
        
        if option == '1':  # Divisas
            base_currency = input("Ingresa la moneda base (ejemplo: USD): ")
            target_currency = input("Ingresa la moneda objetivo (ejemplo: EUR): ")
            
            data = get_currency_data(base_currency, target_currency, start_date, end_date)
            
        elif option == '2':  # Acciones
            ticker = input("Ingresa el símbolo de la acción (ejemplo: AAPL): ")
            
            data = get_stock_data(ticker, start_date, end_date)
        
        if data is None or len(data) == 0:
            print("⚠️ No se encontraron datos en el rango seleccionado. Intenta nuevamente.")
            input("\nPresiona Enter para continuar...")
            clear_screen()
            continue
            
        # Asegurarse de que los datos sean una lista plana de números
        try:
            # Convertir a array numpy para asegurar que es un array plano
            data = np.array(data).flatten().tolist()
            
            # Configurar la sonificación
            print("\nConfigura la sonificación:")
            instruments = ['piano', 'trumpet', 'both']
            for i, inst in enumerate(instruments, 1):
                print(f"{i}. {inst.capitalize()}")
                
            while True:
                try:
                    inst_option = int(input("Selecciona un instrumento (1-3): "))
                    if 1 <= inst_option <= 3:
                        instrument = instruments[inst_option-1]
                        break
                    else:
                        print("❌ Opción inválida.")
                except ValueError:
                    print("❌ Ingresa un número válido.")
                    
            while True:
                try:
                    duration = float(input("Duración de cada nota (0.1-2.0 segundos): "))
                    if 0.1 <= duration <= 2.0:
                        break
                    else:
                        print("❌ La duración debe estar entre 0.1 y 2.0 segundos.")
                except ValueError:
                    print("❌ Ingresa un número válido.")
            
            # Procesar datos y generar sonificación
            print("\n🎵 Generando sonificación...\n")
            notes = map_to_notes(data)
            
            if not notes or len(notes) == 0:
                print("⚠️ No se pudieron generar notas para los datos seleccionados.")
                input("\nPresiona Enter para continuar...")
                clear_screen()
                continue
                
            print(f"Datos mapeados a {len(notes)} notas: {', '.join(notes[:10])}{'...' if len(notes) > 10 else ''}")
            print(f"Rango de valores: {min(data):.2f} - {max(data):.2f}")
            print(f"Instrumento: {instrument.capitalize()}")
            print(f"Duración de nota: {duration} segundos")
            
            input("\nPresiona Enter para escuchar la sonificación...")
            play_notes(notes, instrument=instrument, duration=duration)
            print("\n✅ Sonificación completada.")
            
            # Esperar a que el usuario confirme para volver al menú principal
            input("\nPresiona Enter para volver al menú principal...")
            clear_screen()  # Limpiar pantalla antes de mostrar de nuevo el menú
            
        except Exception as e:
            print(f"❌ Error al procesar los datos: {e}")
            input("\nPresiona Enter para continuar...")
            clear_screen()

if __name__ == "__main__":
    main()