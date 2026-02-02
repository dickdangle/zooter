#!/usr/bin/env python3
"""
Agent Interface Chain Manager
The next evolution of TUIs for managing multiple agents safely.
"""

import sys
import time
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class Agent:
    """Represents an agent in the system."""
    id: str
    name: str
    status: str = "idle"
    interface: Optional['Interface'] = None
    metadata: Dict = field(default_factory=dict)
    
    def activate(self):
        """Activate the agent."""
        self.status = "active"
    
    def deactivate(self):
        """Deactivate the agent."""
        self.status = "idle"
    
    def update_status(self, status: str):
        """Update agent status."""
        self.status = status


@dataclass
class Interface:
    """A single interface in the chain."""
    id: str
    name: str
    agent: Optional[Agent] = None
    next_interface: Optional['Interface'] = None
    prev_interface: Optional['Interface'] = None
    commands: Dict[str, Callable] = field(default_factory=dict)
    
    def chain_to(self, next_interface: 'Interface'):
        """Chain this interface to the next one."""
        self.next_interface = next_interface
        next_interface.prev_interface = self
    
    def register_command(self, command: str, handler: Callable):
        """Register a command handler."""
        self.commands[command] = handler
    
    def execute_command(self, command: str, *args, **kwargs):
        """Execute a command on this interface."""
        if command in self.commands:
            return self.commands[command](*args, **kwargs)
        return None


class InterfaceChain:
    """Manages a chain of interfaces."""
    
    def __init__(self):
        self.head: Optional[Interface] = None
        self.tail: Optional[Interface] = None
        self.interfaces: List[Interface] = []
    
    def add_interface(self, interface: Interface):
        """Add an interface to the chain."""
        self.interfaces.append(interface)
        if not self.head:
            self.head = interface
            self.tail = interface
        else:
            self.tail.chain_to(interface)
            self.tail = interface
    
    def get_interface(self, interface_id: str) -> Optional[Interface]:
        """Get an interface by ID."""
        for interface in self.interfaces:
            if interface.id == interface_id:
                return interface
        return None
    
    def traverse(self) -> List[Interface]:
        """Traverse the chain and return all interfaces."""
        return self.interfaces


class AgentManager:
    """Manages multiple agents with interface chains."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.interface_chains: List[InterfaceChain] = []
        self.active_chain: Optional[InterfaceChain] = None
    
    def register_agent(self, agent: Agent):
        """Register a new agent."""
        self.agents[agent.id] = agent
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID."""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Agent]:
        """List all registered agents."""
        return list(self.agents.values())
    
    def create_interface_chain(self) -> InterfaceChain:
        """Create a new interface chain."""
        chain = InterfaceChain()
        self.interface_chains.append(chain)
        if not self.active_chain:
            self.active_chain = chain
        return chain
    
    def attach_agent_to_interface(self, agent_id: str, interface_id: str):
        """Attach an agent to a specific interface."""
        agent = self.get_agent(agent_id)
        if not agent:
            return False
        
        # Search for interface across all chains, not just active chain
        for chain in self.interface_chains:
            interface = chain.get_interface(interface_id)
            if interface:
                interface.agent = agent
                agent.interface = interface
                return True
        return False


class TUI:
    """Text User Interface renderer."""
    
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'cyan': '\033[96m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'magenta': '\033[95m',
    }
    
    @staticmethod
    def clear():
        """Clear the screen."""
        print("\033[2J\033[H", end='')
    
    @staticmethod
    def color(text: str, color: str) -> str:
        """Colorize text."""
        return f"{TUI.COLORS.get(color, '')}{text}{TUI.COLORS['reset']}"
    
    @staticmethod
    def draw_box(title: str, content: List[str], width: int = 60):
        """Draw a box with content."""
        border = "═" * (width - 2)
        print(f"╔{border}╗")
        title_centered = title.center(width - 2)
        print(f"║{title_centered}║")
        print(f"╠{border}╣")
        for line in content:
            padding = " " * (width - 2 - len(line))
            print(f"║{line}{padding}║")
        print(f"╚{border}╝")
    
    @staticmethod
    def render_agent_list(agents: List[Agent]):
        """Render a list of agents."""
        content = []
        for agent in agents:
            status_color = 'green' if agent.status == 'active' else 'yellow'
            status = TUI.color(f"[{agent.status}]", status_color)
            content.append(f"  {status} {agent.name} (ID: {agent.id})")
        
        if not content:
            content = ["  No agents registered"]
        
        TUI.draw_box("AGENTS", content)
    
    @staticmethod
    def render_interface_chain(chain: InterfaceChain):
        """Render an interface chain."""
        content = []
        interfaces = chain.traverse()
        
        for i, interface in enumerate(interfaces):
            agent_info = ""
            if interface.agent:
                agent_info = f" → {interface.agent.name}"
            
            connector = " ↓ " if i < len(interfaces) - 1 else ""
            content.append(f"  [{interface.id}] {interface.name}{agent_info}")
            if connector:
                content.append(f"  {connector}")
        
        if not content:
            content = ["  No interfaces in chain"]
        
        TUI.draw_box("INTERFACE CHAIN", content)


def demo():
    """Run a demonstration of the agent interface chain system."""
    manager = AgentManager()
    tui = TUI()
    
    # Register agents
    agent1 = Agent(id="a1", name="DataCollector", status="idle")
    agent2 = Agent(id="a2", name="Analyzer", status="idle")
    agent3 = Agent(id="a3", name="Reporter", status="idle")
    
    manager.register_agent(agent1)
    manager.register_agent(agent2)
    manager.register_agent(agent3)
    
    # Create interface chain
    chain = manager.create_interface_chain()
    
    interface1 = Interface(id="i1", name="InputInterface")
    interface2 = Interface(id="i2", name="ProcessingInterface")
    interface3 = Interface(id="i3", name="OutputInterface")
    
    chain.add_interface(interface1)
    chain.add_interface(interface2)
    chain.add_interface(interface3)
    
    # Attach agents to interfaces
    manager.attach_agent_to_interface("a1", "i1")
    manager.attach_agent_to_interface("a2", "i2")
    manager.attach_agent_to_interface("a3", "i3")
    
    # Activate agents
    agent1.activate()
    agent2.activate()
    agent3.activate()
    
    # Render the system
    tui.clear()
    print(tui.color("\n╔═══════════════════════════════════════════════════════════╗", "cyan"))
    print(tui.color("║         AGENT INTERFACE CHAIN MANAGER v1.0                ║", "cyan"))
    print(tui.color("║      The Next Evolution of TUIs for Agent Management     ║", "cyan"))
    print(tui.color("╚═══════════════════════════════════════════════════════════╝\n", "cyan"))
    
    print(tui.color("Managing all agents through interface chains reduces risk.\n", "green"))
    print(tui.color("No single interface point of failure.\n", "green"))
    
    tui.render_agent_list(manager.list_agents())
    print()
    tui.render_interface_chain(chain)
    
    print(tui.color("\n✓ System initialized successfully", "green"))
    print(tui.color("✓ Interface chain established", "green"))
    print(tui.color("✓ Agents distributed across interfaces\n", "green"))


if __name__ == "__main__":
    demo()
