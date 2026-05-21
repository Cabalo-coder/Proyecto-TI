# Importa la función create_client para crear la conexión con Supabase
from supabase import create_client

# Permite acceder a variables de entorno del sistema
import os

# Importa load_dotenv para cargar variables desde el archivo .env
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env
load_dotenv()

# Obtiene la URL del proyecto de Supabase desde las variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")

# Obtiene la clave de acceso de Supabase desde las variables de entorno
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Crea la conexión con Supabase utilizando la URL y la clave del proyecto
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)