#!/usr/bin/env python3
"""
Test script for Agent Interface Chain Manager.
Verifies core functionality without user interaction.
"""

import sys
from agent_manager import Agent, Interface, InterfaceChain, AgentManager


def test_agent_creation():
    """Test agent creation and management."""
    print("Testing agent creation...")
    agent = Agent(id="test1", name="TestAgent", status="idle")
    assert agent.id == "test1"
    assert agent.name == "TestAgent"
    assert agent.status == "idle"
    
    agent.activate()
    assert agent.status == "active"
    
    agent.deactivate()
    assert agent.status == "idle"
    print("  ✓ Agent creation and state management")


def test_interface_chain():
    """Test interface chain creation."""
    print("Testing interface chain...")
    chain = InterfaceChain()
    
    i1 = Interface(id="i1", name="First")
    i2 = Interface(id="i2", name="Second")
    i3 = Interface(id="i3", name="Third")
    
    chain.add_interface(i1)
    chain.add_interface(i2)
    chain.add_interface(i3)
    
    assert len(chain.interfaces) == 3
    assert chain.head == i1
    assert chain.tail == i3
    assert i1.next_interface == i2
    assert i2.next_interface == i3
    assert i2.prev_interface == i1
    print("  ✓ Interface chain creation and linking")


def test_agent_manager():
    """Test agent manager functionality."""
    print("Testing agent manager...")
    manager = AgentManager()
    
    # Register agents
    a1 = Agent(id="a1", name="Agent1")
    a2 = Agent(id="a2", name="Agent2")
    
    manager.register_agent(a1)
    manager.register_agent(a2)
    
    assert len(manager.list_agents()) == 2
    assert manager.get_agent("a1") == a1
    assert manager.get_agent("a2") == a2
    print("  ✓ Agent registration and retrieval")
    
    # Create chain
    chain = manager.create_interface_chain()
    i1 = Interface(id="i1", name="Interface1")
    i2 = Interface(id="i2", name="Interface2")
    
    chain.add_interface(i1)
    chain.add_interface(i2)
    
    # Attach agents
    result1 = manager.attach_agent_to_interface("a1", "i1")
    result2 = manager.attach_agent_to_interface("a2", "i2")
    
    assert result1 == True
    assert result2 == True
    assert a1.interface == i1
    assert a2.interface == i2
    assert i1.agent == a1
    assert i2.agent == a2
    print("  ✓ Agent-interface attachment")


def test_command_system():
    """Test interface command system."""
    print("Testing command system...")
    interface = Interface(id="test", name="TestInterface")
    
    # Register commands
    def cmd1(x):
        return x * 2
    
    def cmd2(x, y):
        return x + y
    
    interface.register_command("double", cmd1)
    interface.register_command("add", cmd2)
    
    assert "double" in interface.commands
    assert "add" in interface.commands
    
    result1 = interface.execute_command("double", 5)
    assert result1 == 10
    
    result2 = interface.execute_command("add", 3, 7)
    assert result2 == 10
    
    result3 = interface.execute_command("nonexistent")
    assert result3 is None
    print("  ✓ Command registration and execution")


def test_multiple_chains():
    """Test multiple independent chains."""
    print("Testing multiple chains...")
    manager = AgentManager()
    
    # Create two chains
    chain1 = manager.create_interface_chain()
    chain2 = manager.create_interface_chain()
    
    assert len(manager.interface_chains) == 2
    assert manager.active_chain == chain1
    
    # Add interfaces to each chain
    i1 = Interface(id="i1", name="Chain1-Interface1")
    i2 = Interface(id="i2", name="Chain2-Interface1")
    
    chain1.add_interface(i1)
    chain2.add_interface(i2)
    
    assert len(chain1.interfaces) == 1
    assert len(chain2.interfaces) == 1
    assert chain1.head != chain2.head
    print("  ✓ Multiple independent chains")


def test_agent_metadata():
    """Test agent metadata."""
    print("Testing agent metadata...")
    agent = Agent(
        id="meta1",
        name="MetadataAgent",
        metadata={"type": "processor", "priority": "high", "version": "1.0"}
    )
    
    assert agent.metadata["type"] == "processor"
    assert agent.metadata["priority"] == "high"
    assert agent.metadata["version"] == "1.0"
    print("  ✓ Agent metadata storage")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Agent Interface Chain Manager - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_agent_creation,
        test_interface_chain,
        test_agent_manager,
        test_command_system,
        test_multiple_chains,
        test_agent_metadata,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Test error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
