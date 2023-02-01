# GROUP MEMBERS
# LORIA, BRIAN ANGELO I.
# DOLOR, RONEL DYLAN JOSHUA A.
# ENRIQUEZ, CHAD ANDREI A.

class Symbol_Table:
	def __init__(self):
		self.symbol_table = {"IT": "NOOB"}

	def create_symbol_table_identifier(self, identifier, value):
		self.symbol_table[identifier] = value

	def get_symbol_table_identifier(self, identifier):
		value = self.symbol_table.get(identifier)
		return value
