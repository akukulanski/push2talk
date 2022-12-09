import pystray                                                                                
from PIL import Image
from .resources import icons

icon = pystray.Icon('test name')
image = Image.open('/home/kuku/STORAGE/current/repositories/push-to-talk/resources/muted.png')
icon = pystray.Icon(name ="SPAM!", icon =image, title ="MOBASuite", menu =None)               
icon.run()                                                                                    

# https://stackoverflow.com/questions/58001335/create-a-dynamic-tray-icon-with-python
