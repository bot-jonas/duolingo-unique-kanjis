# duolingo-unique-kanjis
A python program to get unique kanjis that I learned in Duolingo japanese course

### get_jwt_from_duolingo

Try to get a jwt token from Duolingo using inputs for login and password, and tries to save it in a file called `duolingo-jwt`

### get_words(from_duolingo=True)
If `from_duolingo == True`

Try to get all known words from Duolingo account (at least mine), and tries to save it in a file called `words.json`

If `from_duolingo == False`

Try to load words from the file called `words.json`

### get_unique_kanjis_from_words(words)
Get all unique kanjis from `words`
