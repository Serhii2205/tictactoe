from pprint import pprint


class Director:
    __builder = None

    def set_builder(self, builder):
        self.__builder = builder

    def build_action_wf(self, action):
        return (
            self.__builder.add_description("timeout_wf")
            .add_action_notation("message_node", "wait_for_interaction", action)
            .add_wait_notation("wait_for_interaction", "end", "timer.wait(100)")
            .build()
        )


class Builder:
    def __init__(self):
        self.workflow = {"notation": [], "description": ""}

    def add_description(self, description):
        self.workflow.update({"description": description})
        return self

    def add_action_notation(self, name, next_, action):
        self.workflow["notation"].append(
            {"name": name, "next": next_, "type": "action", "action": action}
        )
        return self

    def add_wait_notation(self, name, next_, wait):
        self.workflow["notation"].append(
            {"name": name, "next": next_, "type": "wait", "wait": wait}
        )
        return self

    def build(self):
        self.workflow["notation"].insert(
            0,
            {
                "name": "init",
                "next": self.workflow["notation"][0].get("name"),
                "type": "init",
            },
        )
        self.workflow["notation"].append({"name": "end", "type": "end"})
        return self.workflow


if __name__ == "__main__":
    builder = Builder()
    director = Director()

    director.set_builder(builder)

    workflow = director.build_action_wf(["bus.sendInteraction('hi')"])
    pprint(workflow)
