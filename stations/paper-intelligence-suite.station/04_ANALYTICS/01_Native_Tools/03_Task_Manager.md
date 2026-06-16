# Task Manager
> [!INFO]
> Aggregated view of all tasks across the vault.

## 🔥 Overdue / Due Today
```dataview
TASK
WHERE due <= date(today) AND !completed
```

## 📥 Inbox (No Due Date)
```dataview
TASK
WHERE !due AND !completed AND !contains(tags, "#future")
LIMIT 20
```

## ✅ Recently Completed
```dataview
TASK
WHERE completed
SORT completion.date DESC
LIMIT 10
```
