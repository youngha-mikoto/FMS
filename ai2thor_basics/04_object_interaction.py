from ai2thor.controller import Controller


# Find the first visible and pickupable object
def find_visible_pickupable_object(event):
    objects = event.metadata["objects"]

    for obj in objects:
        if obj["visible"] and obj["pickupable"]:
            return obj

    return None


# Search for a pickupable object by rotating the agent
def search_pickupable_object(controller):
    for _ in range(4):
        event = controller.last_event
        target = find_visible_pickupable_object(event)

        if target is not None:
            return target

        controller.step(action="RotateRight")

    return None


# Print the objects currently held by the agent
def print_inventory(event):
    inventory = event.metadata["inventoryObjects"]

    if not inventory:
        print("Inventory: empty")
        return

    print("Inventory:")
    for obj in inventory:
        print(f"- {obj['objectType']} ({obj['objectId']})")


def main():
    # Initialize the AI2-THOR environment
    controller = Controller(scene="FloorPlan1")

    print("AI2-THOR started successfully.")
    print(f"Scene: {controller.last_event.metadata['sceneName']}")

    print("\nSearching for a visible pickupable object...")

    # Search the surroundings for an interactable object
    target = search_pickupable_object(controller)

    if target is None:
        print("\nNo visible pickupable object found.")
        controller.stop()
        return

    print("\n[Target Object]")
    print(f"Type      : {target['objectType']}")
    print(f"Object ID : {target['objectId']}")
    print(f"Distance  : {target['distance']:.2f} m")

    input("\nPress Enter to pick up the object...")

    # Pick up the target using its unique object ID
    event = controller.step(
        action="PickupObject",
        objectId=target["objectId"],
    )

    print("\n[Pickup Result]")
    print(f"Success: {event.metadata['lastActionSuccess']}")

    # Stop if the pickup action fails
    if not event.metadata["lastActionSuccess"]:
        print(f"Error: {event.metadata['errorMessage']}")
        input("\nPress Enter to exit...")
        controller.stop()
        return

    print_inventory(event)

    input("\nPress Enter to put down the object...")

    # Drop the object currently held by the agent
    event = controller.step(action="DropHandObject")

    print("\n[Drop Result]")
    print(f"Success: {event.metadata['lastActionSuccess']}")

    if not event.metadata["lastActionSuccess"]:
        print(f"Error: {event.metadata['errorMessage']}")

    print_inventory(event)

    input("\nPress Enter to exit...")
    controller.stop()


if __name__ == "__main__":
    main()
