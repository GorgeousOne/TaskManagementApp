import re


def replace_property(stylesheet, key, value):
	"""Replaces a property value in the string of a stylesheet"""
	# because I could not get PyQt's unpolish() and polish() to work
	index = stylesheet.rfind(key)
	if index == -1:
		return stylesheet + "{}: {};".format(key, value)
	else:
		index += len(key) + 1
		semicolon = stylesheet.find(";", index)
		return stylesheet[:index] + value + stylesheet[semicolon:]


def highlight_urls(text):
	"""Used to turn some types of urls in task descriptions into hyperlinks"""
	hyper_words = []
	for word in text.split():
		if re.search("\.[com|net|org|io|de]", word):
			hyper_words.append("""<a href={url}>{url}</>""".format(url=word))
		else:
			hyper_words.append(word)
	return " ".join(hyper_words)


if __name__ == '__main__':
	test_str = "please update this property's value style: medieval; thanks"
	test_str2 = "nothing to replace here, "
	print(replace_property(test_str, "style", "modern"))
	print(replace_property(test_str2, "ill do it", "anyway"))
