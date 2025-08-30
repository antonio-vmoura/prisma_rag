import torch
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Defina o número de GPU que deseja usar (0, 1, 2, etc.)


def check_gpu_availability():
    # Verificar se o PyTorch foi compilado com suporte a CUDA
    if not torch.cuda.is_available():
        print("CUDA não está disponível. Certifique-se de ter instalado os drivers corretos e que sua GPU é compatível.")
        return False
    
    # Verificar a disponibilidade de GPU
    device = torch.cuda.current_device()
    print(f"GPU encontrada: {torch.cuda.get_device_name(device)}")
    
    # Verificar a versão do CUDA
    print(f"Versão do CUDA: {torch.version.cuda}")
    
    # Verificar a versão do PyTorch
    print(f"Versão do PyTorch: {torch.__version__}")
    
    return True

if __name__ == "__main__":
    if check_gpu_availability():
        print("Todas as verificações passaram. Você pode usar a GPU com o PyTorch.")
    else:
        print("Alguma verificação falhou. Verifique as mensagens de erro acima para resolver o problema.")
