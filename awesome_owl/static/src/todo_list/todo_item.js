/** @odoo-module **/
import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: Object,
        toggleState: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true },
    };

    toggle() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todo.id);
        }
    }
    deleteTodo() {
        if (this.props.removeTodo) {
            this.props.removeTodo(this.props.todo.id);
        }
    }
}