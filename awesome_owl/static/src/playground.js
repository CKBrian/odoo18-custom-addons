/** @odoo-module **/
import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };
    static props = {};
    cards = [
        { title: "my title", content: "some content" },
        { title: "Another Card Title", content: "This is another card content" },
        { title: "Trusted HTML", content: markup("<h1>Trusted HTML</h1>") },
        { title: "Untrusted HTML", content: "<h1>Untrusted HTML</h1>" },
    ];

    setup() {
        this.state = useState({ sum: 2 });
    }

    /**
     * Increments the sum of the state by the given value.
     * @param {Number} value the value to increment by
     */
    incrementSum(value) {
        this.state.sum += value;
    }
}
