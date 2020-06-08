import re

def phone_number_validation(number):
	regex = r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$'
	res = re.search(regex, number)
	if res is None:
		raise ValueError('Phone number is not valid')
	return number

