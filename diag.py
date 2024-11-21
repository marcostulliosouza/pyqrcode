import ctypes

try:
    ctypes.CDLL("/opt/homebrew/lib/libzbar.dylib")
    print("ZBar carregado com sucesso!")
except OSError as e:
    print(f"Erro ao carregar ZBar: {e}")
