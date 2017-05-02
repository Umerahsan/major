from flask import Flask, render_template, request,send_from_directory
application = Flask(__name__)
import run_inference
@application.route('/')
@application.route('/upload')
def upload_file():
   return render_template('upload.html')

@application.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
      
      f = request.files['file']
      filename=f.filename
      
      destination="/".join(["images",filename])
      f.save(destination)
      sentence=run_inference.run_inference(filename)
      #return sentence
      return render_template('complete.html',image_name=filename,text=sentence)
	
@application.route('/upload/<filename>')
def send_image(filename):
   return send_from_directory("images",filename)   
@application.route('/index')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    application.run(host='0.0.0.0')
