#curl -X GET -G  'https://api.foursquare.com/v2/venues/explore'     -d client_id="J4X3WOSHBWAVP3MDTCX4UVSFHQZKL1D0TGUZGA4WIJY2OY2J"     -d client_secret="ECYXS2O3ABQ0TWZXT0PM1WQKBYORKPF4NDYTL3DX01BHSX1H"  -d v="20180323"  -d ll="40.7243,-74.0018" -d query="coffee" -d limit=1\

# https://maps.googleapis.com/maps/api/geocode/json?address=%22los%20angeles,%20california,%20usa%22&key=AIzaSyBsKJemNsmqcqdaJZi5fXYPPqIMqBg0BMg
import httplib2
from urllib import urlencode
import json
from pprint import pprint as pp
import codecs, sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# foursqare
CLIENT_ID = ""
CLIENT_SECRET = ""
# google maps
GEOLOCATION_KEY = "AIzaSyBsKJemNsmqcqdaJZi5fXYPPqIMqBg0BMg"

def getGeocodeLocation(inputString):
	locationString = inputString.replace(" ", "+")
	url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, GEOLOCATION_KEY))

	h = httplib2.Http()
	response, content = h.request(url, 'GET')
	result = json.loads(content)
	#print 'response header: %s \n\n' % response
	#print 'content: %s' % pp(result)
	longtitude = result["results"][0]["geometry"]["location"]["lng"]
	latitude = result["results"][0]["geometry"]["location"]["lat"]
	return (latitude, longtitude)


# api mashup
# findARestaurant(mealType, location)
# geolocate thelocation
# pass lat, lng to forsquare
# parse responce and return one restaurant
def getARestaurant(location, queryStr):
	url = "https://api.foursquare.com/v2/venues/explore?"
	params = dict(
		client_id=CLIENT_ID,
		client_secret=CLIENT_SECRET,
		v='20180323',
		ll='',
		query='',
		limit=1)
	#url = url + "&".join(params)
	lng, lat = getGeocodeLocation(location)
	params["ll"] = ",".join([str(lng),str(lat)])
	params["query"] = queryStr
	#print (url+urlencode(params))
	h = httplib2.Http()
	response, content = h.request((url+urlencode(params)), 'GET')
	#print 'location: %s' % pp(json.loads(content))
	results = json.loads(content)
	if results['response']['groups'][0]['items'][0]:
		restaurant = results['response']['groups'][0]['items'][0]["venue"]
		venue_id = restaurant["id"]
		restaurant_name = restaurant["name"]
		restaurant_address = " ".join(restaurant["location"]["formattedAddress"])
		
		# get a picture
		url = 'https://api.foursquare.com/v2/venues/%s/photos?' % venue_id 
		params = dict(
			client_id=CLIENT_ID,
			v=20150603,
			client_secret=CLIENT_SECRET)
		h = httplib2.Http()
		#print url+urlencode(params)
		response, content = h.request((url+urlencode(params)), 'GET')
		# grap first image
		#print pp(json.loads(content))
		content = json.loads(content)
		#print content
		if content['response']['photos']['items']:
			pic = content['response']['photos']['items'][0]
			prefix = pic['prefix']
			suffix = pic['suffix']
			imageUrl = prefix + "300x300" + suffix
		else:
			# no image
			imageUrl = "https://pixabay.com/vectors/burger-sandwich-hamburger-31788/"
		# return to dict with name address etc
		restaurantInfo = dict(
			name = restaurant_name,
			address = restaurant_address,
			image = imageUrl)
		print pp(restaurantInfo)
		return restaurantInfo
	else:
		print "No restaurants found for %s" % location
		return "No restaurants Found"
		



if __name__ == "__main__":
	
	#location =  getGeocodeLocation("Tokyo, Japan")
	#getARestaurant(location, "pizza")
	getARestaurant("Tokyo, Japan", "Pizza")
	getARestaurant("Jakarta, Indonesia", "Tacos")
	getARestaurant("Maputo, Mozambique", "Tapas")
	getARestaurant("cairo, egypt", "falafel")
	getARestaurant("new delhi", "spaghetti")
	getARestaurant("geneva, switzerland", "cappuccino")
	getARestaurant("los angeles, california", "sushi")
	getARestaurant("la paz, bolivia", "steak")
	getARestaurant("sydney, australia", "gyros")
	# paella


