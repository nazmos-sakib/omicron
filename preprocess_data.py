def user_data_process(message):
	
	#print(type(message['age']))
	#
	#print(x)
	x = {}
	
	for key in message.keys():
		x[key] = message[key]

	message = x

	'''
	print(x)

	message = pd.DataFrame.from_dict(message,orient='index')
	print(message)

	print(message[0]['age'])

	'''
	#01 age
	message['age'] = int(message['age'])
	#print(message)

	
	#02 gender
	if(message['gender']=='male'):
		message['gender'] = 1
	else:
		message['gender'] = 2
	
	
	#03 Smoking
	if(message['smoking']=='no'):
		message['smoking'] = 0
	elif(message['smoking']=='ex'):
		message['smoking'] = 1
	else:
		message['smoking'] = 2

	#04 HTN
	if(message['HTN']=='no'):
		message['HTN'] = 0
	else:
		message['HTN'] = 1

	#05 DPL
	if(message['DPL']=='no'):
		message['DPL'] = 0
	else:
		message['DPL'] = 1

	#06 DM
	if(message['DM']=='no'):
		message['DM'] = 0
	else:
		message['DM'] = 1

	#07 physical_exercise
	if(message['physical_exercise']=='no'):
		message['physical_exercise'] = 0
	else:
		message['physical_exercise'] = 1


	#08 family_history
	if(message['family_history']=='no'):
		message['family_history'] = 0
	else:
		message['family_history'] = 1

	#09 drug_history
	if(message['drug_history']=='no'):
		message['drug_history'] = 0
	else:
		message['drug_history'] = 1

	#10 psychological_stress
	if(message['psychological_stress']=='no'):
		message['psychological_stress'] = 0
	else:
		message['psychological_stress'] = 1

	#11 chest_pain
	if(message['chest_pain']=='no'):
		message['chest_pain'] = 0
	else:
		message['chest_pain'] = 1

	#12 dyspnea
	if(message['dyspnea']=='no'):
		message['dyspnea'] = 0
	else:
		message['dyspnea'] = 1

	#13 palpitation
	if(message['palpitation']=='no'):
		message['palpitation'] = 0
	else:
		message['palpitation'] = 1

	#14 ECG
	if(message['ECG']=='normal'):
		message['ECG'] = 0
	else:
		message['ECG'] = 1
	
	#print(message)

	return message