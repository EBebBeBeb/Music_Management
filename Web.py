from PIL import Image
import requests
from io import BytesIO

#def Search_img(title,artist):
def Get_img(url):
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	img.show()
	img.save("test.jpg")
	return "test.jpg"
	#https://images-na.ssl-images-amazon.com/images/I/712TZuEYzQL._AC_SX355_.jpg