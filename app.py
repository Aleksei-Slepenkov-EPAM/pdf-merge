import subprocess
import sys

subprocess.run([sys.executable, "-m", "pip", "install", "flask"])


from flask import Flask, render_template, request, send_file
from datetime import datetime
app = Flask(__name__)

@app.route('/', methods=['POST'])
def process():
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"output_{current_datetime}.png"

    pdf1 = request.files['pdf1']
    pdf2 = request.files['pdf2']
    pdf1.save('temp1.pdf')
    pdf2.save('temp2.pdf')

    subprocess.run('convert temp1.pdf -background white -flatten temp1.png', shell=True)
    subprocess.run('convert temp2.pdf -background none -flatten temp2.png', shell=True)

    subprocess.run('rm temp1.pdf temp2.pdf', shell=True)
    subprocess.run(f"composite -gravity east temp2.png temp1.png {output_filename}", shell=True)
    subprocess.run('rm temp1.png temp2.png', shell=True)

    return send_file(output_filename, as_attachment=True)


@app.route("/")
def index():
    # Define the output file name with datetime
    return '''
    <html>
      <head>
        <title>PDF to PNG Converter</title>
        <style>
          body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f1f1f1;
          }

          form {
            width: 300px;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
          }

          h1 {
            text-align: center;
            color: #333;
          }

          input[type="file"] {
            margin-bottom: 10px;
          }

          button[type="submit"] {
            background-color: #4CAF50;
            color: #fff;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
          }

          button[type="submit"]:hover {
            background-color: #45a049;
          }
        </style>
      </head>
      <body>
        <form action="/" method="POST" enctype="multipart/form-data">
          <h1>PDF to PNG Converter</h1>
          <input type="file" name="pdf1"><br>
          <input type="file" name="pdf2"><br>
          <button type="submit">Convert</button>
        </form>
      </body>
    </html>
    '''


subprocess.run('sudo apt-get update', shell=True)
subprocess.run('sudo apt-get install -y imagemagick', shell=True)
subprocess.run('echo "" | sudo tee /etc/ImageMagick-*/policy.xml >/dev/null', shell=True)

app.run()