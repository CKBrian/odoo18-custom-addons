/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item.js";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static props = {};
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "learn to use Odoo's qweb syntax", isCompleted: false },
            { id: 2, description: "learn how to use the Odoo's build-in components", isCompleted: false },
            { id: 3, description: "learn how to build the Odoo Dashboard component", isCompleted: false }]);
    }
}
