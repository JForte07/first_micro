from flask import Flask



app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
 prefix_google = """
 <!-- Google tag (gtag.js) -->
<script async
src="https://www.googletagmanager.com/gtag/js?id=G-XFPGT0NR9L"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', ' G-XFPGT0NR9L');
</script>
 """
 return prefix_google + "Hello World"

#add logger 
@app.route('/logger', methods=["GET"])
def logger():
    #print('hi')
    app.logger.info('testing info log in the console')
    script = """
    <script> console.log("Hello, if you see me it means is working")</script>"""
    print('Hello, if you see me it means is working')
    return "hello word" + script