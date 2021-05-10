from interfaceConcept.reporter import Reporter

class PetInteface:
    def run(self) -> str:
        raise NotImplementedError

    def eat(self, amount:int) -> str:
        raise NotImplementedError

    def shit(self) -> str:
        raise NotImplementedError

class Cat(PetInteface):
    def __init__(self, reporter:Reporter):
        self.reporter = reporter

    def run(self) -> str:
        action = "I've ran for 3 miles."
        self.reporter.report(action)
        return action

    def eat(self, amount:int) -> str:
        action = "I've eaten {} cat food(s).".format(amount)
        self.reporter.report(action)
        return action

    def shit(self) -> str:
        action = "I've shit on your carpet, happy cleaning!!!"
        self.reporter.report(action)
        return action

if __name__ == '__main__':
    cat = Cat(Reporter())
    cat.run()
    cat.shit()
    cat.eat(4)
