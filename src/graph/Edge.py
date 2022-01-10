class Edge:
    def __init__(self, src: int, dest: int, weight: float) -> None:
        super().__init__()
        self.src = src
        self.dest = dest
        self.weight = weight
        self.info = "Weight"
        self.tag = -1

    def setSrc(self, s: int) -> None:
        self.src = s

    def setDest(self, d: int) -> None:
        self.dest = d

    def setWeight(self, w: float) -> None:
        self.weight = w

    def setInfo(self, i: str) -> None:
        self.info = i

    def setTag(self, t: int) -> None:
        self.tag = t

    def getweight(self):
        return self.weight

    def getweight(self):
        return self.weight