/** @odoo-module **/
import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item.js";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static props = {};
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1; // Counter for unique IDs
        this.inputRef = useRef("todo_input")
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {
        // Check if Enter key was pressed
        if (ev.keyCode === 13) {
            const input = ev.target;
            const description = input.value.trim();

            // Bonus: Don't create todo if input is empty
            if (description) {
                // Create new todo object
                const newTodo = {
                    id: this.nextId++,
                    description: description,
                    isCompleted: false
                };

                // Add to todos array
                this.todos.push(newTodo);

                // Clear input
                input.value = '';
            }
        }
    }

    toggleState(id) {
        this.todos.forEach(todo => {
            if (todo.id === id) {
                todo.isCompleted = !todo.isCompleted;
            }
        });
    }

    removeTodo(id) {
        this.todos.splice(0, this.todos.length, ...this.todos.filter(todo => todo.id !== id));
        console.log(`Todo with id ${id} removed\n todo list:`, this.todos);
    }

}
