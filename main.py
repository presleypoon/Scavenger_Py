import os
from subprocess import run
from time import sleep
from random import randint as Random
import msvcrt


class Entity:
    def __init__(self, x=0, y=0) -> None:
        self.x: int = x
        self.y: int = y


Player = Entity()
Loot = Entity()
Enemy = Entity(5, 5)

Score = -10
FPS = 30
Tick = 0
Health = 20

Paused = False

run('cls' if os.name == 'nt' else 'clear', shell=True)
os.system("")


def Move(c: str) -> None:
    match c:
        case 'w':
            Player.y -= 1
            if Player.y < 0:
                Player.y = 9
        case 'a':
            Player.x -= 1
            if Player.x < 0:
                Player.x = 9
        case 's':
            Player.y += 1
            if Player.y > 9:
                Player.y = 0
        case 'd':
            Player.x += 1
            if Player.x > 9:
                Player.x = 0


def PickUpLogic() -> None:
    global Score
    if (Player.x != Loot.x or Player.y != Loot.y):
        return
    Loot.x = Random(0, 9)
    Loot.y = Random(0, 9)
    Score += 10
    if Score >= 500:
        Render()
        print("\nYou've won!!!")
        Restart()


def EnemyLogic() -> None:
    global Score, Health
    if Tick % 10:
        return

    XDist: int = Enemy.x - Player.x
    YDist: int = Enemy.y - Player.y

    if abs(XDist) > abs(YDist):
        Enemy.x -= sign(XDist)
    else:
        Enemy.y -= sign(YDist)

    if Enemy.x != Player.x or Enemy.y != Player.y:
        return

    Score -= 5
    Health -= 1

    if (Health != 0):
        return

    Render()
    print("\nYou've lose :(")
    Restart()


def sign(num: int) -> int:
    if num > 0:
        return 1
    if num < 0:
        return -1
    return 0


def Render() -> None:
    Buffer = """++++++++++++
+          +
+          +
+          +
+          +
+          +
+          +
+          +
+          +
+          +
+          +
++++++++++++"""
    Buffer: str = ChangeCharAtId(
        Buffer, (Player.x + 1) + 13 * (Player.y + 1), '@')
    Buffer: str = ChangeCharAtId(
        Buffer, (Enemy.x + 1) + 13 * (Enemy.y + 1), '!')
    Buffer: str = ChangeCharAtId(Buffer, (Loot.x + 1) + 13 * (Loot.y + 1), '$')

    print(f"\x1b[?25l\x1b[H{Score:<4}", end="")

    PrintColouredPx('r', Health)
    PrintColouredPx('d', 20-Health)
    print()

    for i in range(0, len(Buffer)):
        match Buffer[i]:
            case ' ': print("  ", end="")
            case '+': PrintColouredPx('w', 2)
            case '@': PrintColouredPx('g', 2)
            case '$': PrintColouredPx('y', 2)
            case '!': PrintColouredPx('r', 2)
            case '\n': print()

    print("\x1b[?25h", end="")


def PrintColouredPx(colour: str, length: int) -> None:
    # @param colour b for black, r for red, g for green, y for yellow, l for blue, m for magenta, c for cyan and w for white, other will be default
    match colour:
        case 'b': print("\x1b[40m", end="")
        case 'r': print("\x1b[41m", end="")
        case 'g': print("\x1b[42m", end="")
        case 'y': print("\x1b[43m", end="")
        case 'l': print("\x1b[44m", end="")
        case 'm': print("\x1b[45m", end="")
        case 'c': print("\x1b[46m", end="")
        case 'w': print("\x1b[47m", end="")
    print(" " * length + "\x1b[49m", end="")


def ChangeCharAtId(list: str, id: int, char: str) -> str:
    return list[:id] + char + list[id + 1:]


def Restart() -> None:
    global Player, Loot, Enemy, Score, Tick, Health, Paused
    Player.x, Player.y = 0, 0
    Loot.x, Loot.y = 0, 0
    Enemy.x, Enemy.y = 5, 5

    Score = -10
    Tick = 0
    Health = 20

    Paused = False
    run('cls' if os.name == 'nt' else 'clear', shell=True)
    Render()
    msvcrt.getch()


if __name__ == "__main__":
    msvcrt.getch()
    while True:
        input: bool = msvcrt.kbhit()
        if input:
            c: str = msvcrt.getch().decode('utf-8').lower()
            if c == 'p':
                Paused: bool = not Paused

        if not Paused:
            if input:
                Move(c)
            PickUpLogic()
            EnemyLogic()
            Render()
            Tick += 1
        print("\x1b[?25h", end="")
        sleep(1/FPS)
