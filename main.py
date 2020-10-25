import re, json, requests

# https://stackoverflow.com/questions/33338713/filtering-out-all-non-kanji-characters-in-a-text-with-python-3
# hiragana_full = r'[ぁ-ゟ]'
# katakana_full = r'[゠-ヿ]'
re_kanji = r'[㐀-䶵一-鿋豈-頻]'
# radicals = r'[⺀-⿕]'
# katakana_half_width = r'[｟-ﾟ]'
# alphanum_full = r'[！-～]'
# symbols_punct = r'[、-〿]'
# misc_symbols = r'[ㇰ-ㇿ㈠-㉃㊀-㋾㌀-㍿]'
# ascii_char = r'[ -~]'

def get_jwt_from_duolingo():
	num_tries = 3

	for i in range(1, num_tries+1):
		print("Tries: {}/{}".format(i, num_tries))
		r = requests.post("https://www.duolingo.com/login", data={"login": input("login: "), "password": input("password: ")})

		if("user_id" in r.json()):
			jwt_token = r.headers['jwt']

			try:
				with open("./duolingo-jwt", "w") as file:
					file.write(jwt_token)

				print("Duolingo jwt token saved locally: ./duolingo-jwt\n")
			except:
				print("Can't save jwt token locally: ./duolingo-jwt\n")

			return jwt_token
		else:
			print("Login failed\n")

	return False

def get_words(from_duolingo=True):
	words = []

	if(from_duolingo):
		# Try to load jwt token from local file
		try:
			with open("./duolingo-jwt", "r") as file:
				jwt_token = file.read()
		except:
			print("Can't load jwt token from local file: ./duolingo-jwt\n")
			jwt_token = get_jwt_from_duolingo()

		if(jwt_token != False):
			r = requests.get('https://www.duolingo.com/vocabulary/overview', cookies={"jwt_token": jwt_token})
			
			try:
				data = r.json()
				words = list(map(lambda d: d["word_string"], data["vocab_overview"]))

				try:
					with open("./words.json", "w") as file:
						file.write(json.dumps(words))
					print("Words saved locally: ./words.json\n")
				except:
					print("Can't save words locally\n")
			except:
				print("Can't get the json from Duolingo response :(\nTry deleting ./duolingo-jwt\n")
		else:
			print("Can't get the jwt_token	")
	else:
		# When there is no internet, bruh
		try:
			with open("./words.json", "r") as file:
				words = json.loads(file.read())
			print("Words loaded from local file: ./words.json")
		except:
			print("Can't load words from local file: ./words.json")

	return words

def get_unique_kanjis_from_words(words):
	kanjis = []

	for word in words:
		kanjis += list(filter(lambda k: k not in kanjis, re.findall(re_kanji, word)))

	return kanjis

words = get_words(True)
kanjis = get_unique_kanjis_from_words(words)

print(kanjis)