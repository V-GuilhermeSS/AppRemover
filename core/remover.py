import os
import subprocess

from core.apps import localizar_arquivos_relacionados


def remover_aplicativo(app_name, senha, caixa_log):
    """Remove o aplicativo e seus arquivos relacionados, com permissões de sudo se necessário."""
    app_path = f"/Applications/{app_name}"

    # Exibe os arquivos removidos durante o processo
    log_remocao = []

    # Verifica e remove o aplicativo da pasta /Applications
    if os.path.exists(app_path):
        subprocess.run(["sudo", "-S", "rm", "-rf", app_path], input=senha, text=True, check=True)
        log_remocao.append(f"Removido: {app_path}")

    # Remove os arquivos relacionados encontrados nas bibliotecas do sistema
    arquivos = localizar_arquivos_relacionados(app_name)
    for arquivo in arquivos:
        try:
            if os.path.isdir(arquivo):
                subprocess.run(["sudo", "-S", "rm", "-rf", arquivo], input=senha, text=True, check=True)
                log_remocao.append(f"Removido: {arquivo}")
            else:
                subprocess.run(["sudo", "-S", "rm", "-f", arquivo], input=senha, text=True, check=True)
                log_remocao.append(f"Removido: {arquivo}")
        except subprocess.CalledProcessError:
            print(f"Erro ao tentar remover o arquivo: {arquivo}")

    # Exibe os arquivos removidos na caixa de log
    caixa_log.setText("\n".join(log_remocao))

    return log_remocao
