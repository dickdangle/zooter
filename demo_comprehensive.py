#!/usr/bin/env python3
"""
Comprehensive demonstration of Agent Interface Chain concepts.
Shows various scenarios and use cases.
"""

import time
from agent_manager import Agent, Interface, InterfaceChain, AgentManager, TUI


def demo_basic_chain():
    """Demo 1: Basic interface chain setup."""
    tui = TUI()
    manager = AgentManager()
    
    tui.clear()
    print(tui.color("═" * 70, "cyan"))
    print(tui.color("DEMO 1: Basic Interface Chain", "bold"))
    print(tui.color("═" * 70, "cyan"))
    print("\nSetting up a simple 3-stage processing pipeline...\n")
    
    # Create agents
    agents = [
        Agent("input", "InputAgent", metadata={"role": "data_intake"}),
        Agent("process", "ProcessorAgent", metadata={"role": "transformation"}),
        Agent("output", "OutputAgent", metadata={"role": "delivery"}),
    ]
    
    for agent in agents:
        manager.register_agent(agent)
        print(f"  ✓ Registered {agent.name}")
    
    print("\nBuilding interface chain...\n")
    
    # Create chain
    chain = manager.create_interface_chain()
    interfaces = [
        Interface("i1", "DataIngestion"),
        Interface("i2", "Processing"),
        Interface("i3", "OutputDelivery"),
    ]
    
    for iface in interfaces:
        chain.add_interface(iface)
        print(f"  ✓ Added interface: {iface.name}")
    
    print("\nAttaching agents to interfaces...\n")
    
    # Attach agents
    for agent, iface in zip(agents, interfaces):
        manager.attach_agent_to_interface(agent.id, iface.id)
        agent.activate()
        print(f"  ✓ {agent.name} ← {iface.name}")
    
    print("\n" + tui.color("Result: Single chain with 3 interfaces managing 3 agents", "green"))
    print(tui.color("No single point of failure in the processing pipeline.\n", "green"))


def demo_multiple_chains():
    """Demo 2: Multiple independent chains."""
    tui = TUI()
    manager = AgentManager()
    
    tui.clear()
    print(tui.color("═" * 70, "cyan"))
    print(tui.color("DEMO 2: Multiple Independent Interface Chains", "bold"))
    print(tui.color("═" * 70, "cyan"))
    print("\nDemonstrating isolation and independence...\n")
    
    # Chain 1: Production pipeline
    print(tui.color("Chain 1: Production Pipeline", "yellow"))
    chain1 = manager.create_interface_chain()
    
    prod_agents = [
        Agent("p1", "ProductionCollector"),
        Agent("p2", "ProductionProcessor"),
    ]
    
    prod_interfaces = [
        Interface("pi1", "ProdIngestion"),
        Interface("pi2", "ProdProcessing"),
    ]
    
    for agent in prod_agents:
        manager.register_agent(agent)
    
    for iface in prod_interfaces:
        chain1.add_interface(iface)
    
    manager.attach_agent_to_interface("p1", "pi1")
    manager.attach_agent_to_interface("p2", "pi2")
    
    print(f"  → {prod_interfaces[0].name} ← {prod_agents[0].name}")
    print(f"  → {prod_interfaces[1].name} ← {prod_agents[1].name}")
    
    # Chain 2: Monitoring pipeline
    print(tui.color("\nChain 2: Monitoring Pipeline", "yellow"))
    chain2 = manager.create_interface_chain()
    
    monitor_agents = [
        Agent("m1", "HealthMonitor"),
        Agent("m2", "AlertAgent"),
    ]
    
    monitor_interfaces = [
        Interface("mi1", "HealthCheck"),
        Interface("mi2", "Alerting"),
    ]
    
    for agent in monitor_agents:
        manager.register_agent(agent)
    
    for iface in monitor_interfaces:
        chain2.add_interface(iface)
    
    manager.attach_agent_to_interface("m1", "mi1")
    manager.attach_agent_to_interface("m2", "mi2")
    
    print(f"  → {monitor_interfaces[0].name} ← {monitor_agents[0].name}")
    print(f"  → {monitor_interfaces[1].name} ← {monitor_agents[1].name}")
    
    print("\n" + tui.color("Result: 2 independent chains operating in parallel", "green"))
    print(tui.color("Issues in one chain don't affect the other.\n", "green"))


def demo_command_handling():
    """Demo 3: Command handling in interfaces."""
    tui = TUI()
    
    tui.clear()
    print(tui.color("═" * 70, "cyan"))
    print(tui.color("DEMO 3: Command Handling", "bold"))
    print(tui.color("═" * 70, "cyan"))
    print("\nInterfaces can handle custom commands...\n")
    
    # Create interface with commands
    interface = Interface("cmd1", "CommandInterface")
    
    def process_data(data):
        return f"Processed: {data}"
    
    def validate_data(data):
        return len(data) > 0
    
    def transform_data(data):
        return data.upper()
    
    interface.register_command("process", process_data)
    interface.register_command("validate", validate_data)
    interface.register_command("transform", transform_data)
    
    print("Registered commands:")
    for cmd in interface.commands.keys():
        print(f"  • {cmd}")
    
    print("\nExecuting commands:")
    
    test_data = "sample data"
    
    result1 = interface.execute_command("validate", test_data)
    print(f"  validate('{test_data}') → {result1}")
    
    result2 = interface.execute_command("transform", test_data)
    print(f"  transform('{test_data}') → {result2}")
    
    result3 = interface.execute_command("process", test_data)
    print(f"  process('{test_data}') → {result3}")
    
    print("\n" + tui.color("Result: Flexible command system for interface operations", "green"))
    print(tui.color("Each interface can define its own command set.\n", "green"))


def demo_scalability():
    """Demo 4: Scalability demonstration."""
    tui = TUI()
    manager = AgentManager()
    
    tui.clear()
    print(tui.color("═" * 70, "cyan"))
    print(tui.color("DEMO 4: Scalability", "bold"))
    print(tui.color("═" * 70, "cyan"))
    print("\nScaling to multiple chains and agents...\n")
    
    # Create multiple chains
    num_chains = 5
    agents_per_chain = 3
    
    total_agents = 0
    total_interfaces = 0
    
    for chain_num in range(1, num_chains + 1):
        chain = manager.create_interface_chain()
        
        for agent_num in range(1, agents_per_chain + 1):
            agent_id = f"a{chain_num}_{agent_num}"
            agent = Agent(agent_id, f"Agent_{chain_num}_{agent_num}")
            manager.register_agent(agent)
            total_agents += 1
            
            iface_id = f"i{chain_num}_{agent_num}"
            interface = Interface(iface_id, f"Interface_{chain_num}_{agent_num}")
            chain.add_interface(interface)
            total_interfaces += 1
            
            manager.attach_agent_to_interface(agent_id, iface_id)
    
    print(f"  Created: {num_chains} chains")
    print(f"  Total agents: {total_agents}")
    print(f"  Total interfaces: {total_interfaces}")
    print(f"  Agents per chain: {agents_per_chain}")
    
    print("\n" + tui.color(f"Result: System scales to {total_agents} agents across {num_chains} chains", "green"))
    print(tui.color("Architecture supports horizontal scaling without bottlenecks.\n", "green"))


def main():
    """Run all demonstrations."""
    tui = TUI()
    
    # Header
    tui.clear()
    print(tui.color("╔════════════════════════════════════════════════════════════════════╗", "cyan"))
    print(tui.color("║    AGENT INTERFACE CHAIN MANAGER - Comprehensive Demonstration     ║", "cyan"))
    print(tui.color("║         The Next Evolution of TUIs for Agent Management            ║", "cyan"))
    print(tui.color("╚════════════════════════════════════════════════════════════════════╝", "cyan"))
    print()
    print(tui.color("Core Principle:", "magenta"))
    print("  Managing all agents through ONE interface is a risk.")
    print("  Interface chains distribute risk and enable scalability.\n")
    input("Press Enter to start demonstrations...")
    
    # Run demos
    demo_basic_chain()
    input("\nPress Enter for next demo...")
    
    demo_multiple_chains()
    input("\nPress Enter for next demo...")
    
    demo_command_handling()
    input("\nPress Enter for next demo...")
    
    demo_scalability()
    
    # Conclusion
    tui.clear()
    print(tui.color("╔════════════════════════════════════════════════════════════════════╗", "cyan"))
    print(tui.color("║                         CONCLUSION                                 ║", "cyan"))
    print(tui.color("╚════════════════════════════════════════════════════════════════════╝", "cyan"))
    print()
    print(tui.color("Key Takeaways:", "bold"))
    print()
    print("  1. " + tui.color("Risk Distribution", "green"))
    print("     Interface chains eliminate single points of failure")
    print()
    print("  2. " + tui.color("Scalability", "green"))
    print("     Add new chains without disrupting existing ones")
    print()
    print("  3. " + tui.color("Isolation", "green"))
    print("     Problems in one chain don't cascade to others")
    print()
    print("  4. " + tui.color("Flexibility", "green"))
    print("     Each interface can have specialized capabilities")
    print()
    print("  5. " + tui.color("Evolution", "green"))
    print("     This represents the next generation of TUI design")
    print()
    print(tui.color("Interface chains: The crux of managing all agents safely.", "magenta"))
    print()


if __name__ == "__main__":
    main()
