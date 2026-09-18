from ai2thor.controller import Controller


def main():
    controller = Controller(scene="FloorPlan1")

    print("AI2-THOR started successfully.")
    print(f"Scene: {controller.last_event.metadata['sceneName']}")

    input("Press Enter to exit...")

    controller.stop()


if __name__ == "__main__":
    main()
