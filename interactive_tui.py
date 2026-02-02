#!/usr/bin/env python3
"""
Interactive Agent Interface Chain TUI
Demonstrates managing multiple agents through chained interfaces.
"""

import sys
import os
from agent_manager import Agent, Interface, InterfaceChain, AgentManager, TUI


class InteractiveTUI:
    """Interactive Terminal User Interface for agent management."""
    
    def __init__(self):
        self.manager = AgentManager()
        self.tui = TUI()
        self.running = True
        self.current_view = "main"
    
    def setup_demo_data(self):
        """Setup demo agents and interface chains."""
        # Create diverse agents
        agents_data = [
            ("a1", "DataCollector", "idle", {"type": "collector", "priority": "high"}),
            ("a2", "Analyzer", "idle", {"type": "processor", "priority": "medium"}),
            ("a3", "Reporter", "idle", {"type": "output", "priority": "low"}),
            ("a4", "Monitor", "idle", {"type": "watcher", "priority": "high"}),
            ("a5", "Validator", "idle", {"type": "checker", "priority": "medium"}),
        ]
        
        for agent_id, name, status, metadata in agents_data:
            agent = Agent(id=agent_id, name=name, status=status, metadata=metadata)
            self.manager.register_agent(agent)
        
        # Create first interface chain
        chain1 = self.manager.create_interface_chain()
        
        interfaces1 = [
            ("i1", "DataIngestion"),
            ("i2", "Processing"),
            ("i3", "Output"),
        ]
        
        for iface_id, name in interfaces1:
            interface = Interface(id=iface_id, name=name)
            chain1.add_interface(interface)
        
        # Attach agents to interfaces
        self.manager.attach_agent_to_interface("a1", "i1")
        self.manager.attach_agent_to_interface("a2", "i2")
        self.manager.attach_agent_to_interface("a3", "i3")
        
        # Create second interface chain
        chain2 = self.manager.create_interface_chain()
        
        interfaces2 = [
            ("i4", "Monitoring"),
            ("i5", "Validation"),
        ]
        
        for iface_id, name in interfaces2:
            interface = Interface(id=iface_id, name=name)
            chain2.add_interface(interface)
        
        # Attach remaining agents
        self.manager.attach_agent_to_interface("a4", "i4")
        self.manager.attach_agent_to_interface("a5", "i5")
    
    def render_header(self):
        """Render the application header."""
        print(self.tui.color("╔═══════════════════════════════════════════════════════════════════╗", "cyan"))
        print(self.tui.color("║        AGENT INTERFACE CHAIN MANAGER - Interactive TUI            ║", "cyan"))
        print(self.tui.color("║          The Next Evolution of Agent Management Systems           ║", "cyan"))
        print(self.tui.color("╚═══════════════════════════════════════════════════════════════════╝", "cyan"))
        print()
    
    def render_main_view(self):
        """Render the main dashboard view."""
        self.tui.clear()
        self.render_header()
        
        print(self.tui.color("✦ CONCEPT: Interface Chains", "magenta"))
        print("  Managing all agents through distributed interfaces eliminates")
        print("  single points of failure. Each chain is independent yet coordinated.\n")
        
        # Show all agents
        agents = self.manager.list_agents()
        print(self.tui.color("═" * 67, "cyan"))
        print(self.tui.color("REGISTERED AGENTS", "bold"))
        print(self.tui.color("═" * 67, "cyan"))
        
        for agent in agents:
            status_symbol = "●" if agent.status == "active" else "○"
            status_color = "green" if agent.status == "active" else "yellow"
            
            interface_info = ""
            if agent.interface:
                interface_info = f" → Interface: {agent.interface.name}"
            
            print(f"  {self.tui.color(status_symbol, status_color)} {self.tui.color(agent.name, 'bold')} (ID: {agent.id}){interface_info}")
        
        print()
        
        # Show all interface chains
        for idx, chain in enumerate(self.manager.interface_chains, 1):
            print(self.tui.color("═" * 67, "cyan"))
            print(self.tui.color(f"INTERFACE CHAIN #{idx}", "bold"))
            print(self.tui.color("═" * 67, "cyan"))
            
            interfaces = chain.traverse()
            for i, interface in enumerate(interfaces):
                agent_info = self.tui.color("(no agent)", "yellow")
                if interface.agent:
                    status = self.tui.color("●", "green") if interface.agent.status == "active" else self.tui.color("○", "yellow")
                    agent_info = f"{status} {self.tui.color(interface.agent.name, 'green')}"
                
                connector = "  ↓" if i < len(interfaces) - 1 else ""
                print(f"  [{interface.id}] {self.tui.color(interface.name, 'cyan')} ← {agent_info}")
                if connector:
                    print(connector)
            
            print()
    
    def render_menu(self):
        """Render the menu options."""
        print(self.tui.color("═" * 67, "cyan"))
        print(self.tui.color("ACTIONS", "bold"))
        print(self.tui.color("═" * 67, "cyan"))
        print("  [1] Activate Agent     [2] Deactivate Agent")
        print("  [3] Show Statistics    [4] Toggle All Agents")
        print("  [5] Refresh View       [q] Quit")
        print(self.tui.color("═" * 67, "cyan"))
        print()
    
    def activate_agent(self, agent_id: str):
        """Activate a specific agent."""
        agent = self.manager.get_agent(agent_id)
        if agent:
            agent.activate()
            return True
        return False
    
    def deactivate_agent(self, agent_id: str):
        """Deactivate a specific agent."""
        agent = self.manager.get_agent(agent_id)
        if agent:
            agent.deactivate()
            return True
        return False
    
    def toggle_all_agents(self):
        """Toggle all agents between active and idle."""
        agents = self.manager.list_agents()
        active_count = sum(1 for a in agents if a.status == "active")
        
        if active_count > len(agents) / 2:
            # Deactivate all
            for agent in agents:
                agent.deactivate()
        else:
            # Activate all
            for agent in agents:
                agent.activate()
    
    def show_statistics(self):
        """Show system statistics."""
        self.tui.clear()
        self.render_header()
        
        agents = self.manager.list_agents()
        active_agents = [a for a in agents if a.status == "active"]
        idle_agents = [a for a in agents if a.status == "idle"]
        
        print(self.tui.color("╔═══════════════════════════════════════════════════════════════════╗", "cyan"))
        print(self.tui.color("║                        SYSTEM STATISTICS                          ║", "cyan"))
        print(self.tui.color("╚═══════════════════════════════════════════════════════════════════╝", "cyan"))
        print()
        
        print(f"  Total Agents:          {len(agents)}")
        print(f"  {self.tui.color('Active Agents:', 'green')}        {len(active_agents)}")
        print(f"  {self.tui.color('Idle Agents:', 'yellow')}          {len(idle_agents)}")
        print(f"  Total Interface Chains: {len(self.manager.interface_chains)}")
        
        total_interfaces = sum(len(chain.traverse()) for chain in self.manager.interface_chains)
        print(f"  Total Interfaces:       {total_interfaces}")
        
        attached_agents = sum(1 for a in agents if a.interface is not None)
        print(f"  Attached Agents:        {attached_agents}")
        
        print()
        print(self.tui.color("  Key Benefits:", "magenta"))
        print("  • No single interface point of failure")
        print("  • Distributed agent management")
        print("  • Scalable chain architecture")
        print("  • Independent yet coordinated operations")
        
        print("\n  Press Enter to return...")
        input()
    
    def run(self):
        """Run the interactive TUI."""
        self.setup_demo_data()
        
        # Activate some agents by default
        self.activate_agent("a1")
        self.activate_agent("a2")
        self.activate_agent("a4")
        
        while self.running:
            self.render_main_view()
            self.render_menu()
            
            try:
                choice = input(self.tui.color("Enter choice: ", "cyan")).strip().lower()
                
                if choice == 'q':
                    self.running = False
                    print(self.tui.color("\n✓ Shutting down agent interface chain manager...", "green"))
                elif choice == '1':
                    agent_id = input("Enter agent ID to activate: ").strip()
                    if self.activate_agent(agent_id):
                        print(self.tui.color(f"✓ Agent {agent_id} activated", "green"))
                    else:
                        print(self.tui.color(f"✗ Agent {agent_id} not found", "red"))
                    input("Press Enter to continue...")
                elif choice == '2':
                    agent_id = input("Enter agent ID to deactivate: ").strip()
                    if self.deactivate_agent(agent_id):
                        print(self.tui.color(f"✓ Agent {agent_id} deactivated", "yellow"))
                    else:
                        print(self.tui.color(f"✗ Agent {agent_id} not found", "red"))
                    input("Press Enter to continue...")
                elif choice == '3':
                    self.show_statistics()
                elif choice == '4':
                    self.toggle_all_agents()
                    print(self.tui.color("✓ All agents toggled", "green"))
                    input("Press Enter to continue...")
                elif choice == '5':
                    # Just refresh by continuing the loop
                    pass
                else:
                    print(self.tui.color("Invalid choice", "red"))
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                self.running = False
                print(self.tui.color("\n\n✓ Shutting down agent interface chain manager...", "green"))
            except EOFError:
                self.running = False
                print(self.tui.color("\n\n✓ Shutting down agent interface chain manager...", "green"))


def main():
    """Main entry point."""
    tui = InteractiveTUI()
    tui.run()


if __name__ == "__main__":
    main()
