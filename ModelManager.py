import random
from collections import defaultdict
from enum import Enum


class Status(Enum):
    online = "online"
    offline = "offline"


class Model:
    def __init__(self, name, version, status, cost_per_use):
        self._name = name
        self._version = version
        self._status = status
        self._cost_per_use = cost_per_use

    def get_name(self):
        return self._name

    def get_version(self):
        return self._version

    def get_status(self):
        return self._status

    def get_cost(self):
        return self._cost_per_use

    def set_status(self, status):
        self._status = status


class Registry:
    def __init__(self):
        self._registry = defaultdict(list)

    def add_model(self, model):
        self._registry[model.get_name()].append(model)

    def get_models(self):
        return self._registry

    def search(self, name):
        if name in self._registry:
            return self._registry[name]
        else:
            print("model does not exist in registry")
            return

    def version_search(self, name, version):
        if name in self._registry:
            for i in self._registry[name]:
                if i.get_version() == version:
                    print(i)
                    return i
        print("that model version does not exisit")
        return


class Route:
    def __init__(self, name, registry):
        self._registry = registry
        self._weights = defaultdict(list)
        self._name = name

    def get_name(self):
        return self._name

    def set_split(self, weights):
        for version, weight in weights.items():
            self._weights[version] = weight

    def route_request(self, version_pin):
        if version_pin is not None:
            model = self._registry.version_search(self._name, version_pin)
            if model.get_status() == Status.online:
                print("the next task will be assigned to: ", self._name, version_pin)
                return
            else:
                highest = max

        roll = random.random()
        cumulative = 0
        for i, w in self._weights.items():
            model = self._registry.version_search(self._name, i)
            cumulative += w
            if model.get_status() == Status.online and roll < cumulative:
                print("the next task will be assigned to: ", self._name, i)
                return i


def main():
    model1 = Model("llama", "v3", Status.online, 0.01)
    model2 = Model("llama", "v4", Status.online, 0.21)
    model3 = Model("gpt", "4.0", Status.offline, 0.22)
    model4 = Model("llama", "v5", Status.online, 0.4)

    models = Registry()
    route = Route("llama", models)

    models.add_model(model1)
    models.add_model(model4)
    models.add_model(model2)
    models.add_model(model3)

    route.set_split({"v3": 0.2, "v4": 0.6, "v5": 0.2})
    route.route_request("v5")

    # models.search("llama")
    # models.version_search("llama", "v3")


main()

# # Step 1: Define a base class
# class FallbackStrategy:
#     def select(self, registry, name, weights):
#         raise NotImplementedError

# # Step 2: Make concrete strategies
# class WeightedFallback(FallbackStrategy):
#     def select(self, registry, name, weights):
#         # Your existing traffic split logic goes here
#         # (the random roll + cumulative loop, but only online models)
#         pass

# class HighestWeightFallback(FallbackStrategy):
#     def select(self, registry, name, weights):
#         # Pick the online model with the biggest weight
#         pass

# # Step 3: Route receives the strategy
# class Route:
#     def __init__(self, name, registry, fallback_strategy):
#         self._fallback = fallback_strategy
#         # ... rest of init

#     def route_request(self, version_pin):
#         if version_pin is not None:
#             model = self._registry.version_search(self._name, version_pin)
#             if model and model.get_status() == Status.online:
#                 return model
#             else:
#                 # Don't hardcode the fallback — delegate it
#                 return self._fallback.select(self._registry, self._name, self._weights)

#         # ... normal traffic split logic

# # Step 4: In main(), you choose which strategy to use
# route = Route("llama", models, WeightedFallback())
