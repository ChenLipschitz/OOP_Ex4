class Node:
    def __init__(self, node_id: int, pos: tuple) -> None:
        # super()._init_()
        self.key = node_id
        self.weight = 1000000
        self.info = "Weight"
        self.tag = -1
        self.pos = pos

    def setKey(self, k: int) -> None:
        self.key = k

    def getKey(self) -> int:
        return self.key

    def setWeight(self, w: float) -> None:
        self.weight = w

    def getWeight(self, w: float) -> float:
        return self.weight

    def setInfo(self, i: str) -> None:
        self.info = i

    def getInfo(self, i: str) -> str:
        return self.info

    def setTag(self, t: int) -> None:
        self.tag = t

    def getTag(self, t: int) -> int:
        return self.tag

    def setPos(self, p: tuple) -> None:
        self.pos = p

    def getpos(self) -> tuple:
        return self.pos

    def __repr__(self):
        return f"({self.key} , {self.pos})"

    def __lt__(self, other):
        return self.weight < other.weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __ne__(self, other):
        return self.weight != other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __ge__(self, other):
        return self.weight <= other.weight


