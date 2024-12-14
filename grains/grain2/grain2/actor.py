import pykka

class Grain2Actor(pykka.ThreadingActor):
    """
    Grain2 actor that analyzes processed data and returns a final result.
    """
    def on_receive(self, message):
        command = message.get("command")
        data = message.get("data")

        if command == "analyze_data":
            print(f"[Grain2] Analyzing data: {data}")
            return f"[Grain2] Analyzed: {data}"

        return f"Unknown command: {command}"