def getlocationid(postal_code):
	postcode_str = str(postal_code)
	list_postcode = [i for i in postcode_str]
	first2digits = list_postcode[0] + list_postcode[1]


	list1 = [
	["01","02","03","04","05"],
	["07","08"],
	["14","15","16"],
	["09","10"],
	["11","12","13"], 
	["17"] ,["18","19"],
	["20","21"],
	["22","23"],
	["24","25","26","27"],
	["28","29","30"],
	["31","32","33"],
	["34","35","36","37"],
	["38","39","40","41"],
	["42","43","44","45"],
	["46","47","48"],
	["49","50","81"],
	["51","52"],
	["53","54","55","82"],
	["56","57"],
	["58","59"],
	["60","61","62","63","64"],
	["65","66","67","68"],
	["69","70","71"],
	["72","73"],
	["77","78"],
	["75","76"],
	["79","80"]
	]

	locationId_to_place = {
		1:"Raffles Place, Cecil, Marina, People's Park",
		2:"Anson, Tanjong Pagar",
		3:"Queenstown, Tiong Bahru",
		4:"Telok Blangah, Harbourfront",
		5:"Pasir Panjang, Hong Leong Garden, Clementi New Town",
		6:"High Street, Beach Road (part)",
		7:"Middle Road, Golden Mile",
		8:"Little India",
		9:"Orchard, Cairnhill, River Valley",
		10:"Ardmore, Bukit Timah, Holland Road, Tanglin",
		11:"Watten Estate, Novena, Thomson",
		12:"Balestier, Toa Payoh, Serangoon",
		13:"Macpherson, Braddell",
		14:"Geylang, Eunos",
		15:"Katong, Joo Chiat, Amber Road",
		16:"Bedok, Upper East Coast, Eastwood, Kew Drive",
		17:"Loyang, Changi",
		18:"Simei, Tampines, Pasir Ris",
		19:"Serangoon Garden, Hougang, Ponggol",
		20:"Bishan, Ang Mo Kio",
		21:"Upper Bukit Timah, Clementi Park, Ulu Pandan",
		22:"Jurong",
		23:"Hillview, Dairy Farm, Bukit Panjang, Choa Chu Kang",
		24:"Lim Chu Kang, Tengah",
		25:"Kranji, Woodgrove, Woodlands",
		26:"Upper Thomson, Springleaf",
		27:"Yishun, Sembawang",
		28:"Seletar"
	}

	for i in range(0,len(list1)):
		if(first2digits in list1[i]):
			locationId = (i+1);
			area = locationId_to_place[locationId]
			finallist = [locationId,area]

	print(finallist)
	return finallist






