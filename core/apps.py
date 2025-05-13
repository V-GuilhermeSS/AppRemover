import os
import glob

def listar_aplicativos():
    """Lista os aplicativos instalados na pasta /Applications."""
    apps = [app for app in os.listdir("/Applications") if app.endswith(".app")]
    return apps

def localizar_arquivos_relacionados(app_name):
    """Localiza arquivos do aplicativo em várias pastas do sistema."""
    app_name = app_name.replace(".app", "")
    caminhos = [
        f"~/Library/Preferences/{app_name}*.plist",
        f"~/Library/Application Support/{app_name}*",
        f"~/Library/Caches/{app_name}*",
        f"~/Library/Logs/{app_name}*"
    ]
    arquivos_encontrados = []
    for caminho in caminhos:
        arquivos_encontrados.extend(glob.glob(os.path.expanduser(caminho)))
    return arquivos_encontrados
