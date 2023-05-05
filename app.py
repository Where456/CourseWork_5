from base import Arena

from flask import Flask, render_template, request, redirect, url_for

from equipment import Equipment
from unit import PlayerUnit, EnemyUnit
from classes import unit_classes, WarriorClass, ThiefClass

app = Flask(__name__)

heroes = {
    "player": PlayerUnit(name='ДАЯНА', unit_class=WarriorClass),
    "enemy": EnemyUnit(name='Лох какой-то', unit_class=ThiefClass)
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(heroes['player'], heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, result=arena.battle_result())


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == 'POST':
        name = request.form['name']
        unit_class = request.form['unit_class']
        weapon = request.form['weapon']
        armor = request.form['armor']

        hero = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        hero.equip_weapon(Equipment().get_weapon(weapon))
        hero.equip_armor(Equipment().get_armor(armor))

        heroes['player'] = hero
        return redirect(url_for("choose_enemy"))

    if request.method == 'GET':
        header = 'Выберите героя'
        classes = unit_classes
        weapons = Equipment().get_weapons_names()
        armors = Equipment().get_armors_names()

        return render_template("hero_choosing.html", result={
            "header": header,
            "classes": classes,
            "weapons": weapons,
            "armors": armors
        })


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == 'POST':
        name = request.form['name']
        unit_class = request.form['unit_class']
        weapon = request.form['weapon']
        armor = request.form['armor']

        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        enemy.equip_weapon(Equipment().get_weapon(weapon))
        enemy.equip_armor(Equipment().get_armor(armor))

        heroes['enemy'] = enemy
        return redirect(url_for("start_fight"))

    if request.method == 'GET':
        header = 'Выберите противника'
        classes = unit_classes
        weapons = Equipment().get_weapons_names()
        armors = Equipment().get_armors_names()

        return render_template("hero_choosing.html", result={
            "header": header,
            "classes": classes,
            "weapons": weapons,
            "armors": armors
        })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
