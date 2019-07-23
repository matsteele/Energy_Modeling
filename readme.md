

cd into server
cd server
run
start virtual environment
source venv/bin/activate
pip3 install -r requirements.txt
python main.py
cd into static
webpack --watch
also start Sass styling
sass --watch style/style.scss:style/style.css
