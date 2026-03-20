- python3 -m venv pytorch_env
- source pytorch_env/bin/activate
- Without NVIDIA video card
    -   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

- With NVIDIA video card
    -   pip3 install torch torchvision torchaudio

- check installation

        import torch

        x = torch.rand(5, 3)
        print(x)

        print(f"Versione PyTorch: {torch.__version__}")
        print(f"CUDA disponibile: {torch.cuda.is_available()}")

        if torch.cuda.is_available():
            print(f"GPU rilevata: {torch.cuda.get_device_name(0)}")