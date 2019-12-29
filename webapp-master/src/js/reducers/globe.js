import { ADD_POINTS, SET_TIME } from "../actions";

const initialState = {
	satellites: [],
	stations: [],
	lines: false,
	radius: 1,
	time: null
};

export default (state = initialState, action) => {
    switch (action.type) {
	    case ADD_POINTS:
    		return {
			    ...state, satellites: action.satellites, lines: action.lines, stations: action.stations
		    };
	    case SET_TIME:
	    	return {
			    ...state, time: action.time
		    };
	    default:
	    	return state
    }
};
