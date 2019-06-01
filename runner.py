import plex

class ParseError(Exception):
	pass

class ParseRun(Exception):
	pass

class MyParser:
	def __init__(self):
		YEET = plex.Any(" \n\t")
		Parentheseis = plex.Str('(',')')
		letter = plex.Range('azAZ')
		digit = plex.Range('09')
		name = letter+plex.Rep(letter|digit)
		bitch = plex.Range('01')
		ban = plex.Rep1(bitch)
		keyword = plex.Str('print','PRINT')
		operator=plex.Str('AND','OR','XOR','=')
		self.st = {}
		self.lexicon = plex.Lexicon([
			(operator,plex.TEXT),
			(ban,'BIT_TOKEN'),
			(keyword,'PRINT'),
			(Parentheseis,plex.TEXT),
			(name,'IDENTIFIER'),
			(YEET,plex.IGNORE)
			])

	def create_scanner(self,fp):
		self.scanner = plex.Scanner(self.lexicon,fp)
		self.la,self.text=self.next_token()

	def next_token(self):
		return self.scanner.read()

	def match(self,token):
		if self.la==token:
			self.la,self.text=self.next_token()
		else:
			raise ParseError("I AM WAITING (")

	def parse(self,fp):
		self.create_scanner(fp)
		self.stmt_list()
		
	def stmt_list(self):
		if self.la=='IDENTIFIER' or self.la=='PRINT':
			self.stmt()
			self.stmt_list()
		elif self.la==None:
			return
		else:
			raise ParseError("I AM WAITING IDENTIFIER or Print")
	def stmt(self):
		if self.la=='IDENTIFIER':
			varname= self.text
			self.match('IDENTIFIER')
			self.match('=')
			e=self.expr()
			self.st[varname]= e
		elif self.la=='PRINT':
			self.match('PRINT')
			e=self.expr()
			print('{:b}'.format(e))
		else:
			raise ParseError("I AM WAITING IDENTIFIER or PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN':	
			freak=self.term()
			while self.la == 'XOR':
				self.match('XOR')
				freak2 = self.term()
				freak ^= freak2
			if self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
					return freak
			else:
					raise ParseError("I AM WAITING XOR")
		else:
			raise ParseError("I AM STILL WAITING ( or IDENTIFIER or BIT or )")
	
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN':	
			freak=self.factor()
			while self.la == 'OR':
				self.match('OR')
				freak2 = self.factor()
				freak |= freak2
			if self.la == 'XOR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
					return freak
			else:
					raise ParseError("I AM WAITING FOR OR ")
		else:
			raise ParseError("I AM STILL WAITING ( or IDENTIFIER or BIT or )")
	def factor(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN':	
			freak=self.atom()
			while self.la == 'AND':
				self.match('AND')
				freak2 = self.atom()
				freak &= freak2
			if self.la == 'XOR' or self.la == 'OR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
					return freak
			else:
					raise ParseError("COME ON GIVE AN AND")
		else:
			raise ParseError("i AM WAITING ( or IDENTIFIER or BIT or )")
	def atom(self):
		if self.la=='(':
			self.match('(')
			e=self.expr()
			self.match(')')
			return e
		elif self.la=='IDENTIFIER':
			varname = self.text
			self.match('IDENTIFIER')
			if varname in self.st:
				return self.st[varname]
			raise ParseRun("I AM LOSING MY TEMPER.. GIVE ME AN IDENTIFIER YOU F....ING MO..N THAT'S BEEN INITIALISED")
		elif self.la == 'BIT_TOKEN':
			value = int(self.text,2)
			self.match('BIT_TOKEN')
			return value
		else:
			raise ParseError("I wIll MeSS you Up if yoU dont tYpE id BIT or (")
	
parser = MyParser()
with open('test1.txt','r') as fp:
	parser.parse(fp)
