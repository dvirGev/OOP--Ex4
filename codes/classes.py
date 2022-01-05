class agent:
    def __init__(self, data: dict) -> None:
        self.id = int(data['id'])
        self.value = float(data['value'])
        self.src = int(data['src'])
        self.dest = int(data['dest'])
        self.speed = float(data['speed'])
        xyz = str(data['pos']).split(',')
        self.pos = []
        for n in xyz:
            self.pos.append(float(n))
        
        self.nextStations = None
        self.time = float('inf')
        self.priorty = 0
    def update(self, data: dict) -> None:
        self.value = float(data['value'])
        self.src = int(data['src'])
        self.dest = int(data['dest'])
        self.speed = float(data['speed'])
        xyz = str(data['pos']).split(',')
        self.pos = []
        for n in xyz:
            self.pos.append(float(n))
        self.time = float('inf')
        self.priorty = 0
        
class pokemon:
    def __init__(self, data:dict) -> None:
        self.value = data['value']
        self.type =int(data['type'])
        xyz = str(data['pos']).split(',')
        self.pos = []
        for n in xyz:
            self.pos.append(float(n))
        self.src = None
        self.dest = None
        self.agent = None
    def __repr__(self) -> str:
        return str((self.src, self.dest))
    

        