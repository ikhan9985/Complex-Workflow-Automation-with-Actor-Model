import pykka

class Grain1Actor(pykka.ThreadingActor):
    """
    Grain1 actor that processes data and returns a processed result.
    """
    def on_receive(self, message):
        command = message.get("command")
        data = message.get("data")

        if command == "process_data":
            print(f"[Grain1] Processing data: {data}")
            return f"[Grain1] Processed: {data.upper()}"

        return f"Unknown command: {command}"