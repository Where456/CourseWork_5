from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = True

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> str:
        if self.player.hp <= 0:
            self.battle_result = f'{self.player.name} проиграл битву'
            return self._end_game()
        elif self.enemy.hp <= 0:
            self.battle_result = f'Так держать {self.player.name}, ты одержал победу!!! '
            return self._end_game()
        elif self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = 'Ничья :)'
            return self._end_game()

    def _stamina_regeneration(self) -> None:
        for i in (self.player, self.enemy):
            if i.stamina + self.STAMINA_PER_ROUND * i.unit_class.stamina > i.unit_class.max_stamina:
                i.stamina = i.unit_class.max_stamina
            else:
                i.stamina += self.STAMINA_PER_ROUND * i.unit_class.stamina

    def next_turn(self):
        result = self._check_players_hp()
        self._stamina_regeneration()
        if result:
            return result
        self._stamina_regeneration()
        result = self.enemy.hit(self.player)
        return result

        # TODO СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
        # TODO срабатывает когда игроп пропускает ход или когда игрок наносит удар.
        # TODO создаем поле result и проверяем что вернется в результате функции self._check_players_hp
        # TODO если result -> возвращаем его
        # TODO если же результата пока нет и после завершения хода игра продолжается,
        # TODO тогда запускаем процесс регенирации стамины и здоровья для игроков (self._stamina_regeneration)
        # TODO и вызываем функцию self.enemy.hit(self.player) - ответный удар врага

    def _end_game(self) -> str:
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        result = self.player.hit(self.enemy)
        self.next_turn()
        return result
        # TODO КНОПКА УДАР ИГРОКА -> return result: str
        # TODO получаем результат от функции self.player.hit
        # TODO запускаем следующий ход
        # TODO возвращаем результат удара строкой

    def player_use_skill(self):
        res = self.player.use_skill(self.enemy)
        self.next_turn()
        return res
        # TODO КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        # TODO получаем результат от функции self.use_skill
        # TODO включаем следующий ход
        # TODO возвращаем результат удара строкой
