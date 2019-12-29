import { ADD_TEXT } from "../actions";

const initialState = {
	text: []
};

export default (state = initialState, action) => {
    switch (action.type) {
	    case ADD_TEXT:
    		return {
			    ...state, text: [...state.text, action.text]
		    };
	    default:
	    	return state
    }
};
