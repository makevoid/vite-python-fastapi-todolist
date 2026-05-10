import React, { useState } from "react";
import { IoAdd, IoTrash, IoCreate, IoCheckmark, IoClose } from "react-icons/io5";
import useTodos from "./hooks/useTodos.js";

function App() {
  const [newTodoTitle, setNewTodoTitle] = useState("");
  const [newTodoDescription, setNewTodoDescription] = useState("");
  const [editingTodo, setEditingTodo] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");

  const {
    todos,
    isLoading,
    error,
    createTodo,
    updateTodo,
    toggleTodoCompletion,
    deleteTodo,
    isCreating,
    isUpdating,
    isToggling,
    isDeleting,
  } = useTodos();

  const handleCreateTodo = (e) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;
    createTodo({ title: newTodoTitle, description: newTodoDescription });
    setNewTodoTitle("");
    setNewTodoDescription("");
  };

  const handleStartEdit = (todo) => {
    setEditingTodo(todo.id);
    setEditTitle(todo.title);
    setEditDescription(todo.description);
  };

  const handleSaveEdit = () => {
    if (!editTitle.trim()) return;
    updateTodo({ id: editingTodo, updates: { title: editTitle, description: editDescription } });
    setEditingTodo(null);
  };

  const handleCancelEdit = () => setEditingTodo(null);

  const completedCount = todos.filter((t) => t.completed).length;
  const pendingCount = todos.length - completedCount;

  return (
    <div style={{ minHeight: "100vh", background: "#fff" }}>
      {/* Header */}
      <header style={{
        borderBottom: "1px solid #e2e8f0",
        background: "#fff",
        position: "sticky",
        top: 0,
        zIndex: 10,
      }}>
        <div style={{ maxWidth: 680, margin: "0 auto", padding: "20px 24px", display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
          <div>
            <h1 style={{
              fontFamily: "'Fraunces', Georgia, serif",
              fontWeight: 400,
              fontSize: "clamp(26px, 4vw, 34px)",
              color: "#1e3a8a",
              margin: 0,
              letterSpacing: "-0.5px",
              lineHeight: 1.1,
            }}>
              Todo List App
            </h1>
            <p style={{ margin: "4px 0 0", fontSize: 13, color: "#94a3b8", fontWeight: 500 }}>
              Keep things moving
            </p>
          </div>
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <span style={{
              fontSize: 12,
              fontWeight: 600,
              padding: "4px 10px",
              borderRadius: 20,
              background: "#eff6ff",
              color: "#2563eb",
              border: "1px solid #dbeafe",
              letterSpacing: "0.3px",
            }}>
              {pendingCount} pending
            </span>
            <span style={{
              fontSize: 12,
              fontWeight: 600,
              padding: "4px 10px",
              borderRadius: 20,
              background: "#f8fafc",
              color: "#64748b",
              border: "1px solid #e2e8f0",
            }}>
              {completedCount} done
            </span>
          </div>
        </div>
      </header>

      <main style={{ maxWidth: 680, margin: "0 auto", padding: "40px 24px 80px" }}>

        {/* Create form */}
        <form onSubmit={handleCreateTodo} style={{ marginBottom: 48 }}>
          <div style={{ marginBottom: 10 }}>
            <input
              className="todo-input"
              placeholder="What needs to be done?"
              value={newTodoTitle}
              onChange={(e) => setNewTodoTitle(e.target.value)}
              data-testid="todo-title-input"
              style={{ fontSize: 15, fontWeight: 500 }}
            />
          </div>
          <div style={{ marginBottom: 12 }}>
            <textarea
              className="todo-input"
              placeholder="Add a note (optional)"
              value={newTodoDescription}
              onChange={(e) => setNewTodoDescription(e.target.value)}
              data-testid="todo-description-input"
              rows={2}
            />
          </div>
          <button
            type="submit"
            data-testid="create-todo-btn"
            disabled={isCreating || !newTodoTitle.trim()}
            style={{
              fontFamily: "'Plus Jakarta Sans', sans-serif",
              display: "flex",
              alignItems: "center",
              gap: 6,
              padding: "10px 20px",
              background: newTodoTitle.trim() ? "#2563eb" : "#dbeafe",
              color: newTodoTitle.trim() ? "#fff" : "#93c5fd",
              border: "none",
              borderRadius: 8,
              fontSize: 14,
              fontWeight: 600,
              cursor: newTodoTitle.trim() ? "pointer" : "default",
              transition: "all 0.15s",
              letterSpacing: "0.2px",
            }}
            onMouseEnter={(e) => { if (newTodoTitle.trim()) e.currentTarget.style.background = "#1d4ed8"; }}
            onMouseLeave={(e) => { if (newTodoTitle.trim()) e.currentTarget.style.background = "#2563eb"; }}
          >
            <IoAdd size={16} />
            {isCreating ? "Adding…" : "Add task"}
          </button>
        </form>

        {/* Divider with label */}
        {todos.length > 0 && (
          <div style={{ marginBottom: 8, display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{ fontSize: 11, fontWeight: 700, color: "#94a3b8", letterSpacing: "1.2px", textTransform: "uppercase" }}>
              Tasks
            </span>
            <div style={{ flex: 1, height: 1, background: "#e2e8f0" }} />
          </div>
        )}

        {/* Error */}
        {error && (
          <div style={{ padding: "12px 16px", background: "#fef2f2", border: "1px solid #fecaca", borderRadius: 8, color: "#dc2626", fontSize: 14, marginBottom: 24 }}>
            Failed to load todos — {error.message}
          </div>
        )}

        {/* Loading */}
        {isLoading && (
          <div style={{ textAlign: "center", padding: "48px 0", color: "#94a3b8", fontSize: 14 }}>
            Loading…
          </div>
        )}

        {/* Empty state */}
        {!isLoading && todos.length === 0 && (
          <div style={{ textAlign: "center", padding: "64px 0" }}>
            <div style={{
              fontFamily: "'Fraunces', Georgia, serif",
              fontSize: 48,
              color: "#dbeafe",
              marginBottom: 16,
              fontStyle: "italic",
            }}>✓</div>
            <p style={{ color: "#94a3b8", fontSize: 15, margin: 0 }}>No todos yet</p>
            <p style={{ color: "#cbd5e1", fontSize: 13, margin: "6px 0 0" }}>Add your first task above</p>
          </div>
        )}

        {/* Todo list */}
        {!isLoading && todos.length > 0 && (
          <div style={{ paddingLeft: 24 }}>
            {todos.map((todo) => (
              <div
                key={todo.id}
                className="todo-item todo-row"
                data-testid={`todo-${todo.id}`}
              >
                {editingTodo === todo.id ? (
                  /* Edit mode */
                  <div style={{ flex: 1 }}>
                    <input
                      className="todo-input"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      data-testid={`edit-title-${todo.id}`}
                      style={{ marginBottom: 8, fontWeight: 500 }}
                    />
                    <textarea
                      className="todo-input"
                      value={editDescription}
                      onChange={(e) => setEditDescription(e.target.value)}
                      data-testid={`edit-description-${todo.id}`}
                      rows={2}
                      style={{ marginBottom: 10 }}
                    />
                    <div style={{ display: "flex", gap: 8 }}>
                      <button
                        onClick={handleSaveEdit}
                        data-testid={`save-edit-${todo.id}`}
                        disabled={isUpdating}
                        style={{
                          fontFamily: "'Plus Jakarta Sans', sans-serif",
                          display: "flex", alignItems: "center", gap: 4,
                          padding: "7px 14px", background: "#2563eb", color: "#fff",
                          border: "none", borderRadius: 6, fontSize: 13, fontWeight: 600, cursor: "pointer",
                        }}
                      >
                        <IoCheckmark size={14} /> Save
                      </button>
                      <button
                        onClick={handleCancelEdit}
                        data-testid={`cancel-edit-${todo.id}`}
                        style={{
                          fontFamily: "'Plus Jakarta Sans', sans-serif",
                          display: "flex", alignItems: "center", gap: 4,
                          padding: "7px 14px", background: "transparent", color: "#64748b",
                          border: "1.5px solid #e2e8f0", borderRadius: 6, fontSize: 13, fontWeight: 600, cursor: "pointer",
                        }}
                      >
                        <IoClose size={14} /> Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  /* View mode */
                  <>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
                        <input
                          type="checkbox"
                          className="todo-checkbox"
                          checked={todo.completed}
                          onChange={() => toggleTodoCompletion(todo.id)}
                          data-testid={`toggle-${todo.id}`}
                          disabled={isToggling}
                          style={{ flexShrink: 0 }}
                        />
                        <p
                          data-testid={`title-${todo.id}`}
                          style={{
                            margin: 0,
                            fontSize: 15,
                            fontWeight: 500,
                            color: todo.completed ? "#94a3b8" : "#0f172a",
                            textDecoration: todo.completed ? "line-through" : "none",
                            transition: "color 0.2s",
                            lineHeight: 1.4,
                          }}
                        >
                          {todo.title}
                        </p>
                      </div>
                      {todo.description && (
                        <p
                          data-testid={`description-${todo.id}`}
                          style={{
                            margin: "4px 0 0",
                            paddingLeft: 34,
                            fontSize: 13,
                            color: todo.completed ? "#cbd5e1" : "#64748b",
                            lineHeight: 1.5,
                          }}
                        >
                          {todo.description}
                        </p>
                      )}
                    </div>
                    <div style={{ display: "flex", gap: 4 }} className="todo-actions">
                      <button
                        onClick={() => handleStartEdit(todo)}
                        data-testid={`edit-${todo.id}`}
                        aria-label="Edit"
                        style={{
                          background: "none", border: "none", cursor: "pointer",
                          color: "#94a3b8", padding: 6, borderRadius: 6,
                          display: "flex", alignItems: "center", transition: "color 0.15s, background 0.15s",
                        }}
                        onMouseEnter={(e) => { e.currentTarget.style.color = "#2563eb"; e.currentTarget.style.background = "#eff6ff"; }}
                        onMouseLeave={(e) => { e.currentTarget.style.color = "#94a3b8"; e.currentTarget.style.background = "none"; }}
                      >
                        <IoCreate size={16} />
                      </button>
                      <button
                        onClick={() => deleteTodo(todo.id)}
                        data-testid={`delete-${todo.id}`}
                        aria-label="Delete"
                        disabled={isDeleting}
                        style={{
                          background: "none", border: "none", cursor: "pointer",
                          color: "#94a3b8", padding: 6, borderRadius: 6,
                          display: "flex", alignItems: "center", transition: "color 0.15s, background 0.15s",
                        }}
                        onMouseEnter={(e) => { e.currentTarget.style.color = "#dc2626"; e.currentTarget.style.background = "#fef2f2"; }}
                        onMouseLeave={(e) => { e.currentTarget.style.color = "#94a3b8"; e.currentTarget.style.background = "none"; }}
                      >
                        <IoTrash size={16} />
                      </button>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{
        borderTop: "1px solid #e2e8f0",
        padding: "20px 24px",
        textAlign: "center",
      }}>
        <p style={{ margin: 0, fontSize: 12, color: "#cbd5e1" }}>
          <a
            href="https://github.com/makevoid/vite-python-fastapi-todolist"
            rel="noopener noreferrer"
            style={{ color: "#94a3b8", textDecoration: "none", fontWeight: 500 }}
            onMouseEnter={(e) => e.currentTarget.style.color = "#2563eb"}
            onMouseLeave={(e) => e.currentTarget.style.color = "#94a3b8"}
          >
            View on GitHub
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
