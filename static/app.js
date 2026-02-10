/**
 * Todo List Application
 * Handles CRUD operations with the FastAPI backend
 */

const API_BASE = '/api/todos';

// DOM Elements
const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');
const emptyState = document.getElementById('empty-state');
const todoCount = document.getElementById('todo-count');
const completedCount = document.getElementById('completed-count');

// State
let todos = [];

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    fetchTodos();
    todoForm.addEventListener('submit', handleAddTodo);
});

// Fetch all todos
async function fetchTodos() {
    try {
        const response = await fetch(API_BASE);
        if (!response.ok) throw new Error('Failed to fetch todos');
        todos = await response.json();
        renderTodos();
    } catch (error) {
        console.error('Error fetching todos:', error);
    }
}

// Add new todo
async function handleAddTodo(e) {
    e.preventDefault();
    const title = todoInput.value.trim();
    if (!title) return;

    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title })
        });

        if (!response.ok) throw new Error('Failed to create todo');

        const newTodo = await response.json();
        todos.push(newTodo);
        renderTodos();
        todoInput.value = '';
        todoInput.focus();
    } catch (error) {
        console.error('Error creating todo:', error);
    }
}

// Toggle todo completion
async function toggleTodo(id) {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completed: !todo.completed })
        });

        if (!response.ok) throw new Error('Failed to update todo');

        const updatedTodo = await response.json();
        todos = todos.map(t => t.id === id ? updatedTodo : t);
        renderTodos();
    } catch (error) {
        console.error('Error updating todo:', error);
    }
}

// Delete todo
async function deleteTodo(id) {
    const todoItem = document.querySelector(`[data-id="${id}"]`);
    if (todoItem) {
        todoItem.style.animation = 'slideOut 0.3s ease forwards';
    }

    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete todo');

        // Wait for animation
        setTimeout(() => {
            todos = todos.filter(t => t.id !== id);
            renderTodos();
        }, 280);
    } catch (error) {
        console.error('Error deleting todo:', error);
        if (todoItem) {
            todoItem.style.animation = '';
        }
    }
}

// Render todos
function renderTodos() {
    todoList.innerHTML = todos.map(todo => `
        <li class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo.id}">
            <label class="checkbox-wrapper">
                <input 
                    type="checkbox" 
                    ${todo.completed ? 'checked' : ''} 
                    onchange="toggleTodo('${todo.id}')"
                >
                <span class="checkmark"></span>
            </label>
            <span class="todo-text">${escapeHtml(todo.title)}</span>
            <button class="delete-btn" onclick="deleteTodo('${todo.id}')" aria-label="Delete todo">
                🗑️
            </button>
        </li>
    `).join('');

    updateStats();
    updateEmptyState();
}

// Update statistics
function updateStats() {
    const total = todos.length;
    const completed = todos.filter(t => t.completed).length;

    todoCount.textContent = `${total} task${total !== 1 ? 's' : ''}`;
    completedCount.textContent = `${completed} completed`;
}

// Update empty state visibility
function updateEmptyState() {
    if (todos.length === 0) {
        emptyState.classList.remove('hidden');
        todoList.style.display = 'none';
    } else {
        emptyState.classList.add('hidden');
        todoList.style.display = 'flex';
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
