echo "Installing dependencies using pip"
pip install -r requirements.txt
echo "downloading required modules for natural language processes"
python -m spacy download en_core_web_sm
echo "DONE!"

