import pykka
from grain1.actor import Grain1Actor
from grain2.actor import Grain2Actor
import random


class Orchestrator:
    def __init__(self, grain1_pool_size=3):
        """
        Initializes the orchestrator and starts actor instances.

        :param grain1_pool_size: Number of Grain1Actor instances to spawn for parallel processing.
        """
        # Start multiple Grain1 actors in a pool
        self.grain1_proxies = [
            Grain1Actor.start().proxy() for _ in range(grain1_pool_size)
        ]
        print(f"Spawned {grain1_pool_size} Grain1 actors for parallel processing.")

        # Start a single Grain2 actor
        self.grain2_proxy = Grain2Actor.start().proxy()

    def run_workflow(self, input_data_list):
        """
        Chains workflows for multiple input data concurrently.

        :param input_data_list: List of input data items to process.
        """
        futures = []

        # Distribute requests to Grain1 actors in the pool
        for data in input_data_list:
            try:
                actor_proxy = random.choice(self.grain1_proxies)
                print(f"Sending data '{data}' to Grain1 actor {actor_proxy.actor_urn}")
                future = actor_proxy.on_receive({"command": "process_data", "data": data})
                futures.append(future)  # Future objects now
            except Exception as e:
                print(f"Error while sending data to Grain1Actor: {e}")

        # Collect results safely
        processed_results = []
        for i, future in enumerate(futures):
            try:
                result = future.get(timeout=5)
                processed_results.append(result)
            except Exception as e:
                print(f"Error receiving result for input '{input_data_list[i]}': {e}")
                processed_results.append(f"Error for {input_data_list[i]}")

        print("\nAll Grain1 results received. Passing to Grain2...\n")

        # Pass results to Grain2
        grain2_futures = []
        for result in processed_results:
            try:
                future = self.grain2_proxy.on_receive({"command": "analyze_data", "data": result})
                grain2_futures.append(future)
            except Exception as e:
                print(f"Error while sending data to Grain2Actor: {e}")

        # Collect final results safely
        final_results = []
        for i, future in enumerate(grain2_futures):
            try:
                result = future.get(timeout=5)
                final_results.append(result)
            except Exception as e:
                print(f"Error receiving result for Grain2 processing: {e}")
                final_results.append("Error in Grain2 processing")

        print("\nFinal Workflow Results:")
        for result in final_results:
            print(result)

    def stop(self):
        """Stops all running actors."""
        pykka.ActorRegistry.stop_all()
        print("All actors stopped.")


if __name__ == "__main__":
    orchestrator = Orchestrator(grain1_pool_size=5)  # Spawn 5 Grain1 actors
    input_data_list = [
        "Request 1",
        "Request 2",
        "Request 3",
        "Request 4",
        "Request 5",
    ]
    print("Starting Workflow...\n")
    orchestrator.run_workflow(input_data_list)
    orchestrator.stop()
    orchestrator.stop()