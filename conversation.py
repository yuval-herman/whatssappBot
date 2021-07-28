retMsg='\n\nלחזרה לתפריט הראשי, שלח 0'
#if msg['Body']=='0': return hello(msg, context)

def hello(msg, context): #0
	return 1, '''שלום לך! אזה כיף שפנית אלינו. 
*שמי בוטי המענה האוטומטי של התכנית*
אם ברצונך למסור מוצר חשמלי או ריהוט- נא לשלוח 1
אם ברצונך לקבל פריט- נא לשלוח 2
בא לך לשמוע עוד על הפרויקט? נשמח נא לשלוח 3
רוצה שנחזור אליך? נא לשלוח 4'''

def giveOrTake(msg, context): #1
	try: query=int(msg['Body'])
	except ValueError: return 1, 'אנא בחר במספר מהאופציות המוצעות'
	if query==1:
		return 2, 'מצוין!, מה תרצה לתת?'
	if query==2:
		return 3, 'בסדר גמור, מה תרצה לקבל?'
	if query==3:
		return -1, '''תוכנית חיים יחד מבית "גרעין יחד" הנה תוכנית חברתית אשר מטרתה להגדיל את תחושת הערבות והשותפות בין התושבים, להצמיח פעילות ומנהיגות בנוער המתנדב של בית שאן והעמק, תוך עידוד מחזור מוצרי חשמל ורהיטים ובכך גם לסייע לאחר ולשמור על סביבה נקיה וקיימות טובה יותר.
התוכנית פועלת מ-2018 ובכל שבוע מתקיימים סבבים של ההעברות מכשור חשמלי ורהיטים מאנשים שרוצים למסור לאנשים שישמחו לקבל.
*הפרויקט עובד בהתנדבות מלאה וללא עלות*
*אנו מעבירים רק ציוד תקין ב-100% ובמצב ראוי*
*כל אחד מוזמן להשתתף ולהעזר בתוכנית, ככל שנכיר יותר נרוויח יותר*'''
	if query==4:
		context['name']='לא ידוע'
		context['status']='מחכה למענה אנושי'
		return -1, 'אנחנו נחזור אליך בקרוב!'
	else:
		return 1, 'המספר שבחרת אינו מופיע באחת מהאופציות, אנא נסה שנית'
	
def give(msg, context): #2
	if msg['Body']=='0': return hello(msg, context)
	context['item']=msg['Body']
	context['status']='נותן'
	return 4, 'תודה רבה לך כמעט סיימנו!\nבבקשה תכתוב לנו את שמך ותשלח צילום של הפריט'.format(context['item'])+retMsg

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
			return 6, 'מעולה {},  נשמח לתמונה של ה{}, במידה וכרגע אין לך תמונה נא להקיש 1'\
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

def give_image(msg, context): #6
	if msg['Body']=='0': return hello(msg, context)
	finRep='תודה רבה אנו שואלים את מי שביקש {}, במידה והוא ירצה, ניצור קשר.\nבמידה והרהיט כבר לא רלוונטי, בבקשה תעדכן אותנו!'.format(context['item'])+retMsg
	if msg['NumMedia']=='0': #there are no media files
		if msg['Body']=='1':
			return -1, finRep
		else:
			return 6, 'אנחנו צריכים שתשלח לנו תמונה של ה{}, אם אתה לא יכול לשלוח לנו תמונה כרגע שלח: 1'.fomart(context['item'])
	else: #an image was sent
		context['images']=[msg['MediaUrl0']]
		return -1, finRep

