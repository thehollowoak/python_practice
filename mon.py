from random import randint

types = ['grass', 'water', 'fire', 'bug', 'flying', 'normal', 'electric']
type_map = [[1],
			[2],
			[3],
			[4, 5],
			[6, 8],
			[7],
			[9]]
advantage_map = [[.5, 2, .5, .5, .5, 1, 1],
				 [.5, .5, 2, 1, 1, 1, 1],
				 [2, .5, .5, 2, 1, 1, 1],
				 [2, 1, .5, 1, .5, 1, 1],
				 [2, 1, 1, 2, 1, 1, 1],
				 [1, 1, 1, 1, 1, 1, 1],
				 [.5, 2, 1, 1, 2, 1, 1]]

def getType(number):
	for row in type_map:
		if number in row:
			return types[type_map.index(row)]

def advantage(attacker, defender):
	return advantage_map[types.index(attacker)][types.index(defender)]

class Mon:
	dex = ['', 'bulb', 'squirt', 'char', 'catter', 'weed', 'pidge', 'rat', 'spar', 'pika']

	def __init__(self, number, lvl, **info):
		self.number = number
		self.type = getType(number)
		self.lvl = lvl
		self.exp = 0
		self.hp = self.totalHp()
		if info.get('name'):
			self.name = info.get('name')
		else: self.name = self.dex[number]

	def attack(self, enemy):
		damage = int(self.attackDamage() * advantage(self.type, enemy.type))
		print("%s does %d damage to %s!" % (self.name, damage, enemy.name))
		enemy.hp -= damage
		if enemy.hp <= 0:
			enemy.faints()
			self.getExp(enemy.giveExp())

	def faints(self):
		print("%s fainted!" % self.name)
		self.hp = 0

	def heal(self, amount):
		self.hp += amount
		if self.hp > self.totalHp():
			self.hp = self.totalHp()

	def getExp(self, gain):
		print("%s gains %d exp!" % (self.name, gain))
		self.exp += gain
		if self.exp > self.nextLvl():
			self.exp -= self.nextLvl()
			self.lvl += 1
			print("%s is now level %d!" % (self.name, self.lvl))

	def giveExp(self): return self.lvl*10
	def nextLvl(self): return self.lvl**2+10
	def totalHp(self): return self.lvl*7+20
	def attackDamage(self): return self.lvl*2+5

a = Mon(1,1)
b = Mon(2,1)
def explore():
	num = randint(2, 9)
	if (num == 2): print("Nothing here."); return
	elif (num == 3): num = randint(1,3)
	enemy = Mon(num, randint(1, 4))
	print("Wild %s attacks!" % enemy.name)
	return enemy




