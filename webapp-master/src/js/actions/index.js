export const ADD_POINTS = 'ADD_POINTS';
export const SET_TIME = 'SET_TIME';
export const ADD_TEXT = 'ADD_TEXT';

export function addPoints(satellites, lines, stations) {
	return { type: ADD_POINTS, satellites, lines, stations }
}

export function setTime(time) {
	return { type: SET_TIME, time }
}

export function addText(text) {
	return { type: ADD_TEXT, text }
}