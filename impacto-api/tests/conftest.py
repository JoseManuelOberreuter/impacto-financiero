import os

# Las pruebas usan los JSON de respaldo de app/datos_ejemplo, nunca Supabase.
os.environ["FOTOS_DESDE"] = "archivos"
os.environ["REVISAR_FOTOS_MINUTOS"] = "0"
