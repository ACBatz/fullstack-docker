import React from "react";
import { connect } from "react-redux";
import io from "socket.io-client";
import PropTypes from "prop-types";
import { addText } from "../actions";

require('../../css/info-panel.css');

class InfoPanel extends React.Component {

	constructor() {
		super();
		this.state = {
			endpoint: "http://127.0.0.1:5000",
		}
	}

	componentDidMount() {
		const socket = io(this.state.endpoint);
		socket.on('sim', (text) => {
			console.log(text);
			this.props.addText(text['text']);
		});
	}

	handleClick() {
		const socket = io(this.state.endpoint);
		socket.emit('sim');
	}

	render() {
		const { text } = this.props;
		let idx = 0;
		return (
			<div>
				<button onClick={ () => this.handleClick() }>Simulate UCCS -> X</button>
				<h3>Messages</h3>
				{ text.map(t => (<p key={idx++}>{ t }</p>)) }
			</div>
		)
	}
}

InfoPanel.propTypes = {

};

function mapStateToProps(state) {
	return {
		text: state.info_panel.text,
		time: state.globe.time
	}
}

function mapDispatchToProps(dispatch) {
	return {
		addText: text => dispatch(addText(text))
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(InfoPanel);