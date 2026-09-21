from ai2thor.controller import Controller


# Find the first visible object of a specific type
def find_visible_object(event, object_type):
    for obj in event.metadata["objects"]:
        if obj["visible"] and obj["objectType"] == object_type:
            return obj
    return None


# Search for an object by rotating the agent
def search_object(controller, object_type):
    for _ in range(4):
        event = controller.last_event
        target = find_visible_object(event, object_type)

        if target is not None:
            return target

        controller.step(action="RotateRight")

    return None


# Move toward the target until it becomes interactable
def approach_object(controller, object_type, max_steps=8):
    for _ in range(max_steps):
        target = find_visible_object(controller.last_event, object_type)

        if target and target["distance"] < 1.2:
            return target

        controller.step(action="MoveAhead")

    return find_visible_object(controller.last_event, object_type)


def main():
    # Initialize the environment
    controller = Controller(scene="FloorPlan1")

    print("=== Simple Task: Apple → CounterTop ===")

    # Step 1. Find Apple
    print("\n[1] Searching for Apple...")
    apple = search_object(controller, "Apple")

    if apple is None:
        print("Apple not found.")
        controller.stop()
        return

    apple = approach_object(controller, "Apple")

    if apple is None:
        print("Could not approach the Apple.")
        controller.stop()
        return

    print(f"Apple found ({apple['distance']:.2f} m)")

    # Step 2. Pick up Apple
    event = controller.step(action="PickupObject", objectId=apple["objectId"])

    if not event.metadata["lastActionSuccess"]:
        print("Failed to pick up Apple.")
        print(event.metadata["errorMessage"])
        controller.stop()
        return

    print("Picked up Apple.")

    # Step 3. Find CounterTop
    print("\n[2] Searching for CounterTop...")
    countertop = search_object(controller, "CounterTop")

    if countertop is None:
        print("CounterTop not found.")
        controller.stop()
        return

    countertop = approach_object(controller, "CounterTop")

    if countertop is None:
        print("Could not approach the CounterTop.")
        controller.stop()
        return

    print(f"CounterTop found ({countertop['distance']:.2f} m)")

    # Step 4. Place Apple on CounterTop
    event = controller.step(action="PutObject", objectId=countertop["objectId"])

    print("\n[3] Task Result")

    if event.metadata["lastActionSuccess"]:
        print("Mission Success: Apple placed on CounterTop.")
    else:
        print("Mission Failed")
        print(event.metadata["errorMessage"])

    input("\nPress Enter to exit...")
    controller.stop()


if __name__ == "__main__":
    main()
