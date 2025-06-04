import { Component, useState } from "@odoo/owl";

export class Card extends Component {
	static props = {
		title: { type: String, optional: false },
		slots: true,
	};
	static template = "awesome_owl.card";
	setup() {
		this.cardState = useState({ isOpen: true });
	}
}
