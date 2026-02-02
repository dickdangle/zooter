# Usage Guide - Agent Interface Chain Manager

## Quick Reference

### Available Scripts

#### 1. Basic Demo (`agent_manager.py`)
Simple demonstration of the core concepts.

```bash
python3 agent_manager.py
```

**Shows:**
- Three agents (DataCollector, Analyzer, Reporter)
- Single interface chain with three interfaces
- Agent-to-interface attachments
- TUI rendering

#### 2. Interactive TUI (`interactive_tui.py`)
Full interactive terminal interface for managing agents.

```bash
python3 interactive_tui.py
```

**Features:**
- Real-time agent status display
- Multiple interface chains
- Interactive agent activation/deactivation
- System statistics view
- Menu-driven interface

**Controls:**
- `[1]` - Activate an agent
- `[2]` - Deactivate an agent
- `[3]` - Show system statistics
- `[4]` - Toggle all agents
- `[5]` - Refresh view
- `[q]` - Quit

#### 3. Comprehensive Demo (`demo_comprehensive.py`)
Step-by-step demonstrations of various features.

```bash
python3 demo_comprehensive.py
```

**Includes:**
- Basic chain setup
- Multiple independent chains
- Command handling
- Scalability demonstration

#### 4. Visual Comparison (`visual_demo.py`)
Visual comparison of single interface vs. interface chains.

```bash
python3 visual_demo.py
```

**Illustrates:**
- Problems with single interface architecture
- Benefits of interface chain architecture
- ASCII art diagrams

#### 5. Test Suite (`test_agent_manager.py`)
Automated tests for core functionality.

```bash
python3 test_agent_manager.py
```

**Tests:**
- Agent creation and state management
- Interface chain creation
- Agent manager operations
- Command system
- Multiple chains
- Metadata handling

## Programming Examples

### Creating a Simple Chain

```python
from agent_manager import Agent, Interface, AgentManager

# Initialize manager
manager = AgentManager()

# Create agents
agent1 = Agent(id="a1", name="Worker")
manager.register_agent(agent1)

# Create chain
chain = manager.create_interface_chain()

# Add interface
interface = Interface(id="i1", name="WorkInterface")
chain.add_interface(interface)

# Attach agent to interface
manager.attach_agent_to_interface("a1", "i1")

# Activate agent
agent1.activate()
```

### Building Multiple Chains

```python
# Create first chain for processing
processing_chain = manager.create_interface_chain()
processing_chain.add_interface(Interface("p1", "Input"))
processing_chain.add_interface(Interface("p2", "Process"))

# Create second chain for monitoring
monitor_chain = manager.create_interface_chain()
monitor_chain.add_interface(Interface("m1", "Monitor"))
monitor_chain.add_interface(Interface("m2", "Alert"))
```

### Registering Commands

```python
from agent_manager import Interface

interface = Interface(id="cmd", name="CommandInterface")

# Define command handler
def process_data(data):
    return f"Processed: {data}"

# Register command
interface.register_command("process", process_data)

# Execute command
result = interface.execute_command("process", "test data")
print(result)  # Output: Processed: test data
```

### Using Agent Metadata

```python
from agent_manager import Agent

agent = Agent(
    id="specialized",
    name="SpecializedAgent",
    metadata={
        "type": "processor",
        "priority": "high",
        "version": "1.0",
        "capabilities": ["transform", "validate", "route"]
    }
)

# Access metadata
print(agent.metadata["type"])  # processor
print(agent.metadata["capabilities"])  # ['transform', 'validate', 'route']
```

## Architecture Patterns

### Pattern 1: Linear Processing Chain
Best for sequential data processing pipelines.

```
Interface1 → Agent1 (Collect)
    ↓
Interface2 → Agent2 (Transform)
    ↓
Interface3 → Agent3 (Output)
```

### Pattern 2: Parallel Chains
Best for independent subsystems.

```
Chain A: Monitoring → Alerting
Chain B: Processing → Storage
Chain C: Analytics → Reporting
```

### Pattern 3: Fan-out Distribution
Best for load distribution.

```
                    ┌→ Chain1 → Agent1
Main Interface ────→ Chain2 → Agent2
                    └→ Chain3 → Agent3
```

## Best Practices

1. **Keep Chains Focused**: Each chain should handle a specific concern
2. **One Agent Per Interface**: Maintain 1:1 relationship for clarity
3. **Use Metadata**: Store agent-specific configuration in metadata
4. **Independent Chains**: Design chains to operate independently
5. **Command Registration**: Pre-register all commands during setup
6. **Status Management**: Use status field to track agent state
7. **Error Isolation**: Handle errors within chain boundaries

## Troubleshooting

### Agent Not Appearing in Chain
- Verify agent is registered: `manager.get_agent(agent_id)`
- Check interface exists: `chain.get_interface(interface_id)`
- Ensure attachment succeeded: check return value

### Command Not Executing
- Verify command is registered: `command in interface.commands`
- Check command name spelling
- Ensure proper arguments passed

### Chain Not Linking
- Verify interfaces added in order: use `chain.add_interface()`
- Check chain traverse: `chain.traverse()`

## Extending the System

### Adding Custom Agent Types

```python
from agent_manager import Agent

class CustomAgent(Agent):
    def __init__(self, id, name, custom_param):
        super().__init__(id, name)
        self.custom_param = custom_param
    
    def custom_method(self):
        return f"Custom: {self.custom_param}"
```

### Adding Custom Interface Behaviors

```python
from agent_manager import Interface

class CustomInterface(Interface):
    def __init__(self, id, name, config):
        super().__init__(id, name)
        self.config = config
    
    def custom_operation(self):
        # Custom logic here
        pass
```

## Performance Considerations

- Chains scale linearly with number of interfaces
- Agent operations are O(1) for lookup
- Interface traversal is O(n) where n is chain length
- No performance penalty for multiple independent chains

## Security Notes

- Each interface provides isolation boundary
- Agent failures don't cascade to other chains
- Command system allows controlled agent interaction
- Metadata can store security context per agent

---

For more information, see [INTERFACE_CHAINS.md](INTERFACE_CHAINS.md)
