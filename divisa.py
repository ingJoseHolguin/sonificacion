import yfinance as yf
import pandas as pd
import numpy as np

def get_currency_data(base_currency, target_currency, start_date, end_date):
    """
    Obtiene datos históricos de una divisa usando yfinance y los reduce a 10 valores representativos.
    
    Parámetros:
    base_currency (str): Moneda base (ejemplo: 'USD')
    target_currency (str): Moneda objetivo (ejemplo: 'EUR')
    start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'
    end_date (str): Fecha de fin en formato 'YYYY-MM-DD'
    
    Retorna:
    list: Lista de 10 valores representativos de cierre de la divisa
    """
    try:
        ticker = f"{base_currency}{target_currency}=X"
        data = yf.download(ticker, start=start_date, end=end_date)
        
        # Verificar si hay datos
        if data.empty:
            return None
        
        # Extraer los valores de cierre
        close_values = data['Close'].values.flatten()
        
        # Si hay menos de 10 valores, devolverlos todos
        if len(close_values) <= 10:
            return close_values.tolist()
        
        # Reducir los datos a 10 valores representativos
        # Usamos un enfoque de subsampling estratégico para capturar la variación
        
        # Método 1: Seleccionar puntos estratégicos (mínimo, máximo y equidistantes)
        min_idx = np.argmin(close_values)
        max_idx = np.argmax(close_values)
        
        # Asegurarse de que tomamos al menos estos puntos importantes
        essential_indices = sorted(list(set([0, min_idx, max_idx, len(close_values)-1])))
        
        # Calcular cuántos puntos adicionales necesitamos
        remaining_points = 10 - len(essential_indices)
        
        # Si necesitamos más puntos, seleccionar equidistantes
        if remaining_points > 0:
            # Dividir el rango completo en segmentos
            step = max(1, len(close_values) // (remaining_points + 1))
            additional_indices = [i for i in range(step, len(close_values), step)][:remaining_points]
            
            # Combinar todos los índices y ordenarlos
            all_indices = sorted(list(set(essential_indices + additional_indices)))[:10]
        else:
            # Si ya tenemos suficientes puntos esenciales, usarlos (primeros 10)
            all_indices = essential_indices[:10]
        
        # Obtener los valores para estos índices
        representative_values = [close_values[i] for i in all_indices]
        
        return representative_values
        
    except Exception as e:
        print(f"❌ Error al obtener los datos de divisas: {e}")
        return None

def get_stock_data(ticker, start_date, end_date):
    """
    Obtiene datos históricos de acciones usando yfinance y los reduce a 10 valores representativos.
    
    Parámetros:
    ticker (str): Símbolo de la acción (ejemplo: 'AAPL')
    start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'
    end_date (str): Fecha de fin en formato 'YYYY-MM-DD'
    
    Retorna:
    list: Lista de 10 valores representativos de cierre de la acción
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        
        # Verificar si hay datos
        if data.empty:
            return None
        
        # Extraer los valores de cierre
        close_values = data['Close'].values.flatten()
        
        # Si hay menos de 10 valores, devolverlos todos
        if len(close_values) <= 10:
            return close_values.tolist()
        
        # Reducir los datos a 10 valores representativos usando el mismo método
        min_idx = np.argmin(close_values)
        max_idx = np.argmax(close_values)
        
        # Asegurarse de que tomamos al menos estos puntos importantes
        essential_indices = sorted(list(set([0, min_idx, max_idx, len(close_values)-1])))
        
        # Calcular cuántos puntos adicionales necesitamos
        remaining_points = 10 - len(essential_indices)
        
        # Si necesitamos más puntos, seleccionar equidistantes
        if remaining_points > 0:
            # Dividir el rango completo en segmentos
            step = max(1, len(close_values) // (remaining_points + 1))
            additional_indices = [i for i in range(step, len(close_values), step)][:remaining_points]
            
            # Combinar todos los índices y ordenarlos
            all_indices = sorted(list(set(essential_indices + additional_indices)))[:10]
        else:
            # Si ya tenemos suficientes puntos esenciales, usarlos (primeros 10)
            all_indices = essential_indices[:10]
        
        # Obtener los valores para estos índices
        representative_values = [close_values[i] for i in all_indices]
        
        return representative_values
        
    except Exception as e:
        print(f"❌ Error al obtener los datos de acciones: {e}")
        return None