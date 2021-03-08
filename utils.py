import re


def replace_property(stylesheet, key, value):
	"""Replaces a property value in the string of a stylesheet"""
	# because I could not get PyQt's unpolish() and polish() to work
	key_index = stylesheet.rfind(key)
	if key_index == -1:
		return stylesheet + "{}:{};".format(key, value)
	else:
		key_index += len(key) + 1
		semicolon = stylesheet.find(";", key_index)
		return stylesheet[:key_index] + value + stylesheet[semicolon:]


def highlight_urls(text):
	"""Used to turn some types of urls in task descriptions into hyperlinks"""
	hyper_words = []
	for word in text.split():
		if re.search("\.(com|net|org|io|de)", word):
			if "http://" in word or "https://" in word:
				hyper_words.append("""<a href="{url}">{url}</a>""".format(url=word))
			else:
				hyper_words.append("""<a href="https://{url}">{url}</a>""".format(url=word))
		else:
			hyper_words.append(word)
	return " ".join(hyper_words)


if __name__ == '__main__':
	test_str = "graphics: ancient;\nstyle: medieval;\ncontrols: awkward;"
	test_str2 = "graphics: ancient;\nstyle: medieval;\n"

	test_str = replace_property(test_str, "style", "modern")
	test_str2 = replace_property(test_str2, "controls", "smooth")

	assert ("style:modern;" in test_str)
	assert ("controls:smooth;" in test_str2)
