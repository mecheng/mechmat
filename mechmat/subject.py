import logging


class Subject:
    def __init__(self, prop, *observers):
        self.property = prop
        self.observers = list(observers)

    def register(self, *observers):
        if hasattr(observers, '__iter__'):
            self.observers.extend(observers)
        else:
            self.observers.append(observers)

    def send(self, instance, key):
        for obs in self.observers:
            obs.notify(instance, key)

    def notify(self, instance, key):
        logging.debug(
            'Observer {} notified for change of {} property in material {}'.format(self.property, key, instance))
        setattr(instance, self.property, key)
