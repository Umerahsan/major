from flask import Flask, render_template, request,send_from_directory
import run_inference
app = Flask(__name__)
@app.route('/')
@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
      
      f = request.files['file']
      filename=f.filename
      
      destination="/".join(["images",filename])
      f.save(destination)
      sentence=run_inference.run_inference()
      return sentence
      #return render_template('complete.html',image_name=filename)
	
@app.route('/upload/<filename>')
def send_image(filename):
   return send_from_directory("images",filename)   
@app.route('/index')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run()
