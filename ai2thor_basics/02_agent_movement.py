from ai2thor.controller import Controller


def print_agent_state(event):
    agent = event.metadata["agent"]

    position = agent["position"]
    rotation = agent["rotation"]

    print(
        f"Position: x={position['x']:.2f}, y={position['y']:.2f}, z={position['z']:.2f}"
    )

    print(
        f"Rotation: x={rotation['x']:.2f}, y={rotation['y']:.2f}, z={rotation['z']:.2f}"
    )


def main():
    controller = Controller(scene="FloorPlan1")

    print("AI2-THOR started successfully.")
    print(f"Scene: {controller.last_event.metadata['sceneName']}")

    print("\n[Initial State]")
    print_agent_state(controller.last_event)

    actions = [
        "MoveAhead",
        "RotateRight",
        "MoveAhead",
        "RotateLeft",
    ]

    for action in actions:
        input(f"\nPress Enter to execute: {action}")

        event = controller.step(action=action)

        print(f"Action: {action}")
        print(f"Success: {event.metadata['lastActionSuccess']}")
        print_agent_state(event)

    input("\nPress Enter to exit...")
    controller.stop()


if __name__ == "__main__":
    main()
