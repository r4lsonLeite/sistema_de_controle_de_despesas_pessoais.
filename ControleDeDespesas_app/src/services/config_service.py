import json
import os

def carregar_configuracoes(caminho="config/settings.json"):
    """Carrega as configurações do arquivo JSON ou retorna valores padrão."""
    try:
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("Aviso: settings.json não encontrado. Usando padrões.")
            return {
                "alerta_alto_valor": 500.0,
                "meta_economia_percentual": 10.0
            }
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")
        return {}