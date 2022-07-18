# Name: Geoff Miller
# Github Username: millegeo
# Date: 5/30/2022
# Description: A simple version of a monopoly game. Contains one class for the game that creates the board spaces, initializes the players and sets out how to buy spaces, pay rent and move players.


class RealEstateGame:
	'''Class that creates a Monopoly type game/creates players for the game. Has methods to create each player, create purchase prices for each space (20 spaces), charge rent to a player whom lands on a purchased space, buy a space, get player account balance, get player current position, move a player, check to see if the game has ended'''

	def __init__(self):
		'''Method that takes no parameters, creates an empty dictionary for each player, creates a dictionary key for each space starting from 1-25.'''
		self._player = {}
		self._spaces = {}


	def create_spaces(self, go_space, game_spaces):
		'''Method to create each of the spaces, uses the empty dictionary and fills in spaces starting with 1 being the GO space and 2-15 being the game_spaces list given as a parameter. Sets up the rent amount for each space as well as how much money the player gets each time they pass go'''
		space = 1
		self._spaces = {"GO":go_space}
		while space < 25:
			for values in game_spaces:
				self._spaces[space] = {"Rent" : values, "Purchase Price" : 5*values, "Owned By" : None}
				space += 1
		return

	def create_player(self, player_name, account_balance, starting_position = 0):
		'''Method to create a player. Adds to the dictionary from the init method. Player name is the key and the value is a dictionary of account balance followed by the space that the player is currently on. Space is initialized to "GO".'''
		player_dict = self._player
		player_dict[player_name] = {"Account Balance" : account_balance, "Current Space" : starting_position}
		return

	def get_player_account_balance(self, player_name):
		'''Method to get the account balance of a specified player. Takes players name as a parameter'''
		if player_name in self._player:
			return self._player[player_name]["Account Balance"]
		else:
			return print("Invalid Player")

	def get_player_current_position(self, player_name):
		'''Method to get the current position of a specified player. Takes a players name as a parameter'''
		if player_name in self._player:
			return self._player[player_name]["Current Space"]
		else:
			return print("Invalid Player")

	def buy_space(self, player_name):
		'''Method to buy a space for a specific player. Determines if the space is already purchased, and if the player has enough funds to purchase it. Adds to dictionary of spaces owned by the player. If a legal purchase returns True, otherwise returns False.'''
		current_space = self._player[player_name]["Current Space"]
		if current_space == 0:
			return False
		account_balance = self._player[player_name]["Account Balance"]
		rent = self._spaces[current_space]["Rent"]
		if self._spaces[current_space]["Owned By"] == None:
			if (5 * rent) >= account_balance:
				return False
			else:
				self._spaces[current_space]["Owned By"] = player_name
				account_balance -= (5 * rent)
				self._player[player_name]["Account Balance"] = account_balance
				return True
		else:
			return False

	def move_player(self, player_name, num_of_spaces):
		'''Method to determine how many spaces to move a player. Checks players balance and returns if 0. If sum of roll greater than 25 subtract sum by 25 to determine space the player is on/collect defined GO amount. If the space landed on is owned by a player, subtracts the balance by rent amount and adds that amount to the player whom owns the space. If player’s account balance goes to 0 after paying rent, they will be removed from ownership of the space.'''
		if num_of_spaces < 1:
			return
		if num_of_spaces > 6:
			return
		player_balance = self._player[player_name]["Account Balance"]
		current_space = self._player[player_name]["Current Space"]
		go_amount = self._spaces["GO"]

		if player_balance == 0:
			return
		if current_space + num_of_spaces > 24:
			current_space = current_space + num_of_spaces - 25
			self._player[player_name]["Current Space"] = current_space
			player_balance += go_amount
			if current_space == 0:
				return
		else:
			current_space += num_of_spaces
			self._player[player_name]["Current Space"] = current_space

		rent = self._spaces[current_space]["Rent"]
		space_ownership = self._spaces[current_space]["Owned By"]

		if space_ownership != None and player_name:
			if rent >= player_balance:
				self._player[space_ownership]["Account Balance"] += player_balance
				player_balance -= player_balance
				for values in self._spaces:
					if "Owned By" == player_name:
						self._spaces["Owned By"] = None
				check_game = self.check_game_over()
				if check_game != "":
					return check_game
				else:
					return print("Out of money, you lose")

			else:
				self._player[space_ownership]["Account Balance"] += rent
				self._player[player_name]["Account Balance"] -= rent
		else:
			return


	def check_game_over(self):
		'''Method to determine if the game is over. Checks all players balances and if only one is not 0 it will return the name of the winner. Otherwise it returns an empty string.'''
		still_playing_count = 0
		for players in self._player:
			if self._player[players]["Account Balance"] > 0:
				still_playing_count += 1
				winner = players
		if still_playing_count ==  1:
			return winner
		else:
			return ""

game = RealEstateGame()

rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350, 350, 350]
game.create_spaces(50, rents)

game.create_player("Player 1", 1000)
game.create_player("Player 2", 1000)
game.create_player("Player 3", 1000)

print(game.move_player("Player 1", 6))
print(game.buy_space("Player 1"))
game.move_player("Player 2", 6)
print(game.buy_space("Player 2"))

print(game.get_player_account_balance("Player 1"))
print(game.get_player_account_balance("Player 2"))

print(game.check_game_over())