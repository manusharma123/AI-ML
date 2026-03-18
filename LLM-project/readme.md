pip3 install matplotlib numpy pylzma ipykernel jupyter notebook

pip3 install torch --index-url https://download.pytorch.org/whl/cu118
python -m ipykernel install --user --name=cuda --display-name "CUDA_GPT"
cude\Scripts\activate
jupyter notebook