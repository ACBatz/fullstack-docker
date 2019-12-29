import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import Globe from './Globe';
import InfoPanel from './InfoPanel';

require('../../css/bootstrap.min.css');
require('../../css/app.css');

class App extends React.Component {

	render() {
		return (
			<div className="root-element">
				<div className="row">
					<div className="col-sm-10 globe-container">
						<Globe/>
					</div>
					<div className="col-sm-2 message-container">
						<InfoPanel/>
					</div>
				</div>
			</div>
		)
	}
}

App.propTypes = {

};

function mapStateToProps(state) {
	return {

	}
}

function mapDispatchToProps(dispatch) {
	return {

	}
}

export default connect(mapStateToProps, mapDispatchToProps)(App);