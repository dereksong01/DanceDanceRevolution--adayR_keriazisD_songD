from util.ids import Id, gen_id

PlayerId = Id


class Player:
    def __init__(self: "Player", name: str) -> None:
        self.id = gen_id(16)
        self.name = name
        self.color = ""
