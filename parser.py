import plex

class ParseError(Exception):
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
			raise ParseError("ERROR 404..(")

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
			self.match('IDENTIFIER')
			self.match('=')
			self.expr()
		elif self.la=='PRINT':
			self.match('PRINT')
			self.expr()
		else:
			raise ParseError("I AM WAITING IDENTIFIER or PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN':	
			self.term()
			self.term_tail()
		else:
			raise ParseError("I AM STILL WAITING ( or IDENTIFIER or BIT or )")
	def term_tail(self):
		if self.la=='XOR':
			self.match('XOR')
			self.term()
			self.term_tail()
		elif self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("I AM STILL WAITING XOR")
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN' or self.la==')':	
			self.factor()
			self.factor_tail()
		else:
			raise ParseError("I AM STILL WAITING ( or IDENTIFIER or BIT or )")
	def factor_tail(self):
		if self.la=='OR':
			self.match('OR')
			self.factor()
			self.factor_tail()
		elif self.la=='XOR' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("COME ON  OR")
	def factor(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN' or self.la==')':	
			self.atom()
			self.atom_tail()
		else:
			raise ParseError("I AM LOSING MY TEMPER ( or IDENTIFIER or BIT or )")
	def atom_tail(self):
		if self.la=='AND':
			self.match('AND')
			self.atom()
			self.atom_tail()
		elif self.la=='XOR' or self.la == 'OR' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("I AM WAITING PLEASE AND")		
	def atom(self):
		if self.la=='(':
			self.match('(')
			self.expr()
			self.match(')')
		elif self.la=='IDENTIFIER':
			self.match('IDENTIFIER')
		elif self.la=='BIT_TOKEN':
			self.match('BIT_TOKEN')
		else:
			raise ParseError("TIME OUT id bit or (")
parser = MyParser()
with open('test1.txt','r') as fp:
	parser.parse(fp)
