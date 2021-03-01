import os
from os.path import sep
import re

icons_folder = os.path.dirname(os.path.abspath("main.py")) + sep + "uis" + sep + "res" + sep + "icons" + sep


def replace_property(stylesheet, key, value):
	"""Replaces a property value in the string of a stylesheet"""  # because I could not get PyQt's unpolish() and polish() to work
	index = stylesheet.rfind(key)
	if index == -1:
		return stylesheet + "{}: {};".format(key, value)
	else:
		index += len(key) + 1
		semicolon = stylesheet.find(";", index)
		return stylesheet[:index] + value + stylesheet[semicolon:]


def highlight_urls(text):
	"""Turns a small selection of urls types inside a string into PyQt's hyperlinks for"""
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
