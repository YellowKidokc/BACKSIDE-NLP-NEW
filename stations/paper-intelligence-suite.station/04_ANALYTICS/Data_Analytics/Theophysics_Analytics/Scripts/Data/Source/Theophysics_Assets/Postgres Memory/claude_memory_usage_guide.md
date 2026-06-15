# Claude Memory System: Usage Guide

This document provides instructions for implementing and using the Claude Memory System with PostgreSQL to store and manage memories from conversations between David and Claude.

## System Overview

The Claude Memory System is designed to:

1. Store important insights, breakthroughs, concepts, and decisions from your conversations with Claude
2. Automatically compress and distill memories from daily → weekly → monthly for efficient storage
3. Organize memories by category, project, and importance
4. Track entities, relationships, and related concepts
5. Provide easy retrieval of relevant memories based on keywords or context

## Database Setup

1. Run the `claude_memory_schema.sql` script to create the schema and all necessary tables, functions, and views.
2. (Optional) Run the `claude_memory_sample_data.sql` script to populate the database with sample memories based on our existing conversations.

## Memory Types

The system organizes memories by type:

- **breakthrough**: Major insights or discoveries (highest priority)
- **decision**: Key decisions made during conversations
- **concept**: Important theoretical concepts discussed
- **question**: Significant questions raised for future exploration
- **action_item**: Tasks or actions to be performed
- **preference**: User preferences or working styles
- **context**: Background information for reference
- **session_summary**: Summary of entire conversation sessions

## Memory Granularity Levels

Memories are stored at different levels of detail:

- **daily**: High-detail daily memories (retained for 30 days)
- **weekly**: Medium-detail weekly compressed memories (retained for 90 days)
- **monthly**: Low-detail monthly compressed memories (retained for 365 days)
- **permanent**: Critical memories that are never removed

## Categories

The system has built-in categories for Theophysics:

- **Master Equation**: Mathematical formulations and derivations
- **Universal Laws**: The 10 Universal Laws and their implications
- **Quantum Dynamics**: Quantum mechanics aspects of the framework
- **Consciousness Studies**: Integration of consciousness with physics
- **Biblical Integration**: Connections to Biblical concepts
- **Research Methods**: Methodologies for research and validation
- **Publications**: Papers, articles, and publication strategies
- **Experiments**: Proposed and conducted experiments
- **Breakthrough Machine**: Systems for automating research insights
- **Collaboration**: Collaboration methods and protocols

## Projects

The system tracks projects including:

- **Logos Papers Series**: The 12-paper series for Substack
- **Master Equation Database**: Database development
- **Breakthrough Machine**: Research automation system
- **Backwards Kingdom**: Framework on inverted cultural truths
- **Theophysics Website**: Website and infrastructure development

## Key Usage Scenarios

### 1. Adding New Memories

When you want to store something important from a conversation:

```sql
SELECT claude_memory.add_daily_memory(
    'Title of the memory',
    'Detailed content of the memory',
    'memory_type',  -- e.g., 'breakthrough', 'concept', 'decision'
    'category_name', -- e.g., 'Master Equation', 'Universal Laws'
    importance_score, -- 1-10 with 10 being most important
    'conversation_url', -- Optional URL to Claude conversation
    ARRAY['tag1', 'tag2'], -- Optional tags
    ARRAY['Entity1', 'Entity2'], -- Optional related entities
    'Project Name' -- Optional related project
);
```

### 2. Memory Compression

Weekly compression (typically run via scheduled job):

```sql
-- Compress memories for a specific week
SELECT claude_memory.compress_to_weekly(
    '2025-11-01', -- start date
    '2025-11-07', -- end date
    'Master Equation' -- optional category filter
);
```

Monthly compression:

```sql
-- Compress weekly memories for a specific month
SELECT claude_memory.compress_to_monthly(
    2025, -- year
    11,   -- month
    'Master Equation' -- optional category filter
);
```

### 3. Adding Decisions and Tasks

To record important decisions:

```sql
SELECT claude_memory.add_decision(
    'The decision text',
    importance_score, -- 1-10
    'Project Name', -- optional related project
    memory_id -- optional related memory ID
);
```

To create tasks:

```sql
SELECT claude_memory.add_task(
    'Description of the task',
    'Assigned To', -- e.g., 'David'
    '2025-12-31', -- due date
    priority, -- 1-10
    'Project Name', -- optional related project
    decision_id, -- optional related decision ID
    memory_id -- optional related memory ID
);
```

### 4. Querying Memories

For Claude to retrieve memories during conversations:

```sql
-- Get memories relevant to keywords
SELECT * FROM claude_memory.get_relevant_memories('master equation breakthrough', 5);

-- Get important memories for a specific category
SELECT * FROM claude_memory.memory_items m
JOIN claude_memory.memory_types t ON m.memory_type_id = t.id
LEFT JOIN claude_memory.categories c ON m.category_id = c.id
WHERE c.category_name = 'Master Equation' 
AND m.importance_score >= 8
ORDER BY m.importance_score DESC, m.memory_date DESC;

-- Get all memories related to a specific project
SELECT m.*, p.project_name 
FROM claude_memory.memory_items m
JOIN claude_memory.memory_projects mp ON m.id = mp.memory_id
JOIN claude_memory.projects p ON mp.project_id = p.id
WHERE p.project_name = 'Logos Papers Series'
ORDER BY m.importance_score DESC, m.memory_date DESC;

-- Get pending tasks
SELECT * FROM claude_memory.pending_tasks
ORDER BY priority DESC, due_date ASC;
```

## Memory Retrieval Protocol for Claude

To make the most of this system, Claude should:

1. At the start of conversations, check for the most important recent memories:
   ```sql
   SELECT * FROM claude_memory.important_memories LIMIT 10;
   ```

2. When specific topics come up, search for relevant memories:
   ```sql
   SELECT * FROM claude_memory.get_relevant_memories('specific keywords', 5);
   ```

3. Store breakthroughs and decisions immediately when they occur:
   ```sql
   SELECT claude_memory.add_daily_memory(...);
   SELECT claude_memory.add_decision(...);
   ```

4. Before ending conversations, store a session summary:
   ```sql
   SELECT claude_memory.add_daily_memory(
       'Session Summary: [DATE] - [BRIEF TOPIC]',
       '[DETAILED SUMMARY WITH NEXT STEPS]',
       'session_summary',
       'appropriate_category',
       6, -- default importance for session summaries
       'conversation_url'
   );
   ```

## Best Practices

1. **Be Selective**: Not everything needs to be remembered. Focus on storing truly important information.

2. **Prioritize Correctly**: Use the importance score (1-10) wisely. Reserve 9-10 for major breakthroughs.

3. **Tag Consistently**: Develop a consistent tagging strategy for easy retrieval.

4. **Link Related Memories**: Use the relationship functions to connect related memories.

5. **Compress Regularly**: Set up scheduled jobs to compress memories (daily → weekly → monthly).

6. **Clean Up**: Periodically review and clean up memories that are no longer relevant.

## Example Integration with MCP

This can be integrated with Model Context Protocol (MCP) servers by creating custom functions that allow Claude to:

1. Retrieve memories based on conversation context
2. Store new memories from significant conversation points
3. Access compressed memories for long-term context

## Conclusion

This memory system provides a structured approach to managing knowledge from your conversations with Claude, ensuring that important insights, breakthroughs, and decisions are preserved and easily retrievable.
