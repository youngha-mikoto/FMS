from ai2thor.controller import Controller


def print_object_summary(obj):
    position = obj["position"]

    print(f"Name       : {obj['name']}")
    print(f"Type       : {obj['objectType']}")
    print(f"Object ID  : {obj['objectId']}")
    print(
        f"Position   : "
        f"x={position['x']:.2f}, "
        f"y={position['y']:.2f}, "
        f"z={position['z']:.2f}"
    )
    print(f"Visible    : {obj['visible']}")
    print(f"Pickupable : {obj['pickupable']}")
    print(f"Receptacle : {obj['receptacle']}")
    print("-" * 50)


def main():
    controller = Controller(scene="FloorPlan1")

    event = controller.last_event
    objects = event.metadata["objects"]

    print("AI2-THOR started successfully.")
    print(f"Scene: {event.metadata['sceneName']}")
    print(f"Number of objects: {len(objects)}")

    print("\n[Object Types]")

    object_types = sorted({obj["objectType"] for obj in objects})

    for object_type in object_types:
        print(f"- {object_type}")

    print("\n[Visible Objects]")

    visible_objects = [obj for obj in objects if obj["visible"]]

    if not visible_objects:
        print("No visible objects.")
    else:
        for obj in visible_objects:
            print_object_summary(obj)

    input("\nPress Enter to exit...")
    controller.stop()


if __name__ == "__main__":
    main()
