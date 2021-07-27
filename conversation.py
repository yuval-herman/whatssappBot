import csv

retMsg='\n\nלחזרה לתפריט הראשי, שלח 0'
#if msg['Body']=='0': return hello(msg, context)

def hello(msg, context): #0
	return 1, 'שלום לך!\nאני בוט שנועד לתאם בין אנשים שרוצים למסור דברים לבין אנשים שרוצים לקבל משהו\nאם אתה רוצה למסור משהו שלח 1\nאם אתה רוצה לקבל משהו שלח 2\nלקבלת עוד מידע על התוכנית שלח 3\nלקבלת מענה אנושי שלח 4'

def giveOrTake(msg, context): #1
	try: query=int(msg['Body'])
	except ValueError: return 1, 'אנא בחר במספר מהאופציות המוצעות'
	if query==1:
		return 2, 'מצוין!, מה תרצה לתת?'
	if query==2:
		return 3, 'בסדר גמור, מה תרצה לקבל?'
	if query==3:
		return 0, '*_כאן יופיע מידע על התוכנית_*'
	if query==4:
		with open('contacts.csv', 'a', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['מחכה למענה אנושי', msg['From']])
		return 0, 'אנחנו נחזור אליך בקרוב!'
	else:
		return 1, 'המספר שבחרת אינו מופיע באחת מהאופציות, אנא נסה שנית'
	
def give(msg, context): #2
	if msg['Body']=='0': return hello(msg, context)
	context['item']=msg['Body']
	context['status']='נותן'
	return 4, 'תודה רבה לך כמעט סיימנו!\nעכשיו תרשום לי, מה שמך המלא וגם אם אפשר תשלח לי תמונה של ה{}'.format(context['item'])+retMsg

def take(msg, context): #3
	if msg['Body']=='0': return hello(msg, context)
	context['item']=msg['Body']
	context['status']='מבקש'
	return 5, 'תודה רבה לך כמעט סיימנו, עכשיו תרשום לי, מה שמך המלא?'+retMsg

def give_name(msg, context): #4
	if msg['Body']=='0': return hello(msg, context)
	finRep='תודה רבה אנו שואלים את מי שביקש {}, במידה והוא ירצה, ניצור קשר.\nבמידה והרהיט כבר לא רלוונטי, בבקשה תעדכן אותנו!'.format(context['item'])+retMsg
	if msg['NumMedia']=='0': #there are no media files
		if 'name' in context:
			hello(msg, context)
		if ' ' not in msg['Body']:
			return 4, 'אני צריך גם את שמך הפרטי וגם שם משפחה...'
		context['name']=msg['Body']
		if 'images' in context:
			return -1, finRep
		else:
			return 4, 'בסדר גמור {},\nאם אתה יכול לשלוח לי גם תמונה של ה{} זה יהיה מצוין, גם אם לא, אנחנו נחזור אליך ברגע שמישהו שצריך {} יצור איתנו קשר'\
					.format(context['name'].split(' ')[0], context['item'], context['item'])
	else: #an image was sent
		context['images']=[msg['MediaUrl0']]
		if 'name' in context:
			return -1, finRep
		else:
			return 4, 'מצויין!, עכשיו רק תרשום לי מה שמך וסיימנו'
	
def take_name(msg, context): #5
	if msg['Body']=='0': return hello(msg, context)
	if ' ' not in msg['Body']: return 5, 'אני צריך גם את שמך הפרטי וגם שם משפחה...'
	context['name']=msg['Body']
	return -1, 'תודה רבה {}!\nנחזור אליך ברגע שימצא מישהו עם {}'.format(context['name'].split(' ')[0], context['item'])+retMsg


