from ai2thor.controller import Controller


def get_agent_event(event, agent_id):
    return event.events[agent_id]


def find_visible_pickupable_object(event, agent_id):
    agent_event = get_agent_event(event, agent_id)

    for obj in agent_event.metadata["objects"]:
        if obj["visible"] and obj["pickupable"]:
            return obj

    return None


def search_pickupable_object(controller, agent_id):
    # Search the surroundings by rotating the selected agent
    for _ in range(4):
        event = controller.last_event
        target = find_visible_pickupable_object(event, agent_id)

        if target is not None:
            return target

        controller.step(
            action="RotateRight",
            agentId=agent_id,
        )

    return None


def print_inventory(event, agent_id):
    agent_event = get_agent_event(event, agent_id)
    inventory = agent_event.metadata["inventoryObjects"]

    if not inventory:
        print(f"Agent {agent_id} Inventory: empty")
        return

    print(f"Agent {agent_id} Inventory:")
    for obj in inventory:
        print(f"- {obj['objectType']} ({obj['objectId']})")


def execute_agent_task(controller, agent_id):
    print(f"\n=== Agent {agent_id} Task ===")
    print("Searching for a pickupable object...")

    # Find an object visible to this agent
    target = search_pickupable_object(
        controller,
        agent_id,
    )

    if target is None:
        print(f"Agent {agent_id}: No pickupable object found.")
        return False

    print(f"\nAgent {agent_id} found:")
    print(f"Type     : {target['objectType']}")
    print(f"Distance : {target['distance']:.2f} m")

    # Pick up the selected object
    event = controller.step(
        action="PickupObject",
        objectId=target["objectId"],
        agentId=agent_id,
    )

    agent_event = get_agent_event(event, agent_id)

    if not agent_event.metadata["lastActionSuccess"]:
        print(f"Agent {agent_id}: Pickup failed.")
        print(agent_event.metadata["errorMessage"])
        return False

    print(f"\nAgent {agent_id} picked up {target['objectType']}.")
    print_inventory(event, agent_id)

    # Drop the object held by this agent
    event = controller.step(
        action="DropHandObject",
        agentId=agent_id,
    )

    agent_event = get_agent_event(event, agent_id)

    if not agent_event.metadata["lastActionSuccess"]:
        print(f"Agent {agent_id}: Drop failed.")
        print(agent_event.metadata["errorMessage"])
        return False

    print(f"\nAgent {agent_id} dropped {target['objectType']}.")
    print_inventory(event, agent_id)

    return True


def main():
    # Initialize the environment with two agents
    controller = Controller(
        scene="FloorPlan1",
        agentCount=2,
    )

    print("=== Multi-Agent Task Execution ===")
    print(f"Scene: {controller.last_event.metadata['sceneName']}")
    print("Agents: 2")

    input("\nPress Enter to start Agent 0 task...")

    agent0_success = execute_agent_task(
        controller,
        agent_id=0,
    )

    input("\nPress Enter to start Agent 1 task...")

    agent1_success = execute_agent_task(
        controller,
        agent_id=1,
    )

    print("\n=== Task Result ===")

    print(f"Agent 0: {'Success' if agent0_success else 'Failed'}")
    print(f"Agent 1: {'Success' if agent1_success else 'Failed'}")

    if agent0_success and agent1_success:
        print("Mission Success: Both agents completed their tasks.")
    else:
        print("Mission Failed: One or more agents failed.")

    input("\nPress Enter to exit...")
    controller.stop()


if __name__ == "__main__":
    main()
