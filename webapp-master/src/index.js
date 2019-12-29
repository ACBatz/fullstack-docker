import React from 'react';
import { render } from 'react-dom';
import { Provider } from "react-redux";
import { store } from './js/store';
import App from './js/components/App';

import './css/index.css';

import * as serviceWorker from './js/serviceWorker';

render(
	<Provider store={store}>
		<App />
	</Provider>,
	document.getElementById("root")
);

serviceWorker.unregister();
