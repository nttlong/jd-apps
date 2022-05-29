from flask import Flask  #importing flask elements to make everything work
from flask import render_template
from flask import send_from_directory
import config
import quicky.logs

logger = quicky.logs.get_logger(__name__,__file__)

app = Flask(
    __name__,
    static_folder= config.get_full_static_dir(),
    static_url_path=config.static_url,
    template_folder= config.get_full_template_dir()



)



# @app.route('/<path:path>')
# def send_report(path):
#     return send_from_directory(r'C:\code\python\dj\jd-apps\app_manager\static', path)

@app.route('/')
@app.route('/index')
def index():
    name = 'Rosalia'
    return render_template('index.html', title='Welcome', username=name)
if __name__ == '__main__':
  app.run(
      debug=config.debug,
      host= config.host,
      port=config.port
  )
  logger.info("------------------------------------------------------")
  logger.info("web start with:")
  logger.info(dict(debug=config.debug,host=config.host,port=config.port))
  logger.info("------------------------------------------------------")


