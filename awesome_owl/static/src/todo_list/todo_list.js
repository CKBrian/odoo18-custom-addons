/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item.js";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static props = {};
    static components = { TodoItem };

    setup() {
        this.todos = useState([{ id: 3, description: "buy milk", isCompleted: false }]);
    }
}
